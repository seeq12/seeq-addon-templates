import argparse
import asyncio
import base64
import json
import os
import pathlib
import subprocess
import sys
import venv
from typing import List

from _dev_tools import package
from _dev_tools.add_on_manager_session import AddOnManagerSession
from _dev_tools.utils import (
    _parse_url_username_password,
    get_element_identifier_from_path, _upload_file
)

CURRENT_FILE = pathlib.Path(__file__)

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


def bootstrap(element_path: pathlib.Path, clean: bool) -> None:
    print(element_path)
    _create_virtual_environment(element_path, clean)


def build() -> None:
    print('There is no need to build add-on tools that are based on Jupyter notebooks. '
          'This operation is skipped for this add-on element')


def deploy(username: str, password: str, url: str, element_path: pathlib.Path) -> None:
    pass


def watch(element_path: pathlib.Path, url, username, password) -> subprocess.Popen:

    venv_path, windows_os, path_to_python, path_to_pip, path_to_scripts, wheels_path = get_venv_paths(element_path)

    return subprocess.Popen(f"{path_to_python} {CURRENT_FILE} --action watch --element {element_path}"
                            f" --url {url} --username {username} --password {password}", shell=True)


def test(self) -> None:
    pass


def get_build_dependencies() -> List[str]:
    return []


def get_files_to_package(element_path: pathlib.Path) -> List[str]:
    from _dev_tools.utils import find_files_in_folder_recursively
    files_to_deploy = find_files_in_folder_recursively(
        str(element_path),
        file_extensions=FILE_EXTENSIONS,
        excluded_files=EXCLUDED_FILES,
        excluded_folders=EXCLUDED_FOLDERS,
    )
    return files_to_deploy


def _create_virtual_environment(element_path: pathlib.Path, clean: bool = False):

    venv_path, windows_os, path_to_python, path_to_pip, path_to_scripts, wheels_path = get_venv_paths(element_path)
    if (
            not clean
            and venv_path.exists()
            and venv_path.is_dir()
    ):
        print("Virtual environment already exists.")
        return
    print("Creating virtual environment...")
    venv.EnvBuilder(
        system_site_packages=False, with_pip=True, clear=True, symlinks=not windows_os
    ).create(venv_path)
    subprocess.run(
        f"{path_to_python} -m pip install --upgrade pip", shell=True, check=True
    )

    command = f"{path_to_pip} install "
    if (element_path / 'requirements.dev.txt').exists():
        command += f"-r {element_path / 'requirements.dev.txt'}"
    if (element_path / 'requirements.txt').exists():
        command += f" -r {element_path / 'requirements.txt'}"
    if wheels_path.exists():
        command += f" -f {wheels_path}"

    subprocess.run(
        command,
        shell=True,
        check=True,
    )

    print("Virtual environment created.")


def get_venv_paths(element_path: pathlib.Path):

    venv_path = element_path / ".venv"
    wheels_path = element_path / ".wheels"
    windows_os = os.name == "nt"
    path_to_scripts = venv_path / ("Scripts" if windows_os else "bin")
    path_to_pip = path_to_scripts / "pip"
    path_to_python = path_to_scripts / "python"

    return venv_path, windows_os, path_to_python, path_to_pip, path_to_scripts, wheels_path


# def _deploy_from_environment(url: str, username: str, password: str, element_path: pathlib.Path):
#     requests_session, auth_header, project_id = _get_authenticated_session(element_path, url, username, password)
#     for destination in get_files_to_package(element_path):
#         source = element_path / destination
#         _upload_file(url, requests_session, auth_header, project_id, source, destination)
#
#
# def _get_authenticated_session(element_path, url, username, password):
#     from seeq import sdk, spy
#     spy.login(username=username, password=password, url=url, quiet=True)
#     auth_header = {'sq-auth': spy.client.auth_token}
#     items_api = sdk.ItemsApi(spy.client)
#     element_project_name = get_element_identifier_from_path(element_path)
#     response = items_api.search_items(filters=[f'name=={element_project_name}'], types=['Project'])
#     if len(response.items) == 0:
#         raise Exception(f"Could not find a project with name {element_project_name}")
#     project_id = response.items[0].id
#     requests_session = _create_requests_session()
#     return requests_session, auth_header, project_id
#
#
# def _create_requests_session():
#     import requests
#     from requests.adapters import HTTPAdapter, Retry
#     max_request_retries = 5
#     request_retry_status_list = [502, 503, 504]
#     _http_adapter = HTTPAdapter(
#         max_retries=Retry(total=max_request_retries, backoff_factor=0.5, status_forcelist=request_retry_status_list))
#     request_session = requests.Session()
#     request_session.mount("http://", _http_adapter)
#     request_session.mount("https://", _http_adapter)
#     return request_session
#
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Element scripts. Must be run from the virtual environment.")
#     parser.add_argument('--url', type=str, help='URL to the Seeq server')
#     parser.add_argument('--username', type=str, help='Username for authentication')
#     parser.add_argument('--password', type=str, help='Password for authentication')
#     parser.add_argument('--element', type=str, help='Element path')
#     parser.add_argument('--action', type=str, choices=['deploy', 'watch'], help='Action to perform')
#     args = parser.parse_args()
#
#     # make the add-on package available to the deploy script
#     sys.path.append(os.path.abspath(os.path.join(ELEMENT_PATH, os.path.pardir)))
#     if args.action == 'deploy':
#         if args.url is None or args.username is None or args.password is None:
#             raise Exception("Must provide url, username, and password arguments when deploying")
#         _deploy_from_environment(args.url, args.username, args.password, args.element)
#     elif args.action == 'watch':
#         if args.url is None or args.username is None or args.password is None:
#             raise Exception("Must provide url, username, and password arguments when watching")
#         try:
#             asyncio.run(_watch_from_environment(args.url, args.username, args.password))
#         except KeyboardInterrupt:
#             pass
