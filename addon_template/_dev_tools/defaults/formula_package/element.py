import glob
import os
import pathlib
import subprocess
from typing import List

from _dev_tools.addon_tasks.utils import (
    CREDENTIALS_JSON_FILE,
    save_json,
    load_json,
)

FILE_EXTENSIONS = {".json"}
EXCLUDED_FOLDERS = set()
EXCLUDED_FILES = {"element.py"}


def check_dependencies() -> None:
    pass


def bootstrap(
        element_path: pathlib.Path,
        url: str,
        username: str,
        password: str,
        clean: bool,
        global_python_env: pathlib.Path,
        single_element: bool
) -> None:
    pass


def get_build_dependencies() -> List[str]:
    return []


def build(element_path: pathlib.Path) -> None:
    pass


def deploy(element_path: pathlib.Path, url: str, username: str, password: str) -> None:
    raise NotImplementedError(f"This method is not implemented for the Formula Package element. Try deploying the "
                              f"entire Add-on package instead.")


def get_files_to_package(element_path: pathlib.Path) -> List[str]:
    from _dev_tools.addon_tasks.utils import find_files_in_folder_recursively

    files_to_deploy = find_files_in_folder_recursively(
        str(element_path),
        file_extensions=FILE_EXTENSIONS,
        excluded_files=EXCLUDED_FILES,
        excluded_folders=EXCLUDED_FOLDERS,
    )
    return files_to_deploy


def watch(element_path: pathlib.Path, url: str, username: str, password: str) -> subprocess.Popen:
    raise NotImplementedError(f"This method is not implemented for the Formula Package element. Try watching the "
                              f"entire Add-on package instead.")


def test(element_path: pathlib.Path) -> None:
    pass


if __name__ == "__main__":
    pass
