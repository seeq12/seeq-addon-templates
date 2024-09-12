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

# Updates
To update the Add-on Example Generator, follow these steps:
1. Run `git checkout develop` in the root directory of the cloned repository to get the latest version of the Add-on 
   Example Generator.
2. Run `git pull` to update your local repository with the latest changes.
3. Run `./install_template` (Linux/Mac) or double-click on `install_template.bat` (Windows) to re-install the utility.

Once the installation is complete you can run `addon --help` from a terminal window (bash/zsh on Mac or Command
Prompt in Windows) to see the available commands.

# Usage
There are two main commands available in the Add-on Example Generator:
- `addon create` - This command generates a new Add-on project in the specified directory. 
- `addon update` - This command updates the Add-on project in the specified directory with the latest version of the 
  Add-on Example Generator and the updated answers from the user without recreating the existing virtual 
  environment.
- `addon --help` - This command displays the available commands and options. 

## Creating a new Add-on project
To create a new Add-on project, follow these steps:
1. Run `addon create <path/to/destination/folder>` from a terminal window.
2. Follow the prompts to answer the questions about the Add-on project.
3. Navigate to the destination folder and follow the instructions in the README.md file of your newly created Add-on 
   project.

### After creating your Add-on project
* Open the project in your favorite IDE to start developing your Add-on. VS Code is a good choice if you don't have 
  a favorite IDE. 
* The answers to your prompts are stored in the `.copier-answers.yml` file in the project folder. You can update the 
  answers by running `addon update <path/to/destination/folder>` from a terminal window.
* Open the README.md file in the project folder to get started with the Add-on project.
