# coding: utf-8
{% if cookiecutter.project_license == 'sosg' -%}
import re
from parver import Version, ParseError
import setuptools

# Use the following command from a terminal window to generate the whl with source code
# python setup.py bdist_wheel

namespace = 'seeq.*'

with open("README.md", "r") as fh:
    long_description = fh.read()

version_scope = {'__builtins__': None}
with open("seeq/addons/{{cookiecutter.project_name}}/_version.py", "r+") as f:
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
    name='{{cookiecutter.project_slug}}',
    version=version_scope['__version__'],
    author="{{cookiecutter.author}}",
    author_email="{{cookiecutter.author_email}}",
    license='Apache License 2.0',
    platforms=["Linux", "Windows"],
    description="{{cookiecutter.project_description}}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seeq12/{{cookiecutter.project_slug}}",
    packages=setuptools.find_namespace_packages(include=[namespace]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ipywidgets>=7.6.3",
        'ipyvuetify>=1.5.1',
        'numpy>=1.19.5',
        'pandas>=1.2.1',
        'plotly>=4.5.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

setuptools.setup(**setup_args)

{% elif cookiecutter.project_license == 'marketplace' %}
import sys
import re
import pkgutil
import shutil
from distutils.dir_util import copy_tree
from pathlib import Path
from parver import Version, ParseError

import setuptools
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from setuptools.extension import Extension


# Use the following command from a terminal window to generate the whl with source code
# python setup.py bdist_wheel
# Use the following command from a terminal window to generate the whl containing only binaries
# python setup.py bdist_wheel --binary

namespace = 'seeq.*'


class MyBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent
        target_dir = build_dir if not self.inplace else root_dir

        packages = setuptools.find_namespace_packages(include=[namespace])
        package_paths = [x.replace(".", "/") for x in packages]

        for path in package_paths:
            self.copy_file(Path(path) / '__init__.py', root_dir, target_dir)
            self.copy_file(Path(path) / '__main__.py', root_dir, target_dir)

        with open("MANIFEST.in", "r") as fh:
            manifest = fh.readlines()

        paths_to_copy = [Path(line.strip("graft ").strip("\n")) for line in manifest if 'graft' in line]
        for path in paths_to_copy:
            self.copy_directory(path, root_dir, target_dir)

    @staticmethod
    def copy_file(path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return
        shutil.copyfile(str(source_dir / path), str(destination_dir / path))

    @staticmethod
    def copy_directory(path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return
        copy_tree(str(source_dir / path), str(destination_dir / path))


def build_extensions():
    packages = setuptools.find_namespace_packages(include=[namespace])
    sources = []
    for package in packages:
        path = package.replace(".", "/")
        modules = [name for importer, name, ispkg in pkgutil.iter_modules([path]) if not ispkg and name != '__main__']
        sources.extend(["".join([path, "/", module, '.py']) for module in modules])
    names = [source.split(".")[0].replace("/", ".") for source in sources]
    return [Extension(name, [source]) for name, source in zip(names, sources)]


with open("README.md", "r") as fh:
    long_description = fh.read()

version_scope = {'__builtins__': None}
with open("seeq/addons/{{cookiecutter.project_name}}/_version.py", "r+") as f:
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

setup_args = dict(
    name='{{cookiecutter.project_slug}}',
    version=version_scope['__version__'],
    author="{{cookiecutter.author}}",
    author_email="{{cookiecutter.author_email}}",
    # license="No license offered",
    platforms=["Linux", "Windows"],
    description="{{cookiecutter.project_description}}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_namespace_packages(include=[namespace]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ipywidgets>=7.6.3",
        'ipyvuetify>=1.5.1',
        'numpy>=1.19.5',
        'pandas>=1.2.1',
        'plotly>=4.5.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        # "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

if '--binary' in sys.argv:
    setup_args.update(
        dict(
            ext_modules=cythonize(
                build_extensions(),
                build_dir="build",
                compiler_directives=dict(always_allow_keywords=True,
                                         language_level='3')),
            cmdclass=dict(build_ext=MyBuildExt),
            packages=[]
        ),
    )
    sys.argv.remove('--binary')

setuptools.setup(**setup_args)
{% endif %}