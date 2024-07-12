import os
import pathlib
import subprocess
import venv
from typing import List

CURRENT_FILE = pathlib.Path(__file__)
ELEMENT_PATH = CURRENT_FILE.parent.resolve()
VIRTUAL_ENVIRONMENT_PATH = ELEMENT_PATH / ".venv"
WHEELS_PATH = ELEMENT_PATH / ".wheels"


WINDOWS_OS = os.name == "nt"
PATH_TO_SCRIPTS = VIRTUAL_ENVIRONMENT_PATH / ("Scripts" if WINDOWS_OS else "bin")
PATH_TO_PIP = PATH_TO_SCRIPTS / "pip"
PATH_TO_PYTHON = PATH_TO_SCRIPTS / "python"


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


def bootstrap(username: str, password: str, url: str, clean: bool) -> None:
    _create_virtual_environment(clean)


def build() -> None:
    pass


def get_build_dependencies() -> List[str]:
    return []


def get_files_to_package() -> List[str]:
    from _deployment_tools import find_files_in_folder_recursively

    files_to_deploy = find_files_in_folder_recursively(
        str(ELEMENT_PATH),
        file_extensions=FILE_EXTENSIONS,
        excluded_files=EXCLUDED_FILES,
        excluded_folders=EXCLUDED_FOLDERS,
    )
    return files_to_deploy


def _create_virtual_environment(clean: bool = False):
    if (
            not clean
            and VIRTUAL_ENVIRONMENT_PATH.exists()
            and VIRTUAL_ENVIRONMENT_PATH.is_dir()
    ):
        print("Virtual environment already exists.")
        return
    print("Creating virtual environment...")
    venv.EnvBuilder(
        system_site_packages=False, with_pip=True, clear=True, symlinks=not WINDOWS_OS
    ).create(VIRTUAL_ENVIRONMENT_PATH)
    subprocess.run(
        f"{PATH_TO_PYTHON} -m pip install --upgrade pip", shell=True, check=True
    )
    subprocess.run(
        # TODO: WHY DO WE NEED TO INSTALL THE DEV REQUIREMENTS?
        f"{PATH_TO_PIP} install -r {ELEMENT_PATH / 'requirements.dev.txt'}"
        f" -r {ELEMENT_PATH / 'requirements.txt'}"
        f" -f {WHEELS_PATH}",
        shell=True,
        check=True,
    )

    print("Virtual environment created.")
