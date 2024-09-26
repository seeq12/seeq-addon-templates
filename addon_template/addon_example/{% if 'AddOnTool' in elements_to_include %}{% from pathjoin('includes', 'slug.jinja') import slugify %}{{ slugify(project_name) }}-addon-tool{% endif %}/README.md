# Add-on tool element example

This is an example of an Add-on Tool element with multiple files. In this example, the Add-on Tool is deployed with a
target Jupyter notebook `addon_tool_example_target_notebook.ipynb`. The target Jupyter notebook imports the local 
package `my_addon_tool_example` which contains a UI developed with `ipyvuetify` and the backend.


# Interacting with Add-on manager
You can use the `addon.py` tools from the root directory:
1. Activate the virtual environment
	* If you are using a Terminal, you can activate the virtual environment by running `source .venv/bin/activate`
	  (Linux/Mac) or `.venv\Scripts\activate` (Windows).
	* If you are using an IDE, you can configure the IDE to use the virtual environment.
2. Run `python addon.py bootstrap --global-python-env . --url https://<my-seeq-server> --username <username> 
   --password <password> --dir <element_folder>` making sure you pass the correct URL, username, and password to 
   your Seeq server. You only need to run this command if you are adding dependencies to the `requirements.txt` file.
3. Run `python addon.py deploy` to deploy the Add-on package to the Add-on Manager.
4. Run `python addon.py watch --dir <element_folder>` to watch the element folder and make changes that dynamically 
   deployed to the Add-on Manager
