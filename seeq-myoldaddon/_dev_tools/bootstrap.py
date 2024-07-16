import sys
import pathlib
from typing import Dict

from .utils import (
    filter_element_paths,
    get_element_paths_with_type,
    get_folders_from_args,
    get_module
)


def bootstrap(args):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    print(f'Bootstrapping elements: {target_elements}')
    check_dependencies(target_elements)
    for element_path, element_type in target_elements.items():
        print(f'Bootstrapping element: {element_path}')
        get_module(element_path, element_type).bootstrap(pathlib.Path(element_path), args.clean)


def check_dependencies(element_paths_with_type: Dict[str, str]):
    python_version = sys.version_info
    if python_version < (3, 8):
        raise Exception('Python 3.8 or higher is required.')
    print(f'Python version: {python_version.major}.{python_version.minor}.{python_version.micro}')
    for element_path, element_type in element_paths_with_type.items():
        get_module(element_path, element_type).check_dependencies()
