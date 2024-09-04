# Welcome to the {{ project_name }} packaged Add-on project!

This project includes the following Add-on elements:
{% if 'AddOnTool' in elements_to_include %}- {{ project_name }}{% endif %}
{% if 'DataLabFunctions' in elements_to_include %}- {{ project_name }} Data Lab Functions {% endif %}
{% if 'Plugin' in elements_to_include %}- {{ project_name }} Plugin {% endif %}
{% if 'ToolPanePlugin' in elements_to_include %}- {{ project_name }} Tool Pane Plugin {% endif %}
{% if 'FormulaPackage' in elements_to_include %}- {{ project_name }} Formula Package {% endif %}

## If this project was created by the [Add-on Example Generator](https://github.com/seeq12/seeq-addon-templates.git):
* The Add-on Example Generator creates a virtual environment in the project folder. 
* You will notice that the folder structure matches the elements you selected in the prompts of the Add-on Example 
  Generator with their corresponding names. 
* You can also see that the `addon.json` configuration has been filled with the answers to the questions you 
  provided in the CLI. 
* Finally, you will notice a `_dev_tools` folder that hosts all  he utility functions that are helpful to develop, 
  debug, package and deploy your Add-on. This folder is not meant to be manipulated, but you are welcome to look 
  inside for more complex configurations.

  
# Getting Started
To deploy your Add-on package example to Add-on Manager, follow the steps below:
1. Activate the virtual environment 
   * If you are using a Terminal, you can activate the virtual environment by running `source .venv/bin/activate` 
	  (Linux/Mac) or `.venv\Scripts\activate` (Windows). 
   * If you are using an IDE, you can configure the IDE to use the virtual environment.
{% if 'Plugin' in elements_to_include or 'ToolPanePlugin' in elements_to_include %}
2. Run `python addon.py bootstrap --url https://<my-seeq-server> --username <username> --password <password>` making 
   sure you pass the correct URL, username, and password to your Seeq server.
3. Run `python addon.py build` to build the `Plugin` elements in the Add-on package.
4. Run `python addon.py deploy` to deploy the Add-on package to the Add-on Manager.
{% else %}
2. Run `python addon.py deploy --url https://<my-seeq-server> --username <username> --password <password>` making
   sure you pass the correct URL, username, and password to your Seeq server.
{% endif %}