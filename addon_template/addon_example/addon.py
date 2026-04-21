import argparse
import os
import pathlib
import sys


PROJECT_PATH = pathlib.Path(__file__).parent.resolve()
VENV_PYTHON = PROJECT_PATH / ".venv" / ("Scripts" if os.name == "nt" else "bin") / "python"


def _reexec_in_project_venv():
    if not VENV_PYTHON.exists():
        return
    current_prefix = pathlib.Path(sys.prefix).resolve()
    if current_prefix == (PROJECT_PATH / ".venv").resolve():
        return
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON), str(PROJECT_PATH / "addon.py"), *sys.argv[1:]])

def bootstrap(args):
    from _dev_tools.addon_tasks.bootstrap import bootstrap as bootstrapping
    bootstrapping(args)


def build(args=None):
    from _dev_tools.addon_tasks.build import build as building
    building(args)


def package(args=None):
    from _dev_tools.addon_tasks.package import package as packaging
    packaging(args)


def deploy(args):
    from _dev_tools.addon_tasks.deploy import deploy as deploying
    deploying(args)


def watch(args):
    from _dev_tools.addon_tasks.watch import watch as watching
    watching(args)


def elements_test(args):
    from _dev_tools.addon_tasks.testing import elements_testing as testing
    testing(args)


def logs(args):
    from _dev_tools.addon_tasks.logs import print_all_log_files, print_logs
    args.logs_aom = False
    if args.file is None:
        print_all_log_files(args)
        return
    return print_logs(args)


def logs_aom(args):
    from _dev_tools.addon_tasks.logs import print_logs
    args.logs_aom = True
    return print_logs(args)


if __name__ == "__main__":
    _reexec_in_project_venv()
    parser = argparse.ArgumentParser(prog='addon.py', description='Add-on Developer Tools')
    subparsers = parser.add_subparsers(help='sub-command help', required=True)

    parser_bootstrap = subparsers.add_parser('bootstrap', help='Bootstrap your Add-on development environment')
    parser_bootstrap.add_argument('--username', type=str, required=False, default=None)
    parser_bootstrap.add_argument('--password', type=str, required=False, default=None)
    parser_bootstrap.add_argument('--url', type=str, required=False, default=None)
    parser_bootstrap.add_argument('--clean', action='store_true', default=False, help='Clean bootstrap')
    parser_bootstrap.add_argument('--dir', type=str, nargs='*', default=None,
                                  help='Execute the command for the subset of the element directories specified.')
    parser_bootstrap.add_argument('--global-python-env', type=str, nargs='?', default=None,
                                  help='Installs all python dependencies in the same global environment.')
    parser_bootstrap.set_defaults(func=bootstrap)

    parser_build = subparsers.add_parser('build', help='Build your Add-on')
    parser_build.add_argument('--dir', type=str, nargs='*', default=None,
                              help='Execute the command for the subset of the element directories specified.')
    parser_build.set_defaults(func=build)

    parser_deploy = subparsers.add_parser('deploy', help='Deploy your Add-on')
    parser_deploy.add_argument('--username', type=str, required=False)
    parser_deploy.add_argument('--password', type=str, required=False)
    parser_deploy.add_argument('--url', type=str, required=False)
    parser_deploy.add_argument('--clean', action='store_true', default=False, help='Uninstall')
    parser_deploy.add_argument('--replace', action='store_true', default=False, help='Replace elements')
    parser_deploy.add_argument('--skip-build', action='store_true', default=True, help='Skip build step')
    parser_deploy.add_argument('--dir', type=str, nargs='*', default=None,
                               help='Execute the command for the subset of the element directories specified.')
    parser_deploy.set_defaults(func=deploy)

    parser_package = subparsers.add_parser('package', help='Package your Add-on')
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

    parser_logs = subparsers.add_parser('logs-aom', help='Get the Add-on Manager latest logs')
    parser_logs.add_argument('--username', type=str)
    parser_logs.add_argument('--password', type=str)
    parser_logs.add_argument('--url', type=str)
    parser_logs.set_defaults(func=logs_aom)

    parser_logs = subparsers.add_parser(
        'logs',
        help='Get the list of Add-on Manager log files '
             'or view of the logs of a specific file if `--file <filename>` is supplied.')
    parser_logs.add_argument('--username', type=str)
    parser_logs.add_argument('--password', type=str)
    parser_logs.add_argument('--url', type=str)
    parser_logs.add_argument('--file', type=str, default=None, required=False,
                             help='View logs of the supplied file.')
    parser_logs.set_defaults(func=logs)

    parser_test = subparsers.add_parser('test', help='Run the tests for all or individual elements')
    parser_test.add_argument('--dir', type=str, nargs='*', default=None,
                             help='Execute the command for the subset of the element directories specified.')
    parser_test.add_argument('--markers', type=str, default=None,
                             help='Optional pytest marker expression for test runners that support marker selection.')
    parser_test.set_defaults(func=elements_test)

    options, unknown = parser.parse_known_args()
    options.func(options)
