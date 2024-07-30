import json
import re
import sys
import click
import datetime
from collections import OrderedDict
from pathlib import Path
import cookiecutter as cookie
from cookiecutter.main import cookiecutter
from sq_addon_templatess import __version__


NAME_REGEX = r'^[a-zA-Z][_a-zA-Z0-9]+$'
DIRECTORY = Path(__file__).parent.resolve()


def check_project_name(project_name):
    if not re.match(NAME_REGEX, project_name):
        print(f'ERROR: The project name "{project_name}" is not a valid module name for this template. '
              f'Name cannot start with a number or an underscore, and it cannot contain hyphens')
        return True


def request_user_input_text(variable, friendly_name, context_variables, defaults, use_defaults=True):
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


def request_user_input_options(variable, friendly_name, context_variables, defaults):
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



@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('create', required=False)
# @click.option(
#     '-c',
#     '--checkout',
#     help='branch, tag or commit to checkout after git clone',
# )
# @click.option(
#     '--replay',
#     is_flag=True,
#     help='Do not prompt for parameters and use information previously supplied',
# )
# @click.option(
#     '-f',
#     '--overwrite-if-exists',
#     is_flag=True,
#     help='Overwrite the contents of the output directory if it already exists',
# )
# @click.option(
#     '-s',
#     '--skip-if-file-exists',
#     is_flag=True,
#     help='Skip the files in the corresponding directories if they already exist',
#     default=False,
# )
@click.option(
    '-o',
    '--output-dir',
    default='.',
    type=click.Path(),
    help='Where to output the generated project dir into',
)
def main(
        create,
        # checkout,
        # replay,
        # overwrite_if_exists,
        # skip_if_file_exists,
        output_dir,
):
    """
    Template for creating an add-on project deployable on the Seeq Add-on Manager.

    An Add-on in the Add-on Manager is composed of ELEMENTS. There are four element types:
    `AddOnTool`, `Plugin`, `DataLabFunctions` and `FormulaPackage`. An Add-on must have at
    least one element, but it may have any combination of element types and any number
     of each element type.

    This template allows you to get started creating an add-on project with any combination
    of elements that you choose. However, the template is limited to create a maximum of one
    element per element type.
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
            # checkout=checkout,
            # replay=replay,
            # overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir,
            # skip_if_file_exists=skip_if_file_exists,
        )

        if kwargs.get('replay'):
            # Short-circuit everything and re-run with the information previously entered
            cookiecutter(DIRECTORY, **kwargs)
            print(f"'{context_variables.get('project_slug')}' project created successfully")
            return

        # defaults
        with open(Path.joinpath(DIRECTORY, "cookiecutter.json")) as f:
            defaults = json.load(f)

        error = True
        while error:
            request_user_input_text('project_name', 'Add-on project name', context_variables, defaults)
            error = check_project_name(context_variables['project_name'])

        context_variables['project_slug'] = f"{context_variables['project_name'].lower().replace(' ', '-')}"

        """
        project_identifier
        project_name
        project_description
        project_version
        project_maintainer
        project_license
        project_icon
        
        What element do you want to add? 
        1. AddOnTool
        2. Plugin
        3. DataLabFunctions
        4. FormulaPackage
        
        *** Assuming 1.AddOnTool is selected
        addon_tool_identifier:
        addon_tool_name:
        addon_tool_description:
        jupyter_notebook_file(relative path):
        Data Lab resource size:
        Jupyter extensions:
        add_on_tool_icon:
        add_on_tool_display_type["window", "tab", "none"]:
        add_on_tool_window_details:
        custom_configuration? (yes/no)[no]:
        ** if yes:
        configuration_filename:
        configuration_converter["json", "ini", "yaml", "toml"]:
        
        
        
        """






        request_user_input_options('project_license', 'project license', context_variables, defaults)

        request_user_input_text('author', 'Author', context_variables, defaults)
        request_user_input_text('author_email', 'Author email', context_variables, defaults)
        context_variables['current_year'] = str(datetime.datetime.now().year)

        request_user_input_options('template_type', 'the type of template', context_variables, defaults)

        if context_variables['template_type'] == 'documentation_only':
            context_variables['project_pypi_description'] = defaults['project_pypi_description']
            context_variables['addon_name'] = defaults['addon_name']
            context_variables['addon_description'] = defaults['addon_description']
            context_variables['addon_icon'] = defaults['addon_icon']
            context_variables['addon_window_details'] = defaults['addon_window_details']
            context_variables['demo_addon_class'] = defaults['demo_addon_class']
            context_variables['include_tests'] = "no"
        else:
            request_user_input_text('project_pypi_description', 'PyPI description', context_variables, defaults)
            request_user_input_text('addon_name', 'Seeq Add-on name', context_variables, defaults, use_defaults=False)
            request_user_input_text('addon_description', 'Seeq Add-on description', context_variables, defaults)
            request_user_input_text('addon_icon', 'Seeq Add-on icon', context_variables, defaults)
            request_user_input_text('addon_window_details', 'Seeq Add-on window details', context_variables, defaults)
            request_user_input_text('demo_addon_class', 'Name of the demo python class', context_variables, defaults)
            user_input_yes_or_no('include_tests', 'Include tests? (yes/no)', context_variables, defaults)

        print("\n")
        for k, v in context_variables.items():
            print(f"{k}: {v}")

        cookiecutter(str(DIRECTORY), no_input=True, extra_context=context_variables, **kwargs)

        print(f"'{context_variables['project_slug']}' project created successfully")


if __name__ == "__main__":
    main()
