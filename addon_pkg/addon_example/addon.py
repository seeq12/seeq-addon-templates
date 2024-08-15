import argparse

from _dev_tools.ao_tasks import (
    bootstrap as bootstrapping,
    build as building,
    package as packaging,
    deploy as deploying,
    watch as watching,
    elements_testing as testing
)


def bootstrap(args):
    bootstrapping(args)


def build(args=None):
    building(args)


def package(args=None):
    packaging(args)


def deploy(args):
    deploying(args)


def watch(args):
    watching(args)


def elements_test(args):
    testing(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='addon.py', description='Add-on Manager')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_bootstrap = subparsers.add_parser('bootstrap', help='Bootstrap your add-on development environment')
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
