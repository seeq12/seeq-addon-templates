import argparse
import glob
import importlib
import os
import pathlib
import subprocess
import sys
import zipfile
from typing import Optional, List, Dict

from _deployment_tools import load_json, save_json, topological_sort, ElementProtocol

PROJECT_PATH = pathlib.Path(__file__).parent.resolve()
WHEELS_PATH = PROJECT_PATH / '.wheels'
ADDON_JSON_FILE = PROJECT_PATH / "addon.json"
BOOTSTRAP_JSON_FILE = PROJECT_PATH / ".bootstrap.json"

ELEMENT_ACTION_FILE = 'element'

IDENTIFIER = "identifier"
VERSION = 'version'
ELEMENTS = 'elements'
ELEMENT_PATH = 'path'
ELEMENT_TYPE = 'type'
ELEMENT_IDENTIFIER = 'identifier'
PREVIEWS = "previews"

DIST_FOLDER = PROJECT_PATH / 'dist'
ADD_ON_EXTENSION = '.addon'
ADD_ON_METADATA_EXTENSION = '.addonmeta'

DEFAULT_ADD_ON_TOOL_ELEMENT_PATH = '_deployment_tools.defaults.addon_tool'
ADD_ON_TOOL_TYPE = "AddOnTool"


def get_files_to_package() -> List[str]:
    add_on_json = get_add_on_json()
    preview_files = add_on_json.get(PREVIEWS, [])
    return ["addon.json"] + preview_files


def create_package_filename(dist_base_filename: str, version: str) -> str:
    return f"{dist_base_filename}-{version}"


def get_add_on_json() -> Optional[dict]:
    return load_json(ADDON_JSON_FILE)


def get_bootstrap_json() -> Optional[dict]:
    return load_json(BOOTSTRAP_JSON_FILE)


def get_element_paths_with_type() -> Dict[str, str]:
    add_on_json = get_add_on_json()
    if add_on_json is None or ELEMENTS not in add_on_json:
        return {}
    element_paths = {element.get(ELEMENT_PATH): element.get(ELEMENT_TYPE) for element in add_on_json.get(ELEMENTS)}
    for element_path in element_paths:
        if not pathlib.Path(element_path).exists():
            raise Exception(f'Element path does not exist: {element_path}')
    print(f'Element paths: {element_paths}')
    return element_paths


def get_element_types() -> List[str]:
    add_on_json = get_add_on_json()
    if add_on_json is None or ELEMENTS not in add_on_json:
        return []
    return [element.get(ELEMENT_TYPE) for element in add_on_json.get(ELEMENTS)]


def filter_element_paths(element_paths_with_type: Optional[Dict[str, str]], subset_folders: Optional[List[str]]):
    if subset_folders is None:
        return element_paths_with_type
    return {element_path: element_type for element_path, element_type in element_paths_with_type.items()
            if element_path in subset_folders}


def get_module(element_path: str, element_type: str) -> ElementProtocol:

    def load_module(path: str):
        if path in sys.modules:
            return sys.modules[path]
        return importlib.import_module(path)
    try:
        module = load_module(f'{element_path}.{ELEMENT_ACTION_FILE}')
        assert isinstance(module, ElementProtocol)
        return module
    except ModuleNotFoundError:
        if element_type == ADD_ON_TOOL_TYPE:
            module = load_module(f"{DEFAULT_ADD_ON_TOOL_ELEMENT_PATH}.{ELEMENT_ACTION_FILE}")
            assert isinstance(module, ElementProtocol)
            return module
        else:
            raise ModuleNotFoundError(
                f'Neither {element_path}.{ELEMENT_ACTION_FILE} nor '
                f'{DEFAULT_ADD_ON_TOOL_ELEMENT_PATH}.{ELEMENT_ACTION_FILE} were found')


def check_dependencies(element_paths_with_type: Dict[str, str]):
    python_version = sys.version_info
    if python_version < (3, 8):
        raise Exception('Python 3.8 or higher is required.')
    print(f'Python version: {python_version.major}.{python_version.minor}.{python_version.micro}')
    for element_path, element_type in element_paths_with_type.items():
        get_module(element_path, element_type).check_dependencies()


def get_folders_from_args(args) -> Optional[List[str]]:
    if args is None or args.dir is None:
        return None
    for folder in args.dir:
        if not (PROJECT_PATH / pathlib.Path(folder)).exists():
            raise Exception(f'Folder does not exist: {folder}')
    return [str(pathlib.Path(folder)) for folder in args.dir]


def bootstrap(args):
    save_json(BOOTSTRAP_JSON_FILE, {'username': args.username, 'password': args.password, 'url': args.url})
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    print(f'Bootstrapping elements: {target_elements}')
    check_dependencies(target_elements)
    for element_path, element_type in target_elements.items():
        print(f'Bootstrapping element: {element_path}')
        get_module(element_path, element_type).bootstrap(pathlib.Path(element_path), args.clean)


def build(args=None):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    build_dependencies = {element_path: get_module(element_path, element_type).get_build_dependencies()
                          for element_path, element_type in target_elements.items()}
    sorted_elements = topological_sort(build_dependencies)
    sorted_elements_with_types = {element_path: target_elements[element_path] for element_path in sorted_elements}
    for element_path, element_type in sorted_elements_with_types.items():
        print(f'Building element: {element_path}')
        get_module(element_path, element_type).build()


