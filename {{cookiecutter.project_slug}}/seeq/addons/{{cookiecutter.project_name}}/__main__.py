import os
import sys
import argparse
import subprocess
from getpass import getpass
from urllib.parse import urlparse
from seeq import spy
# noinspection PyProtectedMember
from seeq.spy._errors import *
# noinspection PyProtectedMember
from seeq.spy import _url
from seeq.sdk import SystemApi, ConfigurationInputV1, ConfigurationOptionInputV1
from seeq.addons.{{cookiecutter.project_name}}.utils import copy_notebooks

NB_EXTENSIONS = ['widgetsnbextension', 'plotlywidget', 'ipyvuetify', 'ipyvue']
DEPLOYMENT_FOLDER = 'deployment'
DEPLOYMENT_NOTEBOOK = "{{cookiecutter.project_name}}_deployment.ipynb"
DEFAULT_GROUP = ['Everyone']
DEFAULT_USERS = []
ADDON_NAME = "{{cookiecutter.addon_name}}"
ADDON_DESCRIPTION = "{{cookiecutter.addon_description}}"
ADDON_ICON = '{{cookiecutter.addon_icon}}'
ADDON_WINDOW_DETAILS = "{{cookiecutter.addon_window_details}}"
ADDON_SORT_KEY = "a"


def install_app(sdl_url_, *, permissions_group: list = None, permissions_users: list = None):
    """
    Installs MyFirstAddOn as an Add-on Tool in Seeq Workbench.

    Parameters
    ----------
    sdl_url_: str
        URL of the SDL container.
        E.g. `https://my.seeq.com/data-lab/6AB49411-917E-44CC-BA19-5EE0F903100C/`
    permissions_group: list
        Names of the Seeq groups that will have access to each tool. If None,
        the "Everyone" group will be used by default.
    permissions_users: list
        Names of Seeq users that will have access to each tool. If None, no
        individual users will be given access to the tool.

    Returns
    --------
    -: None
        MyFirstAddOn will appear as Add-on Tool(s) in Seeq
        Workbench
    """

    permissions_group = permissions_group if permissions_group else DEFAULT_GROUP
    permissions_users = permissions_users if permissions_users else DEFAULT_USERS

    add_on_details = {
        "Name": ADDON_NAME,
        "Description": ADDON_DESCRIPTION,
        "Icon": ADDON_ICON,
        "Target URL": f'{sdl_url_}/apps/{DEPLOYMENT_FOLDER}/{DEPLOYMENT_NOTEBOOK}',
        "Link Type": "window",
        "Window Details": ADDON_WINDOW_DETAILS,
        "Sort Key": ADDON_SORT_KEY,
        "Reuse Window": False,
        "Groups": permissions_group,
        "Users": permissions_users
    }

    copy_notebooks(des_folder=DEPLOYMENT_FOLDER, src_folder='deployment_notebook', overwrite_folder=False,
                   overwrite_contents=True)
    print(f'\nCopied the notebook used by the Add-on to {DEPLOYMENT_FOLDER}')
    spy.addons.install(add_on_details, include_workbook_parameters=True, update_tool=True, update_permissions=True)


def install_nbextensions():
    """
    Installs the Jupyter nbextensions required to render the Add-on

    Returns
    -------
    -: None
    """
    for extension in NB_EXTENSIONS:
        subprocess.run(f'jupyter nbextension install --user --py {extension}', cwd=os.path.expanduser('~'), shell=True,
                       check=True)
        subprocess.run(f'jupyter nbextension enable --user --py {extension}', cwd=os.path.expanduser('~'), shell=True,
                       check=True)


def login_attempts(_user):
    """
    Allows user to re-enter credentials multiple times in the event of
    authentication failure

    Parameters
    ----------
    _user: str
        Seeq username that needs to be authenticated

    Returns
    -------
    -: None
    """
    count = 0
    allowed_attempts = 20
    while count <= allowed_attempts:
        try:
            if _user is None or count >= 1:
                _user = input("\nAccess Key or Username: ")

            passwd = getpass("Access Key Password: ")
            spy.login(username=_user, password=passwd, ignore_ssl_errors=True)
            break
        except (SPyRuntimeError, SPyValueError):
            count += 1
            try_again = "-"
            while try_again != 'yes' and try_again != 'no':
                try_again = input("\nTry again (yes/no)? [yes] ")
                if try_again == '' or try_again.lower() == 'y':
                    try_again = 'yes'
                if try_again.lower() == 'n':
                    try_again = 'no'
            print("-" * 60)
            if try_again.lower() == 'no':
                raise
            if count > allowed_attempts:
                raise RuntimeError("Number of login attempts exceeded")


