# Overview

An example visualization plugin using plain Javascript. It renders a form in the tool pane. This plugin uses a Data Lab Functions project for the backend calculations.

# Building

A running Seeq Server and an admin access key is a pre-requisite for plugin development. You'll need node.js installed globally.

First run "npm ci" to ensure you've installed the required packages.

Then run "npm run bootstrap" to fetch the latest sdk types and validate the admin credentials. You may be prompted to supply the url to the Seeq server and your access key.

From the example-plugin folder, you can do the following:

  **npm run watch**

      - watches for code changes and does the following:
        - development webpack build
        - create the plugin
        - uploads the plugin to your Seeq Server

  **npm run build**

      - production webpack build
      - create the plugin

  **npm run lint**

      - runs eslint
      - you can do `npm run lint -- --fix` to automatically fix issues if needed

 # SDK

 Once you've executed "npm run bootstrap", the Seeq plugin API can be referenced at the bottom of the sdk/seeq.d.ts file in the API interface.

 # Add-on manager
You can use the `addon.py` tools from the root directory:
1. Activate the virtual environment
	* If you are using a Terminal, you can activate the virtual environment by running `source .venv/bin/activate`
	  (Linux/Mac) or `.venv\Scripts\activate` (Windows).
	* If you are using an IDE, you can configure the IDE to use the virtual environment.
2. Run `python addon.py bootstrap --url https://<my-seeq-server> --username <username> --password <password> --dir <element_folder>` making
   sure you pass the correct URL, username, and password to your Seeq server.
3. Run `python addon.py build --dir <element_folder>` to build the `Plugin` elements in the Add-on package.
4. Run `python addon.py deploy` to deploy the Add-on package to the Add-on Manager.
5. Run `python addon.py watch --dir <element_folder>` to watch the element folder and make changes that dynamically deployed to the Add-on Manager
