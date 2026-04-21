'use strict';

const { URL } = require('url');
const { promisify } = require('util');
const path = require('path');
const fs = require('fs');
const { promises: fsp } = fs;
const stream = require('stream');
const streamPipeline = promisify(stream.pipeline);

const rimraf = promisify(require('rimraf'));
const mkdirp = require('mkdirp');
const archiver = require('archiver');
const fetch = require('node-fetch');
const FormData = require('formdata-node');
const chalk = require('chalk');
const inquirer = require('inquirer');

const { log } = console;
const resolve = (...paths) => path.resolve(__dirname, ...paths);

async function main() {
  const command = process.argv[2];
  switch (command) {
    case 'bootstrap':
      return await commandBootstrap();
    case 'deploy':
      return await commandDeploy();
    case 'package':
      return await commandPackage();
    default:
      throw new Error(`Unknown command, ${command}`);
  }
}

async function commandBootstrap() {
  const existing = await readBootstrap();

  async function promptUrl() {
    if (existing.url) {
      return existing.url;
    }
    const response = await inquirer.prompt([{ type: 'input', name: 'url' }]);
    return response.url;
  }

  const url = await promptUrl();
  const { version, configurationOptions } = await getServerStatus(url);
  await writeBootstrap({ ...existing, url });

  async function promptCredentials() {
    if (existing.accessKey && existing.password) {
      return { accessKey: existing.accessKey, password: existing.password };
    }
    const response = await inquirer.prompt([
      { type: 'input', name: 'accessKey' },
      { type: 'password', name: 'password' }
    ]);
    return response;
  }

  const { accessKey, password } = await promptCredentials();
  const user = await login(url, accessKey, password);
  await writeBootstrap({ url, accessKey, password });

  const pluginsEnabledOption = configurationOptions.find(
    (option) => option.path === 'Features/Plugins/Enabled'
  );
  if (pluginsEnabledOption && !pluginsEnabledOption.value && user.isAdmin) {
    await enablePluginsFeature(url, user.auth);
  }

  log(chalk.dim('Downloading SDK...'));
  await downloadSdk(url);
  log(chalk.green(`  Downloaded ${shortVersion(version)} SDK`));
}

async function commandDeploy() {
  const { url, accessKey, password } = await readBootstrap();
  if (!url || !accessKey || !password) {
    throw new Error('Run the bootstrap command first.');
  }
  const user = await login(url, accessKey, password);
  log(chalk.dim('Uploading plugin...'));
  await postZip(url, user);
  log(chalk.green(`  Uploaded plugin to ${url}`));
}

async function commandPackage() {
  await validateDistHtml();
  const pathToZip = await generateZip();
  log(chalk.green(`  Created ${pathToZip}`));
}

async function writeBootstrap({ url, accessKey, password }) {
  await fsp.writeFile(
    resolve('../.credentials.json'),
    JSON.stringify({ url, username: accessKey, password }, null, 2),
    'utf8'
  );
}

async function readBootstrap() {
  let contents = {};
  try {
    contents = JSON.parse(await fsp.readFile(resolve('../.credentials.json'), 'utf8'));
  } catch (error) {
    if (error.code !== 'ENOENT') {
      throw error;
    }
  }
  return {
    url: contents.url || 'http://localhost:34216',
    accessKey: contents.username || null,
    password: contents.password || null
  };
}

function base(url) {
  const { origin } = new URL(url);
  return origin;
}

async function getServerStatus(url) {
  const res = await fetch(`${base(url)}/api/system/server-status`, {
    headers: { Accept: 'application/vnd.seeq.v1+json' }
  });
  if (!res.ok) {
    throw new Error(`Request failed /api/system/server-status ${res.status}`);
  }
  return await res.json();
}

