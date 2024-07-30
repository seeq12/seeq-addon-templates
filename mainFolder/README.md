 
This is an example of the content that goes in the ReadMe file. We are trying to be as consistent as possible with 
the content of this file across SOSG (Seeq Open Source Gallery) projects since this is considered the "front-page" 
of the repository. That being said, feel free to change this file according to
your project needs.


<p >
  <a href="https://www.seeq.com" rel="nofollow">
    <img src="https://www.seeq.com/sites/default/files/seeq-content/seeq-logo-blue-web-33h.svg" alt="seeq" width="22%">
  </a>
</p>

<p align="center">
  <a href="https://seeq12.github.io/seeq-myoldaddon/index.html" rel="nofollow">
    <img src="https://seeq12.github.io/seeq-myoldaddon/_static/your_image.png" alt="add-on-catchy-image.png">
  </a>
</p>

----

**seeq-myoldaddon** is a Python module to ...

----

# Documentation

The documentation for **seeq-myoldaddon** can be found
[**here**](https://seeq12.github.io/seeq-myoldaddon/index.html).

----

# User Guide

[**seeq-myoldaddon User Guide**](https://seeq12.github.io/seeq-myoldaddon/user_guide.html)
provides a more in-depth explanation of .... Examples of typical types of analyses using **seeq-myoldaddon** can be
found in the section [Use Cases](https://seeq12.github.io/seeq-myoldaddon/examples.html).


-----

# Installation

The backend of **seeq-myoldaddon** requires **Python 3.7** or later.

## Dependencies

See [`requirements.txt`](https://github.com/seeq12/seeq-myoldaddon/tree/master/requirements.txt) file for a list of
dependencies and versions...

## User Installation Requirements (Seeq Data Lab)

...

## User Installation (Seeq Data Lab)

The latest build of the project can be found [here](https://pypi.org/project/seeq-myoldaddon/) as a wheel file. The
file is published as a courtesy to the user, and it does not imply any obligation for support from the publisher.

1. Create a **new** Seeq Data Lab project and open the **Terminal** window
2. Run `pip install seeq-myoldaddon`
3. Run `python -m <addon-name> [--users <users_list> --groups <groups_list>]`

----

# Development

We welcome new contributors of all experience levels. The **Development Guide** has detailed information about
contributing code, documentation, tests, etc.

## Important links

* Official source code repo: https://github.com/seeq12/seeq-myoldaddon
* Issue tracker: https://github.com/seeq12/seeq-myoldaddon/issues

## Source code

You can get started by cloning the repository with the command:

```shell
git clone git@github.com:seeq12/seeq-myoldaddon.git
```

## Installation from source

For development work, it is highly recommended creating a python virtual environment and install the package in that
working environment. If you are not familiar with python virtual environments, you can take a
look [here](https://docs.python.org/3.8/tutorial/venv.html)

Once your virtual environment is activated, you can install **seeq-myoldaddon** from source with:

```shell
python setup.py install
```

## Testing

There are several types of testing available for **seeq-myoldaddon**

### Automatic Testing

After installation, you can launch the test suite from the root directory of the project (i.e. `seeq-myoldaddon`
directory). You will need to have pytest >= 5.0.1 installed

To run all tests:

```shell
pytest
```

There are several pytest markers set up in the project. You can find the description of the marks in the `pytest.ini`
file. You can use the `-m` flag to run only a subset of tests. For example, to run only the `backend` tests, you can
use:

```shell
pytest -m backend
```

The integration tests requires a connection to a Seeq server. The tests are configured to try to access a local Seeq
server with the data directory set up in `ProgramData/Seeq/data` of the local drive. However, you can set the
`seeq_url`, `credentials_file` configuration options in the `test_config.ini` file to run the integration tests on a
remote Seeq server, or change the local seeq data directory with `data_dir`.

*Note:* Remember that the `seeq` module version in your local environment should match the Seeq server version

### User Interface Testing

To test the UI, use the `developer_notebook.ipynb` in the `development` folder of the project. This notebook can also be
used while debugging from your IDE. You can also create a whl first, install it on your virtual environment, and then
run `developer_notebook.ipynb` notebook there.

----

# Changelog

The changelog can be found [**here**](https://seeq12.github.io/seeq-myoldaddon/changelog.html)


----

# Support

Code related issues (e.g. bugs, feature requests) can be created in the
[issue tracker](https://github.com/seeq12/seeq-myoldaddon/issues)


----

# Citation

Please cite this work as:

```shell
seeq-myoldaddon
Seeq Corporation, 2024
https://github.com/seeq12/seeq-myoldaddon
```
