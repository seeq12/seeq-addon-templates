# DATA LAB FUNCTIONS ELEMENT
A Data Lab Functions project is a multi-user project that is typically set up to handle Data Lab endpoints. [For more on Data Lab Functions](https://support.seeq.com/kb/latest/cloud/data-lab-functions-vs-data-lab-projects)

A Seeq Data Lab Functions endpoint has the following structure:
```
https://<my-seeq-server>/data-lab/<project-id>/functions/notebooks/<notebook_name>/endpoints/<endpoint_path>?<query_string>
```
For more on Data Lab Functions endpoints, see the [Invoking A Data Lab Functions REST API Endpoint](https://support.seeq.com/kb/latest/cloud/invoking-a-data-lab-functions-rest-api-endpoint) documentation.

This example contains the following endpoints:

- `GET /hello` - Returns a simple JSON response with a single message.
- `GET /view-querystring` - Returns the request querystring parameters as a JSON response.
- `POST /view-payload` - Returns the request body as a JSON response.
- `POST /combine` - Gets the signals `idA` and `idB` from the request body and the math operator `op`. Then it creates a Seeq formula and pushes the formula to Seeq. Finally, it updates the display pane to show the mathematical result of the math operation that acted on the two signals. Returns the status dataframe of a `spy.workbooks.push()` response.
- `POST /module-example/combine` - Same as `POST /combine` but with endpoint code located in a Python module.

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
   deployed to the Add-on Manager.
