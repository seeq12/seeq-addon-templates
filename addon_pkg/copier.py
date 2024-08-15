#!/usr/bin/env python
import argparse
import pathlib

import copier


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()


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


def create_addon(args):
    args = modify_args(args)
    copier.run_copy(str(CURRENT_DIRECTORY), data=None, **vars(args))


def update_addon(args=None):
    args = modify_args(args)
    copier.run_recopy(data=None, **vars(args))


def main():
    parser = argparse.ArgumentParser(prog='copier.py', description='Template generator for Seeq Add-ons')
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

    parser_create = subparsers.add_parser('create', description='create a new Seeq Add-on example')

    parser_update = subparsers.add_parser('update',
                                          description='update an existing Seeq Add-on example with the latest template')
    for option, option_args in copier_options.items():
        parser_create.add_argument(option, **option_args)
        parser_update.add_argument(option, **option_args)

    parser_create.set_defaults(func=create_addon)
    parser_update.set_defaults(func=update_addon)

    options, unknown = parser.parse_known_args()
    options.func(options)


if __name__ == "__main__":
    main()
