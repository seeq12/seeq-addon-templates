import argparse
import asyncio
import os
import pathlib
import subprocess
import sys
from typing import List

CURRENT_FILE = pathlib.Path(__file__)

# make the Add-on package available to the `deploy` script
sys.path.append(os.path.abspath(CURRENT_FILE.parent.parent.parent.parent.resolve()))

from _dev_tools.addon_tasks.utils import (
    _upload_file,
    _get_authenticated_session,
    _watch_from_environment
)

from _dev_tools.utils import (
    get_venv_paths
)

FILE_EXTENSIONS = {".py", ".txt", ".ipynb", ".json", ".vue"}
EXCLUDED_FILES = {"element.py", "requirements.dev.txt"}
EXCLUDED_FOLDERS = {
    ".venv",
    ".wheels",
    "build",
    "dist",
    "seeq_add_on_manager.egg-info",
    "tests",
}


def check_dependencies() -> None:
    pass


def bootstrap(element_path: pathlib.Path, url: str, username: str, password: str, clean: bool, global_python_env: pathlib.Path) -> None:
    pass  # Environment is already bootstrapped at top level


def build(element_path: pathlib.Path) -> None:
    print('There is no need to build Add-on Tools or Data Lab Functions elements. '
          'This operation is skipped for this Add-on element')


def deploy(element_path: pathlib.Path, url: str, username: str, password: str) -> None:
    # Pass empty path to get_venv_paths to get the paths for the top-level virtual environment
    path_to_python = get_venv_paths(pathlib.Path(''), path_requested="path_to_python")
    subprocess.run(f"{path_to_python} {CURRENT_FILE} --action deploy --element {element_path}"
                   f" --url {url} --username {username} --password {password}",  shell=True, check=True)


def watch(element_path: pathlib.Path, url, username, password) -> subprocess.Popen:
    deploy(element_path, url, username, password)
    # Pass empty path to get_venv_paths to get the paths for the top-level virtual environment
    path_to_python = get_venv_paths(pathlib.Path(''), path_requested="path_to_python")

    return subprocess.Popen(f"{path_to_python} {CURRENT_FILE} --action watch --element {element_path}"
                            f" --url {url} --username {username} --password {password}", shell=True)


def test(element_path: pathlib.Path) -> None:
    path_to_test = get_venv_paths(element_path, path_requested="test")
    process = subprocess.run(f"{path_to_test.resolve()} -m unit", cwd=element_path.resolve(),
                             check=False, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    print("TEST PROCESS\n", process.stdout.decode())
    if process.stderr:
        print("TEST ERRORS\n", process.stderr.decode())


def get_build_dependencies() -> List[str]:
    return []


def get_files_to_package(element_path: pathlib.Path) -> List[str]:
    from _dev_tools.addon_tasks.utils import find_files_in_folder_recursively
    files_to_deploy = find_files_in_folder_recursively(
        str(element_path),
        file_extensions=FILE_EXTENSIONS,
        excluded_files=EXCLUDED_FILES,
        excluded_folders=EXCLUDED_FOLDERS,
    )
    return files_to_deploy


def _deploy_from_environment(url: str, username: str, password: str, element_path: pathlib.Path):
    requests_session, auth_header, project_id = _get_authenticated_session(element_path, url, username, password)
    for destination in get_files_to_package(element_path):
        source = element_path / destination
        _upload_file(url, requests_session, auth_header, project_id, source, destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Element scripts. Must be run from the virtual environment.")
    parser.add_argument('--url', type=str, help='URL to the Seeq server')
    parser.add_argument('--username', type=str, help='Username for authentication')
    parser.add_argument('--password', type=str, help='Password for authentication')
    parser.add_argument('--element', type=str, help='Element path')
    parser.add_argument('--action', type=str, choices=['deploy', 'watch'], help='Action to perform')
    args = parser.parse_args()

    if args.action == 'deploy':
        if args.url is None or args.username is None or args.password is None or args.element is None:
            raise Exception("Must provide url, username, password, and element_path arguments when deploying")
        _deploy_from_environment(args.url, args.username, args.password, pathlib.Path(args.element))
    elif args.action == 'watch':
        if args.url is None or args.username is None or args.password is None:
            raise Exception("Must provide url, username, and password arguments when watching")
        try:
            pass
            asyncio.run(_watch_from_environment(pathlib.Path(args.element), args.url, args.username, args.password,
                                                FILE_EXTENSIONS, EXCLUDED_FILES, EXCLUDED_FOLDERS))
        except KeyboardInterrupt:
            pass
