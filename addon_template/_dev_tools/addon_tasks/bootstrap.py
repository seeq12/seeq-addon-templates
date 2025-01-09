import sys
import pathlib
from typing import Dict

from _dev_tools.addon_tasks.utils import (
    filter_element_paths,
    get_element_paths_with_type,
    get_folders_from_args,
    get_module,
    parse_url_username_password,
    save_json,
    check_python_version,
    CREDENTIALS_JSON_FILE,
)

from _dev_tools.utils import check_python_version, MIN_PYTHON_VERSION


def bootstrap(args):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    check_dependencies(target_elements)
    url, username, password = parse_url_username_password(args)
    save_json(CREDENTIALS_JSON_FILE, {'url': url, 'username': username, 'password': password})
    for element_path, element_type in target_elements.items():
        print(f'Bootstrapping element: {element_path}')
        single_element = True if args.dir else False
        global_python_env = pathlib.Path(args.global_python_env) if args.global_python_env else None
        (get_module(element_path, element_type).
         bootstrap(pathlib.Path(element_path), url, username, password, args.clean, global_python_env, single_element))


def check_dependencies(element_paths_with_type: Dict[str, str]):
    check_python_version(*MIN_PYTHON_VERSION)
    for element_path, element_type in element_paths_with_type.items():
        get_module(element_path, element_type).check_dependencies()
