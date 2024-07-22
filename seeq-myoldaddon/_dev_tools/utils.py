import json
import os
import sys
import importlib
import pathlib
import stat
from typing import Optional, Dict, List, Set
from .element_protocol import ElementProtocol


PROJECT_PATH = pathlib.Path(__file__).parent.parent.resolve()
WHEELS_PATH = PROJECT_PATH / '.wheels'
DIST_FOLDER = PROJECT_PATH / 'dist'
ADDON_JSON_FILE = PROJECT_PATH / "addon.json"
ADD_ON_EXTENSION = '.addon'
DEPLOY_JSON_FILE = PROJECT_PATH / ".credentials.json"

ELEMENT_ACTION_FILE = 'element'

IDENTIFIER = "identifier"
VERSION = 'version'
ELEMENTS = 'elements'
ELEMENT_PATH = 'path'
ELEMENT_TYPE = 'type'
ELEMENT_IDENTIFIER = 'identifier'
CONFIGURATION_SCHEMA = "configuration_schema"
PREVIEWS = "previews"

DEFAULT_ADD_ON_TOOL_ELEMENT_PATH = f'{pathlib.Path(__file__).parent.name}.defaults.addon_tool'
ADD_ON_TOOL_TYPE = "AddOnTool"


def load_json(path: pathlib.Path) -> Optional[dict]:
    if not path.exists():
        return None
    with open(path, mode='r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_json(path: pathlib.Path, values: dict) -> None:
    with open(path, mode='w', encoding='utf-8') as json_file:
        json.dump(values, json_file, indent=2, ensure_ascii=False)


def get_add_on_json() -> Optional[dict]:
    return load_json(ADDON_JSON_FILE)


def get_add_on_identifier() -> str:
    add_on_json = get_add_on_json()
    return add_on_json[IDENTIFIER]


def get_add_on_package_name() -> str:
    add_on_json = get_add_on_json()
    return f"{create_package_filename(add_on_json[IDENTIFIER], add_on_json[VERSION])}"


def create_package_filename(dist_base_filename: str, version: str) -> str:
    return f"{dist_base_filename}-{version}"


def filter_element_paths(element_paths_with_type: Optional[Dict[str, str]], subset_folders: Optional[List[str]]):
    if subset_folders is None:
        return element_paths_with_type
    return {element_path: element_type for element_path, element_type in element_paths_with_type.items()
            if element_path in subset_folders}


def get_folders_from_args(args) -> Optional[List[str]]:
    if args is None or args.dir is None:
        return None
    for folder in args.dir:
        if not (PROJECT_PATH / pathlib.Path(folder)).exists():
            raise Exception(f'Folder does not exist: {folder}')
    return [str(pathlib.Path(folder)) for folder in args.dir]


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


def get_files_to_package() -> List[str]:
    add_on_json = get_add_on_json()
    preview_files = add_on_json.get(PREVIEWS, [])
    return ["addon.json"] + preview_files


def topological_sort(graph: Dict[str, List[str]]) -> List[str]:
    """
    Topological sort algorithm.
    :param graph: a dictionary of nodes and their dependencies
    :return: a list of nodes in topological order
    """
    result = []
    visited = set()

    def dfs(graph_node: str):
        if graph_node in visited:
            return
        visited.add(graph_node)
        for dependency in graph.get(graph_node, []):
            dfs(dependency)
        result.append(graph_node)

    for node in graph:
        dfs(node)
    return result


def file_matches_criteria(root: str,
                          file: str,
                          excluded_files: Set[str] = None,
                          excluded_folders: Set[str] = None,
                          file_extensions: Set[str] = None,
                          exclude_dot_files: bool = False,
                          exclude_hidden_files: bool = True):
    if excluded_folders is None:
        excluded_folders = {}
    relative_path = os.path.relpath(file, root)
    if any(relative_path.startswith(excluded_folder) for excluded_folder in excluded_folders):
        return False
    if excluded_files is not None and relative_path in excluded_files:
        return False
    filename = os.path.basename(file)
    if exclude_dot_files and filename.startswith('.'):
        return False
    if file_extensions is not None and pathlib.Path(filename).suffix not in file_extensions:
        return False
    if exclude_hidden_files and _is_hidden_file(file):
        return False
    return True


def _is_hidden_file(full_path):
    def is_windows():
        return os.name == 'nt'

    def has_hidden_attribute(file_path):
        return is_windows() and bool(os.stat(file_path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)

    try:
        return os.path.basename(full_path).startswith('.') or has_hidden_attribute(full_path)
    except FileNotFoundError:
        return False


def generate_schema_default_dict(schema, path=""):
    """
    Recursively generate a valid instance dictionary from a given JSON schema
    that includes only the fields that are required or have a default value.

    :param schema: The JSON schema dictionary.
    :param path: The path to the current position in the schema (for nested objects).
    :return: A valid instance dictionary according to the schema.
    """
    if "type" not in schema:
        schema["type"] = "any"
    if schema["type"] == "object":
        obj = {}
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        for key, value in properties.items():
            print("key", key)
            print("value", value)
            if key in required_fields or "default" in value:
                # Construct the new path for nested objects
                new_path = f"{path}.{key}" if path else key
                # Recursive call for nested objects or fields with default values
                obj[key] = generate_schema_default_dict(value, path=new_path)
        return obj
    elif schema["type"] == "string":
        # Return the default value if specified, otherwise an empty string if required
        return schema.get("default", "")
    elif schema["type"] == "boolean":
        # Return the default value if specified, otherwise False if required
        return schema.get("default", False)
    elif schema["type"] == "array":
        # Return an empty list or the default value if specified
        return schema.get("default", [])
    elif schema["type"] == "number":
        # Return the default value if specified, otherwise 0 if required
        return schema.get("default", 0)
    elif schema["type"] == "integer":
        # Return the default value if specified, otherwise 0 if required
        return schema.get("default", 0)
    elif schema["type"] == "null":
        # Just return None for null types
        return None
    elif schema["type"] == "any":
        # return None for any type if no default
        return schema.get("default", None)
    else:
        # Extend with additional types as needed
        raise ValueError(f"Unsupported type in path {path}: {schema['type']}")


def find_files_in_folder_recursively(root: str,
                                     excluded_files: Set[str] = None,
                                     excluded_folders: Set[str] = None,
                                     file_extensions: Set[str] = None,
                                     exclude_dot_files: bool = False,
                                     exclude_hidden_files: bool = True):
    if excluded_folders is None:
        excluded_folders = {}
    files_to_deploy = list()
    for (dir_path, _, files) in os.walk(root):
        relative_dir_path = os.path.relpath(dir_path, root)
        if any(relative_dir_path.startswith(excluded_folder) for excluded_folder in excluded_folders):
            continue
        for filename in files:
            if exclude_dot_files and filename.startswith('.'):
                continue
            if file_extensions is not None and pathlib.Path(filename).suffix not in file_extensions:
                continue
            full_path = os.path.join(dir_path, filename)
            if exclude_hidden_files and _is_hidden_file(full_path):
                continue
            relative_path = os.path.relpath(full_path, root)
            if excluded_files is not None and relative_path in excluded_files:
                continue
            files_to_deploy.append(relative_path)
    return files_to_deploy


def get_credentials_json() -> Optional[dict]:
    return load_json(DEPLOY_JSON_FILE)


def parse_url_username_password(args):
    credentials_json = None
    if args.username is None or args.password is None or args.url is None:
        credentials_json = get_credentials_json()
        print("credentials_json", credentials_json)
        if (credentials_json is None or credentials_json.get('username') is None or
                credentials_json.get('password') is None or credentials_json.get('url') is None):
            raise Exception('deploy: error: the following arguments are required: --username, --password, --url')
    url = args.url if args.url else credentials_json.get('url')
    username = args.username if args.username else credentials_json.get('username')
    password = args.password if args.password else credentials_json.get('password')
    return url, username, password
