import json
import os
import pathlib
import stat
from typing import Optional, Dict, List, Set


def load_json(path: pathlib.Path) -> Optional[dict]:
    if not path.exists():
        return None
    with open(path, mode='r', encoding='utf-8') as json_file:
        return json.load(json_file)


def save_json(path: pathlib.Path, values: dict) -> None:
    with open(path, mode='w', encoding='utf-8') as json_file:
        json.dump(values, json_file, indent=2, ensure_ascii=False)


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

