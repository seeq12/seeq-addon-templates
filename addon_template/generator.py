#!/usr/bin/env python
import os
import sys
import argparse
import pathlib
import subprocess


import copier
from addon_template._dev_tools.utils import create_virtual_environment


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
WINDOWS_OS = os.name == 'nt'


def modify_args(args):
    if args.force:
        args.defaults = True
        args.overwrite = True
    delattr(args, 'force')
    delattr(args, 'func')
    args.skip_if_exists = args.skip
    delattr(args, 'skip')
    args.unsafe = True
    return args


def info_open_ide(destination_path):
    return (f"\n{'*' * 80}\n"
            f"Please open the IDE of your choice and navigate to {destination_path}"
            f"\n{'*' * 80}")


def create_addon(args):
    args = modify_args(args)
    try:
        copier.run_copy(str(CURRENT_DIRECTORY), data=None, **vars(args))
        destination_path = pathlib.Path(args.dst_path).resolve()
        create_virtual_environment(destination_path, clean=True, hide_stdout=True)
        path_to_python = destination_path / ".venv" / ("Scripts" if WINDOWS_OS else "bin") / "python"
        print(f"Installing Add-on dependencies ...")
        command_to_run = f"{path_to_python} {destination_path}/addon.py bootstrap --global-python-env {destination_path}"
        subprocess.run(command_to_run, shell=True, check=True, cwd=destination_path, stdout=subprocess.DEVNULL)
        print(info_open_ide(destination_path))
    except KeyboardInterrupt as e:
        print(f"\nError: Operation canceled by user")


def update_addon(args=None):
    args = modify_args(args)
    destination_path = pathlib.Path(args.dst_path).resolve()

    try:
        copier.run_recopy(data=None, **vars(args))
        print(info_open_ide(destination_path))
    except KeyboardInterrupt as e:
        print(f"\nError: Operation canceled by user")


def main():
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
