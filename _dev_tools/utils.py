import json
import os
import subprocess
import pathlib
import venv

from typing import Optional, Dict, List


def save_json(path: pathlib.Path, values: dict) -> None:
    with open(path, mode='w', encoding='utf-8') as json_file:
        json.dump(values, json_file, indent=2, ensure_ascii=False)


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


def create_virtual_environment(element_path: pathlib.Path, clean: bool = False):

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


def get_venv_paths(element_path: pathlib.Path, path_requested=None):

    venv_path = element_path / ".venv"
    wheels_path = element_path / ".wheels"
    windows_os = os.name == "nt"
    path_to_scripts = venv_path / ("Scripts" if windows_os else "bin")
    path_to_pip = path_to_scripts / "pip"
    path_to_python = path_to_scripts / "python"
    path_to_test = path_to_scripts / "pytest"

    if path_requested is None:
        return venv_path, windows_os, path_to_python, path_to_pip, path_to_scripts, wheels_path
    if path_requested == "venv":
        return venv_path
    if path_requested == "windows_os":
        return windows_os
    if path_requested == "path_to_python":
        return path_to_python
    if path_requested == "path_to_pip":
        return path_to_pip
    if path_requested == "path_to_scripts":
        return path_to_scripts
    if path_requested == "wheels":
        return wheels_path
    if path_requested == "test":
        return path_to_test
