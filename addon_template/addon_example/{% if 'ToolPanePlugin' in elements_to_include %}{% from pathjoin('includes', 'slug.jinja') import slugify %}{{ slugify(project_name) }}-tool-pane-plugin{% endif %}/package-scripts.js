'use strict';

import url from 'url';
import { promisify } from 'util';
import path from 'path';

import fs from 'node:fs';
import fsp from 'node:fs/promises';
import stream from 'stream';
import { pipeline } from 'stream';
import process from 'process';

import { rimraf } from 'rimraf';
import { mkdirp } from 'mkdirp';
import archiver from 'archiver';
import FormData from 'formdata-node';
import chalk from 'chalk';
import inquirer from 'inquirer';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const streamPipeline = promisify(pipeline);
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

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
  let retries = 0;

  log(chalk.bold('Please specify the url of the Seeq Server to use for development.') + ' The type');
  log('definitions of the SDK will be fetched from this server and the plugin will');
  log('be uploaded automatically with "npm run watch" for quick iteration.');
  log('');

  async function promptUrl() {
    let url;
    if (existing.url) {
      url = existing.url;
    } else {
      const response = await inquirer.prompt([{
        type: 'input',
        name: 'url',
        default: existing.url,
      }]);
      url = response.url;
    }

    try {
      log('');
      log(chalk.dim('Checking Seeq Server url...'));
      const { version } = await getServerStatus(url);
      log(chalk.green('  Seeq Server running ' + version));
      log('');
      return { url, version };
    } catch (e) {
      logError(e);
      return promptUrl();
    }
  }

  const { url, version } = await promptUrl();

  if (existing.url !== url) {
    await writeBootstrap({ ...existing, url });
  }

  log(chalk.bold('Specify the Access Key (or username) and Password for the Seeq Server.') + ' These');
  log('credentials will be used to publish the plugin to the Seeq Server for');
  log('fast iteration during development.');
  log('');

  log('To generate an access key:');
  log('');
  log(' 1. Click on your name in the upper right corner');
  log(' 2. Click "Access Keys" from the dropdown');
  log(' 3. Name the access key (i.e., Plugin Development)');
  log('');

  async function promptAccessKey(retries) {
    let accessKey, password;
    if (retries === 0 && existing.accessKey && existing.password) {
      accessKey = existing.accessKey;
      password = existing.password;
    } else {
      const response = await inquirer.prompt([{
        type: 'input',
        name: 'accessKey',
        default: existing.accessKey
      }, {
        type: 'password',
        name: 'password',
        default: existing.password
      }]);
      accessKey = response.accessKey;
      password = response.password;
    }

    log('');
    if (!!accessKey && !!password) {
      try {
        log(chalk.dim('Verifying access key...'));
        const user = await login(url, accessKey, password);
        log(chalk.green('  Access key is valid'));
        log('');
        return { accessKey, password, user };
      } catch (e) {
        logError(e);
        retries++;
        if (retries >= 3) {
            throw new Error('Too many retries, please check your credentials and try again.');
        }
        return promptAccessKey(retries);
      }
    }
  }

  const { accessKey, password, user } = await promptAccessKey(retries);

  if (existing.accessKey !== accessKey || existing.password !== password) {
    await writeBootstrap({ ...existing, accessKey, password });
  }

  // test plugin api enabled
  const { configurationOptions } = await getServerStatus(url);
  const pluginsEnabledOption = configurationOptions
    .find(option => option.path === 'Features/Plugins/Enabled');
  if (pluginsEnabledOption && !pluginsEnabledOption.value) {
    log(chalk.bold.red('Experimental plugins support is not enabled.') + ' This');
    log('support is required to develop a plugin. Support is controlled by');
    log('the `Features/Plugins/Enabled` configuration option.');
    log('');
    let enable = false;
    if (!!accessKey && !!password && user.isAdmin) {
      // Since we have an admin user, we can just enable support if the user wants
      ({ enable } = await inquirer
        .prompt([{
          type: 'confirm',
          name: 'enable',
          message: 'Enable experimental plugin features?',
          default: true
        }]));
      log('');
    }

    if (enable) {
      log(chalk.dim('Enabling plugin features...'));
      const { auth } = await login(url, accessKey, password);
      await enablePluginsFeature(url, auth);
      log(chalk.green(`  Enabled plugin features`));
      log('');
    } else if (!user.isAdmin) {
        log('User is not an admin. Will be able to deploy only if experimental plugin support is already enabled.');

    } else {
      throw new Error('Experimental plugin support is not enabled. Please configure `Features/Plugins/Enabled`');
    }
  }

  // download sdk
  log(chalk.dim('Downloading SDK...'));
  await downloadSdk(url);
  log(chalk.green(`  Downloaded ${shortVersion(version)} SDK`));
  log('');

  log(chalk.green.bold('Bootstrap Complete:'));
  log(` - Use ${chalk.bold('"npm run watch"')} to update the plugin on the server as you make changes`);
  log(` - Use ${chalk.bold('"npm run tsc"')} to run the typechecker`);
  log(` - Use ${chalk.bold('"npm run lint"')} to run the code style linter`);
  log(` - Use ${chalk.bold('"npm run build"')} to build a plugin file that can be uploaded to another Seeq Server`);
  log('');
}

