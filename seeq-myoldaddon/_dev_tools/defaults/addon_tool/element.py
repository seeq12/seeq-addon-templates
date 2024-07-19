import base64
import json
import os
import pathlib
import subprocess
import venv
from typing import List

from _dev_tools import package
from _dev_tools.add_on_manager_session import AddOnManagerSession
from _dev_tools.utils import (
    IDENTIFIER,
    ADD_ON_EXTENSION,
    DIST_FOLDER,
    CONFIGURATION_SCHEMA,
    get_add_on_json,
    get_add_on_package_name,
    generate_schema_default_dict, ELEMENT_IDENTIFIER, ELEMENT_PATH, ELEMENTS
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


def bootstrap(element_path: pathlib.Path, clean: bool) -> None:
    print(element_path)
    _create_virtual_environment(element_path, clean)


def build() -> None:
    print('There is no need to build add-on tools that are based on Jupyter notebooks. '
          'This operation is skipped for this add-on element')


def deploy(args) -> None:
    add_on_identifier = get_add_on_identifier()
    session = AddOnManagerSession(args.url, args.username, args.password)

    package(args)

    # if args.clean:
    #     uninstall(args)

    # upload the add-on
    print("Uploading add-on")
    filename = f"{get_add_on_package_name()}{ADD_ON_EXTENSION}"
    print(DIST_FOLDER / f"{filename}")
    with open(DIST_FOLDER / f"{filename}", "rb") as f:
        # file must be base64 encoded
        encoded_file = base64.b64encode(f.read())
        upload_response = session.upload_add_on(filename, encoded_file)
    upload_response.raise_for_status()
    print("Add-on uploaded")
    upload_response_body = upload_response.json()
    print(f"Add-on status is: {upload_response_body['add_on_status']}")

    print("Fetching configuration")
    configuration = get_configuration()
    print("Installing Add-on")
    install_response = session.install_add_on(
        add_on_identifier, upload_response_body["binary_filename"], configuration
    )
    print(install_response.json())
    if not install_response.ok:
        error = install_response.json()["error"]
        error_message = error["message"]
        raise Exception(f"Error installing Add-on: {error_message}")
    install_response.raise_for_status()
    print("Deployment to Add On Manager Complete")


def watch(self, url: str, username: str, password: str) -> subprocess.Popen:
    pass


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


def get_add_on_identifier() -> str:
    add_on_json = get_add_on_json()
    return add_on_json[IDENTIFIER]


def get_configuration():
    """
    Fetch the configuration of the add-on, used when deploying the add-on to add-on-manager.
    If a configuration.json file is present in an element, it will use that instead of the default configuration.
    """
    addon_json = get_add_on_json()
    config = {}
    for element in addon_json[ELEMENTS]:
        # check if there's a configuration.json file in each element. If yes, use that instead of default
        configuration_file_path = (
                pathlib.Path(element[ELEMENT_PATH]) / "configuration.json"
        )
        if configuration_file_path.exists():
            print(f"Using configuration.json for element {element[ELEMENT_IDENTIFIER]}")
            with open(configuration_file_path, "r") as f:
                config[element[ELEMENT_IDENTIFIER]] = json.load(f)
        elif "configuration_schema" in element:
            print(
                f"Using default configuration for element {element[ELEMENT_IDENTIFIER]}"
            )
            default_config = generate_schema_default_dict(element[CONFIGURATION_SCHEMA])
            config[element[ELEMENT_IDENTIFIER]] = default_config
        else:
            print(
                f"No configuration schema found for element {element[ELEMENT_IDENTIFIER]}"
            )
            pass
    return config
