from _dev_tools.add_on_manager_session import AddOnManagerSession
from _dev_tools.utils import get_add_on_identifier


def uninstall(args):
    add_on_identifier = get_add_on_identifier()
    session = AddOnManagerSession(args.url, args.username, args.password)
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
