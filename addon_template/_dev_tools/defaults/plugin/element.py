import glob
import os
import pathlib
import subprocess
from typing import List

from _dev_tools.ao_tasks.utils import (
    CREDENTIALS_JSON_FILE,
    save_json,
    load_json,
)


def check_dependencies() -> None:
    node_result = subprocess.run('node -v', capture_output=True, shell=True, text=True)
    if node_result.returncode != 0:
        raise Exception('Node is not installed. Please install node.')
    node_version = node_result.stdout.strip()
    print(f'Node version: {node_version}')
    npm_result = subprocess.run('npm -v', capture_output=True, shell=True, text=True)
    if npm_result.stderr is not None and len(npm_result.stderr) > 0:
        raise Exception('NPM package is not installed. Please install the npm package.')
    npm_version = npm_result.stdout.strip()
    print(f'NPM version: {npm_version}')


def bootstrap(element_path: pathlib.Path, url: str, username: str, password: str, clean: bool, global_python_env: pathlib.Path) -> None:
    if global_python_env:
        # Global python environment is not supported for this element.
        return
    if url is None or username is None or password is None:
        raise Exception("Please provide --user --password and -url arguments.")
    subprocess.run('npm ci', cwd=element_path, shell=True, check=True)
    subprocess.run('npm run bootstrap quiet', cwd=element_path, shell=True, check=True)


def get_build_dependencies() -> List[str]:
    return []


def build(element_path: pathlib.Path) -> None:
    subprocess.run('npm run build', cwd=element_path, shell=True, check=True)


def deploy(element_path: pathlib.Path, url: str, username: str, password: str) -> None:
    # temporarily save the username, password, and url to the bootstrap file so that the deploy script can use them
    credentials_json = load_json(CREDENTIALS_JSON_FILE)
    save_json(CREDENTIALS_JSON_FILE, {'accessKey': username, 'password': password, 'url': url})
    try:
        subprocess.run('node ./package-scripts.js deploy', cwd=element_path, shell=True, check=True)
    finally:
        if credentials_json is not None:
            save_json(CREDENTIALS_JSON_FILE, credentials_json)


def get_files_to_package(element_path: pathlib.Path) -> List[str]:
    plugin_files = glob.glob(str(element_path) + "/*.plugin")
    if len(plugin_files) != 1:
        raise Exception(f"Expected to find 1 plugin file, found {len(plugin_files)}")
    return [os.path.relpath(plugin_files[0], element_path)]


def watch(element_path: pathlib.Path, url: str, username: str, password: str) -> subprocess.Popen:
    return subprocess.Popen('npm run watch', cwd=element_path, shell=True)


def test(element_path: pathlib.Path) -> None:
    subprocess.run('npm run test', cwd=element_path, shell=True, check=True)


if __name__ == "__main__":
    pass