def cli_interface():
    """ Installs {{cookiecutter.camelcase_addon_class}} as a Seeq Add-on Tool """
    parser = argparse.ArgumentParser(description='Install {{cookiecutter.camelcase_addon_class}} as a Seeq Add-on Tool')
    parser.add_argument('--nbextensions_only', action='store_true',
                        help='Only installs the nbextensions without installing or updating the Add-on Tools'
                             'links')
    parser.add_argument('--username', type=str,
                        help='Username or Access Key of Seeq admin user installing the tool(s) ')
    parser.add_argument('--seeq_url', type=str, nargs='?',
                        help="Seeq hostname URL with the format https://my.seeq.com/ or https://my.seeq.com:34216")
    parser.add_argument('--users', type=str, nargs='*', default=[],
                        help="List of the Seeq users to will have access to the {{cookiecutter.camelcase_addon_class}}"
                             " Add-on Tool, default: %(default)s")
    parser.add_argument('--groups', type=str, nargs='*', default=['Everyone'],
                        help="List of the Seeq groups to will have access to the {{cookiecutter.camelcase_addon_class}}"
                             " Add-on Tool, default: %(default)s")
    return parser.parse_args()


def enable_addon_tools():
    system_api = SystemApi(spy.client)
    config_option_input = ConfigurationOptionInputV1(path='Features/AddOnTools/Enabled', value=True)
    system_api.set_configuration_options(body=ConfigurationInputV1([config_option_input]))


if __name__ == '__main__':

    args = cli_interface()
    if args.nbextensions_only:
        print("\n\nInstalling and enabling nbextensions")
        install_nbextensions()
        sys.exit(0)
    user = args.username
    login_attempts(user)
    seeq_url = args.seeq_url
    if seeq_url is None:
        seeq_url = input(f"\n Seeq base URL [{spy.client.host.split('/api')[0]}]: ")
        if seeq_url == '':
            seeq_url = spy.client.host.split('/api')[0]
    url_parsed = urlparse(seeq_url)
    seeq_url_base = f"{url_parsed.scheme}://{url_parsed.netloc}"

    project_id = spy.utils.get_data_lab_project_id()
    sdl_url = f'{seeq_url_base}/data-lab/{project_id}'
    if project_id is None:
        print("\nThe project ID could not be found. Please provide the SDL project URL with the format "
              "https://my.seeq.com/data-lab/6AB49411-917E-44CC-BA19-5EE0F903100C/\n")
        sdl_url = input("Seeq Data Lab project URL: ")
        project_id = spy.utils.get_data_lab_project_id_from_url(sdl_url)
        if not project_id:
            raise RuntimeError(f'Could not install "{{cookiecutter.project_slug}}" because the SDL project ID could not be found')
    sdl_url_sanitized = _url.SeeqURL.parse(sdl_url).url

    # App Installation
    if not spy.user.is_admin:
        print('You must be an admin user to install AddOns')
        sys.exit(1)

    print(f"\nThe {{cookiecutter.camelcase_addon_class}} Tool will be installed on the SDL "
          f"notebook: {sdl_url_sanitized}\n"
          f"If this is not your intent, you can quit the installation now ")
    print('\n[enter] to continue or type "quit" to exit installation')
    choice = None
    while choice != '' and choice != 'quit':
        choice = input()
        if choice == '':
            print("Enabling Add On Tools...")
            enable_addon_tools()
            print("\n\nInstalling and enabling nbextensions")
            install_nbextensions()
            install_app(sdl_url_sanitized, permissions_group=args.groups, permissions_users=args.users)
        elif choice == 'quit':
            print("\nExited installation")
        else:
            print(f'\nCommand "{choice}" is not valid')
            print('\n[enter] to continue the installation or type "quit" to exit installation')
