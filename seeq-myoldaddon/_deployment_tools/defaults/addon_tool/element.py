import os
import pathlib
import subprocess
import venv
from typing import List


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
    print("I'm bootstrapping!")


def build() -> None:
    print("Generally, there is no need to build add-on tools that are based on Jupyter notebooks")


def deploy(self, username: str, password: str, url: str) -> None:
    pass


def watch(self, url: str, username: str, password: str) -> subprocess.Popen:
    pass


def test(self) -> None:
    pass


def get_build_dependencies() -> List[str]:
    return []


def get_files_to_package(element_path: pathlib.Path) -> List[str]:
    from _deployment_tools import find_files_in_folder_recursively

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
