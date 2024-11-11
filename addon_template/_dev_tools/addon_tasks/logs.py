from io import StringIO
import pandas as pd
from bs4 import BeautifulSoup


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


def print_all_log_files(args):
    """
    Get the log files from the Add-on Manager
    """
    url, username, password = parse_url_username_password(args)
    save_json(CREDENTIALS_JSON_FILE, {'url': url, 'username': username, 'password': password})
    session = AddOnManagerSession(url, username, password)
    log_files = session.get_logs()
    soup = BeautifulSoup(log_files.text, 'html.parser')
    tables = pd.read_html(StringIO(str(soup)))
    df = tables[0]
    df.columns = ['Log Filename', 'Size', 'Modified Date (UTC)']

    print(df)


def print_logs(args):
    """
    Get the latest logs from the Add-on Manager
    """

    url, username, password = parse_url_username_password(args)
    save_json(CREDENTIALS_JSON_FILE, {'url': url, 'username': username, 'password': password})
    session = AddOnManagerSession(url, username, password)
    if not session.spy_session.user.is_admin:
        print("You must be an admin to view Add-on Manager logs.")
        return
    log_file = f"{session.ADD_ON_MANAGER_PROJECT_NAME}.log" if args.logs_aom else args.file
    print(log_file)
    logs = session.get_logs(log_file)
    soup = BeautifulSoup(logs.text, 'html.parser')
    print(soup.text)


def parse_logs(logs: str):
    lines = logs.strip().split("\n")

    # Split each line into its components and store in a list
    data = []
    for line in lines:
        parts = line.split(" - ", 1)
        log_level, timestamp, source = parts[0].split()
        user_start = parts[1].find("User: ") + len("User: ")
        user_end = parts[1].find(" N/A")
        user = parts[1][user_start:user_end]
        message = parts[1][user_end + len(" N/A"):]
        components = [log_level, timestamp, source, user, message]
        data.append(components)

    # Create a DataFrame from the list
    df = pd.DataFrame(data, columns=['Log Level', 'Timestamp', 'Source', 'User', 'Message'])
    return df