async function login(url, username, password) {
  const res = await fetch(`${base(url)}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/vnd.seeq.v1+json',
      Accept: 'application/vnd.seeq.v1+json'
    },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    const err = new Error(`Request failed /api/auth/login ${res.status}`);
    err.data = await res.text();
    throw err;
  }

  const body = await res.json();
  return {
    auth: res.headers.get('x-sq-auth'),
    id: body.id,
    isAdmin: body.isAdmin
  };
}

async function enablePluginsFeature(url, auth) {
  await fetch(`${base(url)}/api/system/configuration/options`, {
    method: 'POST',
    headers: {
      'x-sq-auth': auth,
      'Content-Type': 'application/vnd.seeq.v1+json',
      Accept: 'application/vnd.seeq.v1+json'
    },
    body: JSON.stringify({
      configurationOptions: [{ note: '', path: 'Features/Plugins/Enabled', value: true }]
    })
  });
}

async function downloadFile(url, filename, destination) {
  const res = await fetch(`${base(url)}/api/plugins/sdk/${filename}`);
  if (!res.ok) {
    throw new Error(`Request failed /api/plugins/sdk/${filename} ${res.status}`);
  }
  return await streamPipeline(res.body, fs.createWriteStream(path.resolve(destination, filename)));
}

async function downloadSdk(url) {
  const { version } = await getServerStatus(url);
  await rimraf(resolve('sdk'));
  await mkdirp(resolve('sdk'));
  await fsp.writeFile(resolve('sdk', 'version.txt'), version, 'utf8');
  for (const file of ['seeq.d.ts', 'seeq.js', 'seeq.css']) {
    await downloadFile(url, file, resolve('sdk'));
  }
}

function shortVersion(version) {
  return version.replace(/^(R\d+)\..*$/, '$1');
}

async function createArchive() {
  let seeqVersion;
  try {
    seeqVersion = (await fsp.readFile(resolve('sdk', 'version.txt'), 'utf8')).trim();
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error(
        'Missing frontend/sdk/version.txt. Run the bootstrap command against a Seeq server before packaging the plugin.'
      );
    }
    throw error;
  }
  const pluginJson = JSON.parse(await fsp.readFile(resolve('plugin.json'), 'utf8'));
  const filename = `${pluginJson.name}-${pluginJson.version}-${shortVersion(seeqVersion)}.plugin`;
  const archive = archiver('zip');
  return { archive, filename, pluginJson };
}

async function writePluginManifestToDist(pluginJson) {
  await fsp.writeFile(resolve('dist', 'plugin.json'), JSON.stringify(pluginJson, null, 2), 'utf8');
}

async function generateZip() {
  const { archive, filename, pluginJson } = await createArchive();
  await writePluginManifestToDist(pluginJson);
  archive.directory(resolve('dist'), false);
  const zipPath = resolve(filename);
  await rimraf(zipPath);
  const output = fs.createWriteStream(zipPath);

  await new Promise((resolvePromise, rejectPromise) => {
    archive.on('warning', rejectPromise);
    archive.on('error', rejectPromise);
    output.on('finish', resolvePromise);
    archive.pipe(output);
    archive.finalize();
  });

  return zipPath;
}

async function validateDistHtml() {
  const indexHtmlPath = resolve('dist', 'index.html');
  let indexHtml;
  try {
    indexHtml = await fsp.readFile(indexHtmlPath, 'utf8');
  } catch (error) {
    if (error.code === 'ENOENT') {
      throw new Error(`Build output is missing ${indexHtmlPath}. Run the frontend build first.`);
    }
    throw error;
  }

  if (/["']\/assets\//.test(indexHtml)) {
    throw new Error(
      'dist/index.html contains root-relative /assets/ paths. Configure Vite with base: "./" so packaged plugins load assets correctly.'
    );
  }
}

async function postZip(url, user) {
  const { archive, filename, pluginJson } = await createArchive();
  const form = new FormData();
  const passthrough = new stream.PassThrough();

  const adjustedPluginJson = {
    ...pluginJson,
    identifier: user.isAdmin ? pluginJson.identifier : `${pluginJson.identifier}_${user.id.toLowerCase()}`
  };

  await writePluginManifestToDist(adjustedPluginJson);
  archive.directory(resolve('dist'), false);
  archive.pipe(passthrough);
  archive.finalize();
  form.append('file', passthrough, filename);

  const res = await fetch(`${base(url)}/api/plugins?inDevelopment=${!user.isAdmin}`, {
    method: 'POST',
    headers: {
      'x-sq-auth': user.auth,
      Accept: 'application/vnd.seeq.v1+json',
      ...form.headers
    },
    body: form.stream
  });

  if (!res.ok) {
    const err = new Error(`Request failed /api/plugins ${res.status}`);
    err.data = await res.text();
    throw err;
  }
}

main().catch((error) => {
  log(error.stack);
  if (error.data) {
    log(error.data);
  }
  process.exit(1);
});
