#!/usr/bin/env python
import os
import shutil
import argparse
import pathlib
import subprocess

import copier
from addon_template._dev_tools.utils import create_virtual_environment


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
WINDOWS_OS = os.name == 'nt'
SOURCE_REPOSITORY = 'seeq-addon-templates'


def get_git_repo_name(path: pathlib.Path):
    path = path.resolve()
    while path != path.parent:  # Stop when we reach the root directory
        try:
            repo_path = subprocess.check_output(['git', '-C', path, 'rev-parse', '--show-toplevel'], stderr=subprocess.STDOUT)
            repo_path = repo_path.decode('utf-8').strip()
            repo_path = pathlib.Path(repo_path)
            if repo_path == path:
                repo_url = subprocess.check_output(['git', '-C', path, 'remote', 'get-url', 'origin'], stderr=subprocess.STDOUT)
                repo_url = repo_url.decode('utf-8').strip()

                return repo_url.split('/')[-1].replace('.git', '')
        except subprocess.CalledProcessError:
            pass  # If the current directory is not a git repository, move up to the parent directory
        path = path.parent

    return None


def is_path_in_source_git_repo(path: pathlib.Path):
    if get_git_repo_name(path) == SOURCE_REPOSITORY:
        return True
    else:
        return False


def copy_dev_tools(destination_path):
    print(f"Copying `_dev_tools` to {destination_path}")
    destination = destination_path / "_dev_tools"
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(CURRENT_DIRECTORY / "_dev_tools", destination)


def delete_pycache(destination_path):
    print(f"Deleting `__pycache__` from {destination_path}")
    for root, dirs, files in os.walk(destination_path):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))


def modify_args(args, destination_path=None):
    if args.force or args.data:
        args.defaults = True
        args.overwrite = True
        if not os.path.isfile(destination_path / ".copier-answers.yml"):
            raise FileNotFoundError(
                f"argument --force can't be use if file {destination_path}/.copier-answers.yml doesn't exist."
            )
    delattr(args, 'force')
    delattr(args, 'func')
    delattr(args, 'data')
    args.skip_if_exists = args.skip
    delattr(args, 'skip')
    args.unsafe = True
    return args


def info_open_ide(destination_path):
    return (f"\n{'*' * 80}\n"
            f"Please open the IDE of your choice and navigate to {destination_path}"
            f"\n{'*' * 80}")


def create_addon(args):
    data = args.data
    destination_path = pathlib.Path(args.dst_path).resolve()
    args = modify_args(args, destination_path)

    if is_path_in_source_git_repo(destination_path):
        raise Exception(f"Creating a new Add-on inside the source repository is not allowed. "
                        f"Try a different destination path")

    try:
        copier.run_copy(str(CURRENT_DIRECTORY), data=data, **vars(args))
        copy_dev_tools(destination_path)
        create_virtual_environment(destination_path, clean=True, hide_stdout=True)
        path_to_python = destination_path / ".venv" / ("Scripts" if WINDOWS_OS else "bin") / "python"
        print(f"Installing Add-on dependencies ...")
        command_to_run = f"{path_to_python} {destination_path}/addon.py bootstrap --global-python-env {destination_path}"
        subprocess.run(command_to_run, shell=True, check=True, cwd=destination_path, stdout=subprocess.DEVNULL)
        print(info_open_ide(destination_path))
    except KeyboardInterrupt as e:
        print(f"\nError: Operation canceled by user")
    except Exception as e:
        print(f"\nError: {e}")


def update_addon(args=None):
    data = args.data
    destination_path = pathlib.Path(args.dst_path).resolve()
    args = modify_args(args, destination_path)

    if is_path_in_source_git_repo(destination_path):
        raise Exception(f"Creating a new Add-on inside the source repository is not allowed. "
                        f"Try a different destination path")

    try:
        copier.run_recopy(data=data, **vars(args))
        copy_dev_tools(destination_path)
        print(info_open_ide(destination_path))
    except KeyboardInterrupt as e:
        print(f"\nError: Operation canceled by user")
    except Exception as e:
        print(f"\nError: {e}")


def main():
    def parse_dict(arg):
        pairs = arg.split(',')
        return dict(pair.split('=') for pair in pairs)

    parser = argparse.ArgumentParser(prog='generator.py', description='Template generator for Seeq Add-ons')
    subparsers = parser.add_subparsers(description='sub-command help', required=True)

    copier_options = {
        'dst_path': dict(
            type=str,
            default=None,
            help='Destination directory for the new Seeq Add-on generated example'),
        '--cleanup-on-error': dict(
            action='store_true',
            required=False,
            default=True,
            help='On error, do not delete destination'),
        '--answers-file': dict(
            type=str,
            default=None,
            required=False,
            help='Update using this path (relative to `destination_path`) to find the answers file'),
        '--force': dict(
            action='store_true',
            default=False,
            required=False,
            help='Same as `--defaults --overwrite`.'),
        '--data': dict(
            type=parse_dict,
            default=None,
            required=False,
            help="Update only the specified data in the template. "
                 "For example: `--data 'project_license=Apache License 2.0, project_maintainer=Seeq'`"
        ),
        '--defaults': dict(
            action='store_true',
            required=False,
            help='Use default answers to questions, which might be null if not specified.'),
        '--overwrite': dict(
            action='store_true',
            required=False,
            help='Overwrite files that already exist, without asking'),
        '--pretend': dict(
            action='store_true',
            required=False,
            help='Run but do not make any changes'),
        '--skip': dict(
            type=str,
            nargs='*',
            default=[],
            required=False,
            help='Skip specified files if they exist already; may be given multiple times'),
        '--exclude': dict(
            type=str,
            nargs='*',
            default=[],
            required=False,
            help='A name or shell-style pattern matching files or folders that must not be copied; '
                 'may be given multiple times')
    }

    subparsers_info = {
        'create': 'create a new Seeq Add-on example. '
                  'It will re-create everything from scratch but prompts for previously entered values',
        'update': 'update an existing Seeq Add-on example with the latest template. '
                  'It can be used to update the template or to re-run the template with new values. '
                  'It will not create a new virtual environment, but will re-run `pip install -r requirements.txt`.'
    }

    parser_create = subparsers.add_parser('create',
                                          description=subparsers_info['create'],
                                          help=subparsers_info['create'])

    parser_update = subparsers.add_parser('update',
                                          description=subparsers_info['update'],
                                          help=subparsers_info['update'])
    for option, option_args in copier_options.items():
        parser_create.add_argument(option, **option_args)
        parser_update.add_argument(option, **option_args)

    parser_create.set_defaults(func=create_addon)
    parser_update.set_defaults(func=update_addon)

    options, unknown = parser.parse_known_args()
    options.func(options)


if __name__ == "__main__":
    main()
