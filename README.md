# Overview

This repository contains a templated project and utilities to generate packaged Add-on examples that are easily and 
quickly deployed into Seeq via the Add-on Manager. The example packaged Add-on can be used as a starting point for 
developing your own Add-ons.

# Prerequisites
The Add-on Example Generator requires the following software to be installed on your machine:
- Python 3.8 or later
- Node.js 21.7.3 or later

# Installation
To install the Add-on Example Generator, follow these steps:
1. Clone this repository to your local machine. (e.g. `git clone https://github.com/seeq12/seeq-addon-templates.git`)
2. Navigate to the root directory of the cloned repository.
3. Run `./install_template` (Linux/Mac) or double-click on `install_template.bat` (Windows) to install the utility.

Once the installation is complete you can run `addon --help` from a terminal window (bash/zsh on Mac or Command 
Prompt in Windows) to see the available commands.

# Usage
There are two main commands available in the Add-on Example Generator:
- `addon create` - This command generates a new Add-on project in the specified directory. 
- `addon update` - This command updates the Add-on project in the specified directory with the latest version of the 
  Add-on Example Generator and the updated answers from the user without recreating the already created virtual 
  environment.

## Creating a new Add-on project
To create a new Add-on project, follow these steps:
1. Run `addon create <path/to/destination/folder>` from a terminal window.
2. Follow the prompts to answer the questions about the Add-on project.
3. Navigate to the destination folder and follow the instructions in the README.md file of your newly created Add-on 
   project.

### Some things to keep in mind
* Open the project in your favorite IDE to start developing your Add-on. VS Code is a good choice if you don't have 
  a favorite IDE. 
* The Add-on Example Generator creates a virtual environment in the project folder. 
  * If you are using a Terminal, you can activate the virtual environment by running `source .venv/bin/activate` 
	(Linux/Mac) or `.venv\Scripts\activate` (Windows). 
  * If you are using an IDE, you can configure the IDE to use the virtual environment.
  * You will notice that the folder structure matches the elements you selected in the prompts with their 
	corresponding names.
  * You can also see that the `addon.json` configuration has been filled with the answers to the questions you 
	provided in the CLI. 
  * Finally, you will notice a `_dev_tools` folder that hosts all the utility functions that are helpful to develop,
	debug, package and deploy your Add-on. This folder is not meant to be manipulated, but you are welcome 
	to look inside for more complex configurations. 


# Developer notes
If you are interested in modifying the templates of this project, it can be time-consuming to install the template 
everytime you make a change. To make this process easier, follow these steps:

1. Install the template only the first time following the instructions in the **[Installation(#Installation)]** 
   section. 
2. Activate your virtual environment by running `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` 
   or from the IDE.
3. Make the changes to the templates of this project.
4. Test your changes by running `python addon_template/generate.py --help` from the root. For example, you can run 
   `python addon_template/generate.py create <path/to/destination/folder>` to test the `create` command.