async function commandDeploy() {
  const { url, accessKey, password } = await readBootstrap();

  if (!url) {
    throw new Error('URL for Seeq Server not configured, use "npm run bootstrap" to configure');
  }

  if (!accessKey || !password) {
    throw new Error('Access key for Seeq Server not configured, use "npm run bootstrap" to configure');
  }

  const user = await login(url, accessKey, password);

  log(chalk.dim('Uploading plugin...'));
  await postZip(url, user);
  log(chalk.green('  Uploaded plugin to ' + url));
}

async function commandPackage() {
  log(chalk.dim('Creating plugin...'));
  const path = await generateZip();
  log(chalk.green('  Created ' + path));
}

async function writeBootstrap({ url, accessKey, password }) {
  await fsp.writeFile(resolve('../.credentials.json'), JSON.stringify({ url, accessKey, password }, null, 2), 'utf8');
}

async function readBootstrap() {
  let contents;
  try {
    contents = JSON.parse(await fsp.readFile(resolve('../.credentials.json'), 'utf8'));
  } catch (ex) {
    if (ex.code === 'ENOENT') {
      contents = {};
    } else {
      throw ex;
    }
  }
  const { url, username, password } = contents;
  return {
    url: url || 'http://localhost:34216',
    accessKey: username || null,
    password: password || null
  };
}

function base(url) {
  const { origin } = new URL(url);
  return origin;
}

async function getServerStatus(url) {
  const res = await fetch(`${base(url)}/api/system/server-status`, {
    headers: {
      'Accept': 'application/vnd.seeq.v1+json'
    }
  });

  if (!res.ok) {
    const err = new Error(`Request failed /api/system/server-status ${res.status}`);
    err.data = await res.text();
    err.status = res.status;
    throw err;
  }

  return await res.json();
}

