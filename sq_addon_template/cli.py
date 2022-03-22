import json
import re
import sys
import click
import datetime
from collections import OrderedDict
from pathlib import Path
import cookiecutter as cookie
from cookiecutter.main import cookiecutter
from sq_addon_template import __version__


NAME_REGEX = r'^[a-zA-Z][_a-zA-Z0-9]+$'
DIRECTORY = Path(__file__).parent.resolve()


def version_msg():
    """
    Return the sq-addon-template version, cookiecutter version, location and
    Python powering it.
    """
    python_version = sys.version
    message = f"sq-addon-template: {__version__}\ncookiecutter: {cookie.__version__}" \
              f"\nfrom {DIRECTORY.parent.resolve()} (Python {python_version})"
    return message


def request_user_input(variable, friendly_name, context_variables, defaults, use_defaults=True):
    if use_defaults:
        context_variables[variable] = input(f"{friendly_name} [{defaults[variable]}]: ")
        if context_variables[variable] == '':
            context_variables[variable] = defaults[variable]
    if not use_defaults:
        error = True
        while error:
            context_variables[variable] = input(f"{friendly_name} [{defaults[variable]}]: ")
            if context_variables[variable] != '':
                error = False
            else:
                print(f'ERROR: Please enter a different value for "{friendly_name}"\n')


def user_input_yes_or_no(variable, friendly_name, context_variables, defaults):
    error = True
    while error:
        context_variables[variable] = input(f"{friendly_name} [{defaults[variable][0]}]: ")
        if context_variables[variable] == '' or \
                context_variables[variable].lower() == defaults[variable][0][0].lower() or \
                context_variables[variable].lower() == defaults[variable][0].lower():
            context_variables[variable] = defaults[variable][0].lower()
            error = False
        elif context_variables[variable].lower() == defaults[variable][1][0].lower() or \
                context_variables[variable].lower() == defaults[variable][1].lower():
            context_variables[variable] = defaults[variable][1].lower()
            error = False
        else:
            print(f"""ERROR: Select either 'yes' or 'no'. Got '{context_variables[variable]}'""")


def user_input_list(variable, friendly_name, context_variables, defaults):
    error = True

    options = len(defaults[variable])
    input_message = f'Select {friendly_name} (choose either {" or ".join( [str(x+1) for x in range(options)])}) [1]: '
    input_list = [f"\n{x+1}. {defaults[variable][x]}" for x in range(options)]
    input_message = f'{input_message}{"".join(input_list)}\n'

    while error:
        context_variables[variable] = input(input_message)
        if context_variables[variable] == '':
            context_variables[variable] = defaults[variable][0]
            error = False

        for x in range(options):
            if context_variables[variable] == str(x+1) or context_variables[variable] == defaults[variable][x]:
                context_variables[variable] = defaults[variable][x]
                error = False
        if error:
            print(f"""\nERROR: Select either {" or ".join( [str(x+1) for x in range(options)])}. Got '{
            context_variables[variable]}'\n""")


def check_project_name(project_name):
    if not re.match(NAME_REGEX, project_name):
        print(f'ERROR: The project name "{project_name}" is not a valid module name for this template. '
              f'Name cannot start with a number or an underscore, and it cannot contain hyphens')
        return True
    if 'seeq' in project_name.lower():
        print(f'ERROR: "seeq" cannot be part of the project name.')
        return True


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-V', '--version', message=version_msg())
@click.argument('create', required=False)
@click.option(
    '-c',
    '--checkout',
    help='branch, tag or commit to checkout after git clone',
)
@click.option(
    '--replay',
    is_flag=True,
    help='Do not prompt for parameters and only use information entered previously',
)
@click.option(
    '-f',
    '--overwrite-if-exists',
    is_flag=True,
    help='Overwrite the contents of the output directory if it already exists',
)
@click.option(
    '-s',
    '--skip-if-file-exists',
    is_flag=True,
    help='Skip the files in the corresponding directories if they already exist',
    default=False,
)
@click.option(
    '-o',
    '--output-dir',
    default='.',
    type=click.Path(),
    help='Where to output the generated project dir into',
)
def main(
        create,
        checkout,
        replay,
        overwrite_if_exists,
        skip_if_file_exists,
        output_dir,
):
    """Create a Seeq Add-on project from a Cookiecutter project template.
    """

    # known commands
    known_commands = ['help', 'create']

    if create not in known_commands:
        print('\nERROR: Unknown command\n See help below for correct usage. \n\n')
        create = None

    # Raising usage, after all commands that should work without args.
    if not create or create.lower() == 'help':
        click.echo(click.get_current_context().get_help())
        sys.exit(0)

    if create.lower() == 'create':

        context_variables = OrderedDict()
        kwargs = dict(
            checkout=checkout,
            replay=replay,
            overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir,
            skip_if_file_exists=skip_if_file_exists,
        )

        if kwargs['replay']:
            # Short-circuit everything and re-run with the information previously entered
            cookiecutter(DIRECTORY, **kwargs)
            print(f"'{context_variables['project_slug']}' project created successfully")
            return

        # defaults
        with open(Path.joinpath(DIRECTORY, "cookiecutter.json")) as f:
            defaults = json.load(f)

        error = True
        while error:
            request_user_input('project_name', 'Project name', context_variables, defaults)
            error = check_project_name(context_variables['project_name'])

        context_variables['project_slug'] = f"seeq-{context_variables['project_name'].lower().replace(' ', '-')}"

        user_input_list('project_license', 'project license', context_variables, defaults)

        request_user_input('author', 'Author', context_variables, defaults)
        request_user_input('author_email', 'Author email', context_variables, defaults)
        context_variables['current_year'] = str(datetime.datetime.now().year)

        user_input_list('template_type', 'the type of template', context_variables, defaults)

        if context_variables['template_type'] == 'documentation_only':
            context_variables['project_pypi_description'] = defaults['project_pypi_description']
            context_variables['addon_name'] = defaults['addon_name']
            context_variables['addon_description'] = defaults['addon_description']
            context_variables['addon_icon'] = defaults['addon_icon']
            context_variables['addon_window_details'] = defaults['addon_window_details']
            context_variables['demo_addon_class'] = defaults['demo_addon_class']
            context_variables['include_tests'] = "no"
        else:
            request_user_input('project_pypi_description', 'PyPI description', context_variables, defaults)
            request_user_input('addon_name', 'Seeq Add-on name', context_variables, defaults, use_defaults=False)
            request_user_input('addon_description', 'Seeq Add-on description', context_variables, defaults)
            request_user_input('addon_icon', 'Seeq Add-on icon', context_variables, defaults)
            request_user_input('addon_window_details', 'Seeq Add-on window details', context_variables, defaults)
            request_user_input('demo_addon_class', 'Name of the demo python class', context_variables, defaults)
            user_input_yes_or_no('include_tests', 'Include tests? (yes/no)', context_variables, defaults)

        print("\n")
        for k, v in context_variables.items():
            print(f"{k}: {v}")

        cookiecutter(str(DIRECTORY), no_input=True, extra_context=context_variables, **kwargs)

        print(f"'{context_variables['project_slug']}' project created successfully")


if __name__ == "__main__":
    main()
