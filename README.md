**sq_addon_template** is a python tool to help you get started creating a new Seeq add-on (either as an open-source 
or as a marketplace project). 

# Basic Usage
This is a CLI (Command Line Interface) application. Thus, you will use it from your favorite terminal. You need these 
main steps to run the **sq-addon-template** tool.

1. **Get the wheel file.** You can download the latest wheel file from the [latest release](https://github.com/seeq12/seeq-addons-templates/releases/).
Alternatively, you can clone the repository and build your own wheel file running `python setup.py bdist_wheel` at 
the root directory of the repository. 
2. **Install sq-addon-template.** Once you have the wheel file, install the **sq-addon-template** tool on your python 
   virtual environment with `pip install <whl file>`
3. **Run the tool**. Now you are ready to use **sq-addon-template**. The first thing to try is running 
   `sq-addon-template help` which displays the help of the tool. Next, try with `sq-addon-template create` and 
   create your new project!

