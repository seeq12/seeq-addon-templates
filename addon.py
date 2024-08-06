import argparse
import copier


def create_addon(args):
    pass


def recreate_addon(args=None):
    pass


def update_addon(args=None):
    pass


def deploy(args):
    pass


def watch(args):
    pass


def elements_test(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='addon.py', description='Template generator for Seeq Add-ons')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_create = subparsers.add_parser('create', help='create a new Seeq Add-on example')
    parser_create.add_argument('--dir', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.add_argument('--no-cleanup', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.add_argument('--dir', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.add_argument('--dir', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.add_argument('--dir', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.add_argument('--dir', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.add_argument('--dir', type=str, nargs='*', default=None, required=True,
                               help='Destination directory for the new Seeq Add-on generated example')
    parser_create.set_defaults(func=create_addon)

    parser_recreate = subparsers.add_parser('recreate', help='Build your add-on')
    parser_recreate.add_argument('--dir', type=str, nargs='*', default=None,
                                 help='Execute the command for the subset of the element directories specified.')
    parser_recreate.set_defaults(func=build)

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
