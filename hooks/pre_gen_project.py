"""
Context variables can be modified here. However, there are restrictions. Modifying the project_slug doesn't work
since the value is required to first create the directory.

{{ cookiecutter.update({"project_slug": cookiecutter.project_slug }) }}
"""
import sys

docs_only = True if '{{ cookiecutter.template_type }}' == 'documentation only' else False
addon_class = '{{ cookiecutter.demo_addon_class}}'
addon_name = '{{ cookiecutter.addon_name }}'
addon_description = '{{ cookiecutter.addon_description }}'


if not docs_only:

    if not addon_class:
        print(f"ERROR: demo_addon_class nane is required. This is the name of the addon main class")
        sys.exit(1)

    if not addon_name:
        print(f"ERROR: addon name is required")
        sys.exit(1)

    if not addon_description:
        print(f"ERROR: addon description is required")
        sys.exit(1)