def package(args=None):
    print("Packaging")
    if not args.skip_build:
        build()
    file_name = get_add_on_package_name()

    if DIST_FOLDER.exists():
        for file in glob.glob(f"{DIST_FOLDER}/*"):
            os.remove(file)
    else:
        os.makedirs(DIST_FOLDER)

    artifact_file_name = DIST_FOLDER / f"{file_name}{ADD_ON_EXTENSION}"
    metadata_file_name = DIST_FOLDER / f"{file_name}{ADD_ON_METADATA_EXTENSION}"

    with zipfile.ZipFile(
            artifact_file_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as add_on_file:
        for filename in get_files_to_package():
            add_on_file.write(filename, filename)
        for element_path, element_type in get_element_paths_with_type().items():
            for filename in get_module(element_path, element_type).get_files_to_package(element_path):
                full_path = PROJECT_PATH / element_path / filename
                archive_path = pathlib.Path(element_path) / filename
                add_on_file.write(full_path, archive_path)

    with zipfile.ZipFile(
            metadata_file_name, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as metadata_file:
        for filename in get_files_to_package():
            metadata_file.write(filename, filename)

    print("Done packaging")


def deploy(args):
    url, username, password = _parse_url_username_password(args)
    if args.dir is None:
        path_to_python = get_module('data-lab-functions', "XXX").PATH_TO_PYTHON
        command_to_run = (f"{path_to_python} data-lab-functions/deploy.py"
                          f" --username {username} --password {password} --url {url}")
        if args.clean:
            command_to_run += ' --clean'
        if args.replace:
            command_to_run += ' --replace'
        subprocess.run(command_to_run, shell=True, check=True)
    else:
        target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
        for element_path, element_type in target_elements.items():
            print(f'Deploying element: {element_path}')
            get_module(element_path, element_type).deploy(url, username, password)


def get_add_on_package_name() -> str:
    add_on_json = get_add_on_json()
    return f"{create_package_filename(add_on_json[IDENTIFIER], add_on_json[VERSION])}"


def watch(args):
    url, username, password = _parse_url_username_password(args)
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    processes = {}
    for element_path, element_type in target_elements.items():
        print(f'watching element: {element_path}')
        processes[element_path] = get_module(element_path, element_type).watch(url, username, password)
    while True:
        try:
            for process in processes.values():
                process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            pass
        except KeyboardInterrupt:
            print('Stopping watch')
            for process in processes.values():
                process.terminate()
            break


def elements_test(args):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    for element_path, element_type in target_elements.items():
        print(f'testing element: {element_path}')
        get_module(element_path, element_type).test()


def _parse_url_username_password(args):
    bootstrap_json = None
    if args.username is None or args.password is None or args.url is None:
        bootstrap_json = get_bootstrap_json()
        if bootstrap_json is None:
            raise Exception('Please run the bootstrap command.')
    url = args.url if args.url else bootstrap_json.get('url')
    username = args.username if args.username else bootstrap_json.get('username')
    password = args.password if args.password else bootstrap_json.get('password')
    return url, username, password


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ao.py', description='Add-on Manager')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_bootstrap = subparsers.add_parser('bootstrap', help='Bootstrap your add-on development environment')
    parser_bootstrap.add_argument('--username', type=str, required=False)
    parser_bootstrap.add_argument('--password', type=str, required=False)
    parser_bootstrap.add_argument('--url', type=str, default='http://localhost:34216')
    parser_bootstrap.add_argument('--clean', action='store_true', default=False, help='Clean bootstrap')
    parser_bootstrap.add_argument('--dir', type=str, nargs='*', default=None,
                                  help='Execute the command for the subset of the element directories specified.')
    parser_bootstrap.set_defaults(func=bootstrap)

    parser_build = subparsers.add_parser('build', help='Build your add-on')
    parser_build.add_argument('--dir', type=str, nargs='*', default=None,
                              help='Execute the command for the subset of the element directories specified.')
    parser_build.set_defaults(func=build)

    parser_deploy = subparsers.add_parser('deploy', help='Deploy your add-on')
    parser_deploy.add_argument('--username', type=str)
    parser_deploy.add_argument('--password', type=str)
    parser_deploy.add_argument('--url', type=str)
    parser_deploy.add_argument('--clean', action='store_true', default=False, help='Uninstall')
    parser_deploy.add_argument('--replace', action='store_true', default=False, help='Replace elements')
    parser_deploy.add_argument('--dir', type=str, nargs='*', default=None,
                               help='Execute the command for the subset of the element directories specified.')
    parser_deploy.set_defaults(func=deploy)

    parser_package = subparsers.add_parser('package', help='Package your add-on')
    parser_package.add_argument('--skip-build', action='store_true', default=False, help='Skip build step')
    parser_package.set_defaults(func=package)

    parser_watch = subparsers.add_parser('watch', help='Build, watch, and live-update all or individual elements '
                                                       'whenever code in the elements changes')
    parser_watch.add_argument('--username', type=str)
    parser_watch.add_argument('--password', type=str)
    parser_watch.add_argument('--url', type=str)
    parser_watch.add_argument('--dir', type=str, nargs='*', default=None,
                              help='Execute the command for the subset of the element directories specified.')
    parser_watch.set_defaults(func=watch)

    parser_test = subparsers.add_parser('test', help='Run the tests for all or individual elements')
    parser_test.add_argument('--dir', type=str, nargs='*', default=None,
                             help='Execute the command for the subset of the element directories specified.')
    parser_test.set_defaults(func=elements_test)

    options, unknown = parser.parse_known_args()
    options.func(options)