async function login(url, username, password) {
  const res = await fetch(`${base(url)}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/vnd.seeq.v1+json',
      'Accept': 'application/vnd.seeq.v1+json'
    },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    const err = new Error(`Request failed /api/auth/login ${res.status}`);
    err.data = await res.text();
    err.status = res.status;
    throw err;
  }

  const body = await res.json();

  return {
    auth: res.headers.get('x-sq-auth'),
    name: body.name,
    email: body.email,
    isAdmin: body.isAdmin,
    id: body.id,
  };
}

async function enablePluginsFeature(url, auth) {
  const res = await fetch(`${base(url)}/api/system/configuration/options`, {
    method: 'POST',
    headers: {
      'x-sq-auth': auth,
      'Content-Type': 'application/vnd.seeq.v1+json',
      'Accept': 'application/vnd.seeq.v1+json'
    },
    body: JSON.stringify({
      configurationOptions: [
        {
          note: '',
          path: 'Features/Plugins/Enabled',
          value: true
        }
      ]
    })
  });

  if (!res.ok) {
    const err = new Error(`Request failed /api/system/configuration/options ${res.status}`);
    err.data = await res.text();
    err.status = res.status;
    throw err;
  }
}

async function downloadFile(url, filename, destination) {
  const res = await fetch(`${base(url)}/api/plugins/sdk/${filename}`);

  if (!res.ok) {
    const err = new Error(`Request failed /api/plugins/sdk/${filename} ${res.status}`);
    err.data = await res.text();
    err.status = res.status;
    throw err;
  }

    return await streamPipeline(res.body, fs.createWriteStream(path.resolve(destination, filename)));
}

async function downloadSdk(url) {
  const { version } = await getServerStatus(url);
  await rimraf(resolve('sdk'));
  await mkdirp(resolve('sdk'));
  await fsp.writeFile(resolve('sdk', 'version.txt'), version, 'utf8');
  const files = ['seeq.d.ts', 'seeq.js', 'seeq.css'];
  for (const file of files) {
    await downloadFile(url, file, resolve('sdk'));
  }
  await fsp.writeFile(resolve('sdk', 'README.md'), [
    '# SDK Resources',
    '',
    `Pulled from ${url}; version ${version}`,
    '',
    ...files.map(file => ` - /api/plugins/sdk/${file}`),
    '',
    'These files were retrieved from a Seeq Server for TypeScript typechecking and',
    'for reference. Plugins should not bundle these resources, but should instead',
    'reference them at runtime.',
    '',
    'The plugin may work on different versions of Seeq, but only one versions types',
    'will be checked.',
    '',
  ].join('\n'), 'utf8');
}

function shortVersion(version) {
  return version.replace(/^(R\d+)\..*$/, '$1');
}

async function zip(skipPluginJson = false) {
  const seeqVersion = (await fsp.readFile(resolve('sdk', 'version.txt'))).toString();
  const { name, version } = JSON.parse(await fsp.readFile(resolve('src', 'plugin.json')));
  const filename = `${name}-${version}-${shortVersion(seeqVersion)}.plugin`;

  function pluginJsonSkipper(entryData) {
    if (skipPluginJson && entryData.name === 'plugin.json') {
      return false; // Returning false will skip the file
    }
    return entryData;
  }

  return {
    filename,
    archive: archiver('zip')
      .directory(resolve('dist'), false, (entryData) => pluginJsonSkipper(entryData))
  };
}

async function generateZip() {
  const { filename, archive } = await zip();
  const zipPath = resolve(filename);
  await rimraf(zipPath);
  const output = fs.createWriteStream(zipPath);
  await new Promise((resolve, reject) => {
    try {
      archive.on('warning', (err) => {
        log(`WARNING: ${err}`);
      });

      archive.on('error', (err) => {
        reject(err);
      });

      output.on('finish', () => {
        resolve();
      });

      archive.pipe(output);

      archive.finalize();
    } catch (e) {
      reject(e);
    }
  });
  return zipPath;
}

async function postZip(url, user) {
  const { auth, id, isAdmin } = user;
  const inDevelopment = !isAdmin;
  const skipPluginJson = inDevelopment;
  const { filename, archive } = await zip(skipPluginJson);
  const form = new FormData();
  const IdentityStream = class extends stream.Transform {
    // FormData rejects archive because it isn't a stream, so use this dummy stream
    _transform(chunk, encoding, done) {
      this.push(chunk);
      done();
    }
  };

  if (inDevelopment) {
    // When in development, we need to append the identifier in the plugin.json with the user id 
    const pluginJson = JSON.parse(await fsp.readFile(resolve('src', 'plugin.json'), 'utf8'));
    pluginJson.identifier = `${pluginJson.identifier}_${id.toLowerCase()}`;
    const memoryStream = new stream.Readable({
      read() {
          this.push(JSON.stringify(pluginJson, null, 2));
          this.push(null);
      }
    });
    archive.append(memoryStream, { name: 'plugin.json' });
  }

  const innerStream = new IdentityStream();
  archive.on('warning', (err) => {
    log(`WARNING: ${err}`);
  });
  archive.pipe(innerStream);
  await archive.finalize();

  form.append('file', innerStream, filename);

  const res = await fetch(`${base(url)}/api/plugins?inDevelopment=${inDevelopment}`, {
    method: 'POST',
    headers: {
      'x-sq-auth': auth,
      'Accept': 'application/vnd.seeq.v1+json',
      ...form.headers
    },
    body: form.stream
  });

  if (!res.ok) {
    const err = new Error(`Request failed /api/plugins ${res.status}`);
    err.data = await res.text();
    err.status = res.status;
    throw err;
  }
}

function logError(e) {
  log(e.stack);
  if (e.data) {
    log(e.data);
  }
}

main()
  .catch((e) => {
    logError(e);
    process.exit(1);
  });
