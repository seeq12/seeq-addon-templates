import pathlib

from _dev_tools.utils import (
    filter_element_paths,
    get_element_paths_with_type,
    get_folders_from_args,
    get_module
)


def elements_testing(args):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    for element_path, element_type in target_elements.items():
        print(f'Running test for element: {element_path}')
        get_module(element_path, element_type).test(pathlib.Path(element_path))
