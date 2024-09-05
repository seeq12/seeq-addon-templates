import pathlib
import subprocess

from _dev_tools.ao_tasks.utils import (
    filter_element_paths,
    get_element_paths_with_type,
    get_folders_from_args,
    get_module, parse_url_username_password
)


def watch(args):
    target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
    processes = {}
    url, username, password = parse_url_username_password(args)
    if url is None or username is None or password is None:
        raise Exception("Please provide --url, --user, and --password arguments.")
    for element_path, element_type in target_elements.items():
        print(f'watching element: {element_path}')
        processes[element_path] = get_module(
            element_path, element_type
        ).watch(pathlib.Path(element_path), url, username, password)
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
