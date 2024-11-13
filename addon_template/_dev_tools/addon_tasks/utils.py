import importlib
import json
import os
import pathlib
import sys
import asyncio
import base64
from typing import Optional, List, Dict, Set
from datetime import datetime
from os.path import isdir, relpath
from stat import FILE_ATTRIBUTE_HIDDEN

from _dev_tools.addon_tasks.element_protocol import ElementProtocol

PROJECT_PATH = pathlib.Path(__file__).parent.parent.parent.resolve()
WHEELS_PATH = PROJECT_PATH / '.wheels'
DIST_FOLDER = PROJECT_PATH / 'dist'
ADDON_JSON_FILE = PROJECT_PATH / "addon.json"
ADD_ON_EXTENSION = '.addon'
CREDENTIALS_JSON_FILE = PROJECT_PATH / ".credentials.json"

ELEMENT_ACTION_FILE = 'element'

IDENTIFIER = "identifier"
VERSION = 'version'
ELEMENTS = 'elements'
ELEMENT_PATH = 'path'
ELEMENT_TYPE = 'type'
ELEMENT_IDENTIFIER = 'identifier'
CONFIGURATION_SCHEMA = "configuration_schema"
PREVIEWS = "previews"

ADD_ON_TOOL_TYPE = "AddOnTool"
DEFAULT_ADD_ON_TOOL_ELEMENT_PATH = f'{pathlib.Path(__file__).parent.parent.name}.defaults.data_lab_project'
DISPLAY_PANE_PLUGIN_TYPE = "Plugin"
DEFAULT_DISPLAY_PANE_PLUGIN_ELEMENT_PATH = f'{pathlib.Path(__file__).parent.parent.name}.defaults.plugin'
TOOL_PANE_PLUGIN_TYPE = "Plugin"
DEFAULT_TOOL_PANE_PLUGIN_ELEMENT_PATH = f'{pathlib.Path(__file__).parent.parent.name}.defaults.plugin'
FORMULA_PACKAGE_TYPE = "FormulaPackage"
DEFAULT_FORMULA_PACKAGE_ELEMENT_PATH = f'{pathlib.Path(__file__).parent.parent.name}.defaults.formula_package'
DATA_LAB_FUNCTIONS_TYPE = "DataLabFunctions"
DATA_LAB_FUNCTIONS_ELEMENT_PATH = f'{pathlib.Path(__file__).parent.parent.name}.defaults.data_lab_project'

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
NOTE_FOR_FEATURE_FLAG_CHANGE = "Enabled by Add-on Packaging Utility"


def save_json(path: pathlib.Path, values: dict) -> None:
    with open(path, mode='w', encoding='utf-8') as json_file:
        json.dump(values, json_file, indent=2, ensure_ascii=False)


