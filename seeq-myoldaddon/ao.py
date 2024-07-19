import argparse
import base64
import glob
import json
import os
import pathlib
import subprocess
import zipfile
from typing import Optional, List

from _dev_tools import (
    bootstrap as bootstrapping,
    build as building,
    package as packaging,
    deploy as deploying,
)


def bootstrap(args):
    bootstrapping(args)


def build(args=None):
    building(args)


def package(args=None):
    packaging(args)


def deploy(args):
    deploying(args)


















def get_element_types() -> List[str]:
    add_on_json = get_add_on_json()
    if add_on_json is None or ELEMENTS not in add_on_json:
        return []
    return [element.get(ELEMENT_TYPE) for element in add_on_json.get(ELEMENTS)]








def get_configuration():
    """
    Fetch the configuration of the add-on, used when deploying the add-on to add-on-manager.
    If a configuration.json file is present in an element, it will use that instead of the default configuration.
    """
    addon_json = get_add_on_json()
    config = {}
    for element in addon_json[ELEMENTS]:
        # check if there's a configuration.json file in each element. If yes, use that instead of default
        configuration_file_path = (
                pathlib.Path(element[ELEMENT_PATH]) / "configuration.json"
        )
        if configuration_file_path.exists():
            print(f"Using configuration.json for element {element[ELEMENT_IDENTIFIER]}")
            with open(configuration_file_path, "r") as f:
                config[element[ELEMENT_IDENTIFIER]] = json.load(f)
        elif "configuration_schema" in element:
            print(
                f"Using default configuration for element {element[ELEMENT_IDENTIFIER]}"
            )
            default_config = utils.generate_schema_default_dict(element[CONFIGURATION_SCHEMA])
            config[element[ELEMENT_IDENTIFIER]] = default_config
        else:
            print(
                f"No configuration schema found for element {element[ELEMENT_IDENTIFIER]}"
            )
            pass
    return config















# def deploy(args):
#     url, username, password = _parse_url_username_password(args)
#     add_on_identifier = get_add_on_identifier()
#     session = AddOnManagerSession(url, username, password)
#
#     package(args)
#
#     if args.clean:
#         uninstall(args)
#
#     # upload the add-on
#     print("Uploading add-on")
#     filename = f"{get_add_on_package_name()}{ADD_ON_EXTENSION}"
#     with open(
#             DIST_FOLDER / f"{filename}",
#             "rb",
#     ) as f:
#         # file must be base64 encoded
#         encoded_file = base64.b64encode(f.read())
#         upload_response = session.upload_add_on(filename, encoded_file)
#     upload_response.raise_for_status()
#     print("Add-on uploaded")
#     upload_response_body = upload_response.json()
#     print(f"Add-on status is: {upload_response_body['add_on_status']}")
#
#     print("Fetching configuration")
#     configuration = get_configuration()
#     print("Installing Add-on")
#     install_response = session.install_add_on(
#         add_on_identifier, upload_response_body["binary_filename"], configuration
#     )
#     if not install_response.ok:
#         error = install_response.json()["error"]
#         error_message = error["message"]
#         raise Exception(f"Error installing Add-on: {error_message}")
#     install_response.raise_for_status()
#     print("Deployment to Add On Manager Complete")
#
#
#
#
#
#     if args.dir is None:
#         path_to_python = get_module('data-lab-functions', "XXX").PATH_TO_PYTHON
#         command_to_run = (f"{path_to_python} data-lab-functions/deploy.py"
#                           f" --username {username} --password {password} --url {url}")
#         if args.clean:
#             command_to_run += ' --clean'
#         if args.replace:
#             command_to_run += ' --replace'
#         subprocess.run(command_to_run, shell=True, check=True)
#     else:
#         target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
#         for element_path, element_type in target_elements.items():
#             print(f'Deploying element: {element_path}')
#             get_module(element_path, element_type).deploy(url, username, password)



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





if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='ao.py', description='Add-on Manager')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_bootstrap = subparsers.add_parser('bootstrap', help='Bootstrap your add-on development environment')
    # parser_bootstrap.add_argument('--username', type=str, required=False)
    # parser_bootstrap.add_argument('--password', type=str, required=False)
    # parser_bootstrap.add_argument('--url', type=str, default='http://localhost:34216')
    parser_bootstrap.add_argument('--clean', action='store_true', default=False, help='Clean bootstrap')
    parser_bootstrap.add_argument('--dir', type=str, nargs='*', default=None,
                                  help='Execute the command for the subset of the element directories specified.')
    parser_bootstrap.set_defaults(func=bootstrap)

    parser_build = subparsers.add_parser('build', help='Build your add-on')
    parser_build.add_argument('--dir', type=str, nargs='*', default=None,
                              help='Execute the command for the subset of the element directories specified.')
    parser_build.set_defaults(func=build)

    parser_deploy = subparsers.add_parser('deploy', help='Deploy your add-on')
    parser_deploy.add_argument('--username', type=str, required=False)
    parser_deploy.add_argument('--password', type=str, required=False)
    parser_deploy.add_argument('--url', type=str, required=False)
    parser_deploy.add_argument('--clean', action='store_true', default=False, help='Uninstall')
    parser_deploy.add_argument('--replace', action='store_true', default=False, help='Replace elements')
    parser_deploy.add_argument('--skip-build', action='store_true', default=True, help='Skip build step')
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
