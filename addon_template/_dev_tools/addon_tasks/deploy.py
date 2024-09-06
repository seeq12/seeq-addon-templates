import base64
import json
import pathlib

from .add_on_manager_session import AddOnManagerSession
from _dev_tools.addon_tasks.utils import (
    ADD_ON_EXTENSION,
    DIST_FOLDER,
    ELEMENTS,
    ELEMENT_PATH,
    ELEMENT_IDENTIFIER,
    CONFIGURATION_SCHEMA,
    CREDENTIALS_JSON_FILE,
    get_add_on_identifier,
    parse_url_username_password,
    get_add_on_package_name,
    get_add_on_json,
    generate_schema_default_dict,
    filter_element_paths,
    get_element_paths_with_type,
    get_folders_from_args,
    get_module,
    save_json,
)

from _dev_tools.addon_tasks import package


def deploy(args):
    if args.dir is None:
        _deploy_entire_package(args)
    else:
        url, username, password = parse_url_username_password(args)
        if url is None or username is None or password is None:
            raise Exception("Please provide --url, --user, and --password arguments.")
        save_json(CREDENTIALS_JSON_FILE, {'url': url, 'username': username, 'password': password})
        target_elements = filter_element_paths(get_element_paths_with_type(), get_folders_from_args(args))
        for element_path, element_type in target_elements.items():
            print(f'Deploying element: {element_path}')
            get_module(element_path, element_type).deploy(pathlib.Path(element_path), url, username, password)


def _deploy_entire_package(args):
    add_on_identifier = get_add_on_identifier()
    url, username, password = parse_url_username_password(args)
    session = AddOnManagerSession(url, username, password)

    package(args)

    if args.clean:
        uninstall(args)

    # upload the add-on
    print("Uploading add-on")
    filename = f"{get_add_on_package_name()}{ADD_ON_EXTENSION}"
    print(DIST_FOLDER / f"{filename}")
    with open(DIST_FOLDER / f"{filename}", "rb") as f:
        # file must be base64 encoded
        encoded_file = base64.b64encode(f.read())
        upload_response = session.upload_add_on(filename, encoded_file)
    upload_response.raise_for_status()
    print("Add-on uploaded")
    upload_response_body = upload_response.json()
    print(f"Add-on status is: {upload_response_body['add_on_status']}")

    print("Fetching configuration")
    configuration = get_configuration()

    if upload_response_body['add_on_status'] == "CanInstall":
        print("Installing Add-on")
        install_response = session.install_add_on(
            add_on_identifier, upload_response_body["binary_filename"], configuration
        )
        if not install_response.ok:
            error = install_response.json()["error"]
            error_message = error["message"]
            raise Exception(f"Error installing Add-on: {error_message}")
        install_response.raise_for_status()

    elif upload_response_body['add_on_status'] == "CanUpdate" and args.replace:
        print("Updating Add-on")
        updating_response = session.update_add_on(
            add_on_identifier, upload_response_body["binary_filename"], configuration)
        if not updating_response.ok:
            error = updating_response.json()["error"]
            error_message = error["message"]
            raise Exception(f"Error Updating Add-on: {error_message}")
        updating_response.raise_for_status()
    elif upload_response_body['add_on_status'] == "CanUpdate":
        raise Exception(f"Add-on {get_add_on_identifier()} already exists. Use --replace to update")
    else:
        raise Exception(f"Can't install or update Add-on {get_add_on_identifier()}")

    print("Deployment Complete.")


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
            default_config = generate_schema_default_dict(element[CONFIGURATION_SCHEMA])
            config[element[ELEMENT_IDENTIFIER]] = default_config
        else:
            print(
                f"No configuration schema found for element {element[ELEMENT_IDENTIFIER]}"
            )
            pass
    return config


def uninstall(args):
    add_on_identifier = get_add_on_identifier()
    url, username, password = parse_url_username_password(args)
    session = AddOnManagerSession(url, username, password)
    print("Checking if Add-on is installed")
    add_on_response = session.get_add_on(add_on_identifier)
    if add_on_response.json().get("add_on_status") == "CanUninstall":
        print("Uninstalling add-on")
        uninstall_response = session.uninstall_add_on(add_on_identifier, force=False)
        if not uninstall_response.ok:
            if (
                    uninstall_response.json()["error"]["message"]
                    == f"No installed Add-on found with identifier {get_add_on_identifier()}"
            ):
                raise Exception(f"Unable to uninstall Add-on {get_add_on_identifier()}")
            else:
                if uninstall_response.text:
                    print(uninstall_response.text)
                uninstall_response.raise_for_status()
        print("Uninstall complete")
    else:
        raise Exception(f"Unable to uninstall Add-on {get_add_on_identifier()}")