def load_json(path: pathlib.Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        with open(path, mode='r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except json.JSONDecodeError:
        raise Exception(f'Error loading JSON file: {path}')


def get_credentials_json() -> Optional[dict]:
    return load_json(CREDENTIALS_JSON_FILE)


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
        elif element_type == FORMULA_PACKAGE_TYPE:
            module = load_module(f"{DEFAULT_FORMULA_PACKAGE_ELEMENT_PATH}.{ELEMENT_ACTION_FILE}")
            assert isinstance(module, ElementProtocol)
            return module
        elif element_type == DISPLAY_PANE_PLUGIN_TYPE:
            module = load_module(f"{DEFAULT_DISPLAY_PANE_PLUGIN_ELEMENT_PATH}.{ELEMENT_ACTION_FILE}")
            assert isinstance(module, ElementProtocol)
            return module
        elif element_type == TOOL_PANE_PLUGIN_TYPE:
            module = load_module(f"{DEFAULT_TOOL_PANE_PLUGIN_ELEMENT_PATH}.{ELEMENT_ACTION_FILE}")
            assert isinstance(module, ElementProtocol)
            return module
        elif element_type == DATA_LAB_FUNCTIONS_TYPE:
            module = load_module(f"{DATA_LAB_FUNCTIONS_ELEMENT_PATH}.{ELEMENT_ACTION_FILE}")
            assert isinstance(module, ElementProtocol)
            return module
        else:
            raise ModuleNotFoundError(
                f'Neither {element_path}.{ELEMENT_ACTION_FILE} nor '
                f'{DEFAULT_ADD_ON_TOOL_ELEMENT_PATH}.{ELEMENT_ACTION_FILE} were found')


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
    return element_paths


def get_files_to_package() -> List[str]:
    add_on_json = get_add_on_json()
    preview_files = add_on_json.get(PREVIEWS, [])
    return ["addon.json"] + preview_files


def parse_url_username_password(args=None):
    credentials_json = {}
    if (
            args is None
            or args.username is None
            or args.password is None
            or args.url is None
    ):
        credentials_json = get_credentials_json()
        if credentials_json is None:
            return None, None, None

    url = get_non_none_attr(args, "url", credentials_json.get("url"))
    username = get_non_none_attr(args, "username", credentials_json.get("username"))
    password = get_non_none_attr(args, "password", credentials_json.get("password"))

    return url, username, password


def get_non_none_attr(obj, attr, default):
    value = getattr(obj, attr, default)
    return value if value is not None else default


def _get_timestamp():
    return datetime.now().astimezone().strftime(TIMESTAMP_FORMAT)


def get_element_identifier_from_path(element_path: pathlib.Path) -> str:
    """Used from inside an element to get its identifier from addon.json"""
    add_on_json = get_add_on_json()
    elements = add_on_json[ELEMENTS]
    print(f"Looking for element with path: {element_path.resolve()}")
    return next(
        element[IDENTIFIER]
        for element in elements
        if (PROJECT_PATH / element[ELEMENT_PATH]).resolve() == element_path.resolve()
    )


def filter_element_paths(element_paths_with_type: Optional[Dict[str, str]], subset_folders: Optional[List[str]]):
    if subset_folders is None:
        return element_paths_with_type
    return {element_path: element_type for element_path, element_type in element_paths_with_type.items()
            if element_path in subset_folders}


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


def check_feature_is_enabled(url, username, password, feature_path):
    from seeq import sdk, spy
    spy.login(username=username, password=password, url=url, quiet=True)
    system_api = sdk.SystemApi(spy.client)
    response = system_api.get_server_status()
    for option in response.configuration_options:
        if option.path == feature_path:
            if option.value is False:
                if spy.user.is_admin:
                    print(f"Feature {feature_path} is not enabled. Enabling it now.")
                    system_api.set_configuration_options(body={
                        "configurationOptions": [
                            {
                                "note": NOTE_FOR_FEATURE_FLAG_CHANGE,
                                "path": feature_path,
                                "value": True
                            }
                        ],
                        "dryRun": False
                    })
                else:
                    raise ValueError(
                        f"Feature {feature_path} is not enabled. Please contact your Seeq administrator to enable it")


def _get_authenticated_session(element_path, url, username, password):
    from seeq import sdk, spy
    spy.login(username=username, password=password, url=url, quiet=True)
    auth_header = {'sq-auth': spy.client.auth_token}
    items_api = sdk.ItemsApi(spy.client)
    element_project_name = get_element_identifier_from_path(element_path)
    response = items_api.search_items(filters=[f'name=={element_project_name}'], types=['Project'])
    if len(response.items) == 0:
        raise Exception(f"Could not find a project with name {element_project_name}")
    project_id = response.items[0].id
    requests_session = _create_requests_session()
    return requests_session, auth_header, project_id


def _create_requests_session():
    import requests
    from requests.adapters import HTTPAdapter, Retry
    max_request_retries = 5
    request_retry_status_list = [502, 503, 504]
    _http_adapter = HTTPAdapter(
        max_retries=Retry(total=max_request_retries, backoff_factor=0.5, status_forcelist=request_retry_status_list))
    request_session = requests.Session()
    request_session.mount("http://", _http_adapter)
    request_session.mount("https://", _http_adapter)
    return request_session


def _upload_file(server_url, request_session, auth_header, project_id, source, destination):
    from requests.exceptions import RetryError

    jupyter_path = _get_jupyter_contents_api_path(server_url, project_id, destination)
    base_name = os.path.basename(source)
    with open(source, 'rb') as file:
        contents = file.read() or b''
    body = json.dumps({'path': jupyter_path.replace('//', r'/'),
                       'content': base64.b64encode(contents).decode('ascii'),
                       'format': 'base64',
                       'name': base_name,
                       'type': 'file'})
    response = None
    try:
        response = request_session.put(jupyter_path, data=body, headers=auth_header, cookies=auth_header,
                                       verify=True, timeout=60)
    except RetryError:
        pass
    if response is None or response.status_code == 500:
        _upload_directory(server_url, request_session, auth_header, project_id, destination)
        try:
            response = request_session.put(jupyter_path, data=body, headers=auth_header, cookies=auth_header,
                                           verify=True, timeout=60)
        except RetryError:
            pass

    status = "Success" if (response is not None) else "Failure"
    print(f"    {_get_timestamp()} Attempt to Upload {base_name} : {status}")


def _upload_directory(server_url, request_session, auth_header, project_id, full_path):
    from requests.exceptions import RetryError
    path_parts = pathlib.Path(full_path).parts
    paths_to_create = [list(path_parts[:i]) for i in range(1, len(path_parts))]
    body = json.dumps({'type': 'directory'})
    base = [server_url, 'data-lab', project_id, 'api', 'contents']
    for path in paths_to_create:
        try:
            request_session.put('/'.join(base + path), data=body,
                                headers=auth_header, cookies=auth_header,
                                verify=True, timeout=60)
        except RetryError:
            pass


def _delete_file(server_url, request_session, auth_header, project_id, source, destination):
    from requests.exceptions import RetryError
    base_name = os.path.basename(source)
    jupyter_path = _get_jupyter_contents_api_path(server_url, project_id, destination)
    response = None
    try:
        response = request_session.delete(jupyter_path,
                                          headers=auth_header, cookies=auth_header,
                                          verify=True, timeout=60)
    except RetryError:
        pass
    status = "Success" if (response is not None) else "Failure"
    print(f"    {_get_timestamp()} Attempt to delete {base_name} : {status}")


async def _watch_from_environment(element_path: pathlib.Path, url: str, username: str, password: str,
                                  file_extensions: set, excluded_files: set, excluded_folders: set):
    print(f"Watching {element_path}")
    await asyncio.gather(hot_reload(element_path, url, username, password,
                                    file_extensions, excluded_files, excluded_folders))


async def hot_reload(element_path: pathlib.Path, url: str, username: str, password: str,
                     file_extensions: set, excluded_files: set, excluded_folders: set):

    from watchfiles import awatch, Change
    requests_session, auth_header, project_id = _get_authenticated_session(element_path, url, username, password)
    async for changes in awatch(element_path):
        for change in changes:
            if isdir(change[1]):
                continue  # folder creation handled in _upload_directory

            deleted = change[0] == Change.deleted
            absolute_file_path = change[1]
            destination = relpath(absolute_file_path, element_path)

            if file_matches_criteria(str(element_path),
                                     absolute_file_path,
                                     file_extensions=file_extensions,
                                     excluded_files=excluded_files,
                                     excluded_folders=excluded_folders):
                if deleted:
                    _delete_file(url, requests_session, auth_header, project_id,
                                 absolute_file_path, destination)
                else:
                    _upload_file(url, requests_session, auth_header, project_id,
                                 absolute_file_path, destination)
                _shut_down_kernel(url, requests_session, auth_header, project_id)


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
        return is_windows() and bool(os.stat(file_path).st_file_attributes & FILE_ATTRIBUTE_HIDDEN)

    try:
        return os.path.basename(full_path).startswith('.') or has_hidden_attribute(full_path)
    except FileNotFoundError:
        return False


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


def _shut_down_kernel(url: str, requests_session, auth_header, project_id):
    shut_down_endpoint = f'{url}/data-lab/{project_id}/functions/shutdown'
    requests_session.post(shut_down_endpoint, headers=auth_header, cookies=auth_header)


def _get_jupyter_contents_api_path(url, project_id, path):
    return f'{url}/data-lab/{project_id}/api/contents/' + path.replace('\\', '//')
