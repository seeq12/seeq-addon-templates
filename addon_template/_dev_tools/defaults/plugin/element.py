import glob
import json
import os
import pathlib
import subprocess
from typing import List

from _dev_tools.addon_tasks.utils import (
    CREDENTIALS_JSON_FILE,
    save_json,
    load_json,
)


def _use_pnpm(element_path: pathlib.Path) -> bool:
    if (element_path / "pnpm-lock.yaml").exists():
        return True
    package_json = element_path / "package.json"
    if package_json.exists():
        with open(package_json, "r", encoding="utf-8") as handle:
            package_data = json.load(handle)
        package_manager = package_data.get("packageManager", "")
        if isinstance(package_manager, str) and package_manager.startswith("pnpm@"):
            return True
    return False


def _package_manager(element_path: pathlib.Path) -> str:
    return "pnpm" if _use_pnpm(element_path) else "npm"


def _run(element_path: pathlib.Path, command: str) -> None:
    subprocess.run(command, cwd=element_path, shell=True, check=True)


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
    pnpm_result = subprocess.run('pnpm -v', capture_output=True, shell=True, text=True)
    if pnpm_result.returncode == 0:
        print(f'PNPM version: {pnpm_result.stdout.strip()}')


def bootstrap(
        element_path: pathlib.Path,
        url: str,
        username: str,
        password: str,
        clean: bool,
        global_python_env: pathlib.Path,
        single_element: bool
) -> None:
    if url is None or username is None or password is None:
        raise Exception("Please provide --user --password and --url arguments.")
    if _use_pnpm(element_path):
        _run(element_path, 'pnpm install --no-frozen-lockfile')
        _run(element_path, 'pnpm run bootstrap quiet')
    else:
        _run(element_path, 'npm ci')
        _run(element_path, 'npm run bootstrap quiet')


def get_build_dependencies() -> List[str]:
    return []


def build(element_path: pathlib.Path) -> None:
    _run(element_path, f'{_package_manager(element_path)} run build')


def deploy(element_path: pathlib.Path, url: str, username: str, password: str) -> None:
    # temporarily save the username, password, and url to the bootstrap file so that the deploy script can use them
    credentials_json = load_json(CREDENTIALS_JSON_FILE)
    save_json(CREDENTIALS_JSON_FILE, {'username': username, 'password': password, 'url': url})
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
    return subprocess.Popen(f'{_package_manager(element_path)} run watch', cwd=element_path, shell=True)


def test(element_path: pathlib.Path, markers: str | None = None) -> None:
    _run(element_path, f'{_package_manager(element_path)} run test')


if __name__ == "__main__":
    pass
