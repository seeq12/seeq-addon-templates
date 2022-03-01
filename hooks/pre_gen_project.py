"""
Context variables can be modified here. However, there are restrictions. Modifying the project_slug doesn't work
since the value is required to first create the directory.

{{ cookiecutter.update({"project_slug": cookiecutter.project_slug }) }}
"""

import re
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).parent.parent.resolve()


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

project_name = '{{ cookiecutter.project_name}}'
docs_only = True if '{{ cookiecutter.documentation_only }}' == 'y' else False
addon_class = '{{ cookiecutter.camelcase_addon_class}}'
addon_name = '{{ cookiecutter.addon_name }}'
addon_description = '{{ cookiecutter.addon_description }}'

if not re.match(MODULE_REGEX, project_name):
    print(f'ERROR: The project name "{project_name}" is not a valid Python module name. '
          f'Please do not use a hyphen and use an underscore instead. Name cannnot start with a number either.')
    # Exit to cancel project
    sys.exit(1)

if 'seeq' in project_name.lower():
    print(f'ERROR: "seeq" cannot be part of the project name.')
    # Exit to cancel project
    sys.exit(1)

if not docs_only:

    if not addon_class:
        print(f"ERROR: camelcase_addon_class nane is required. This is the name of the addon main class")
        sys.exit(1)

    if not addon_name:
        print(f"ERROR: addon name is required")
        sys.exit(1)

    if not addon_description:
        print(f"ERROR: addon description is required")
        sys.exit(1)



