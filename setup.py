# coding: utf-8
import re
from parver import Version, ParseError
import setuptools

# Use the following command from a terminal window to generate the whl with source code
# python setup.py bdist_wheel


with open("README.md", "r") as fh:
    long_description = fh.read()

version_scope = {'__builtins__': None}
with open("sq_addon_template/__init__.py", "r+") as f:
    version_file = f.read()
    version_line = re.search(r"__version__ = (.*)", version_file)
    if version_line is None:
        raise ValueError(f"Invalid version. Expected __version__ = 'xx.xx.xx', but got \n{version_file}")
    version = version_line.group(1).replace(" ", "").strip('\n').strip("'").strip('"')
    print(f"version: {version}")
    try:
        Version.parse(version)
        exec(version_line.group(0), version_scope)
    except ParseError as e:
        print(str(e))
        raise

# The metadata included here will be visible in PyPI if the artifact is published
setup_args = dict(
    name='sq-addon-template',
    version=version_scope['__version__'],
    author="Alberto Rivas",
    author_email="alberto.rivas@seeq.com",
    platforms=["Linux", "Windows"],
    description="Template to create Seeq Add-ons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seeq12/seeq-addons-templates",
    packages=['sq_addon_template'],
    package_dir={'sq_addon_template': 'sq_addon_template'},
    entry_points={'console_scripts': ['sq-addon-template = sq_addon_template.__main__:main']},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "cookiecutter>=1.7.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

setuptools.setup(**setup_args)
