# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../..'))
from seeq.addons import {{cookiecutter.project_name}}

# -- Project information -----------------------------------------------------

project = '{{cookiecutter.project_slug}}'
copyright = '{{cookiecutter.current_year}}, Seeq Corporation'
author = '{{cookiecutter.author}}'

# The full version, including alpha/beta/rc tags
version = {{cookiecutter.project_name}}.__version__
release = {{cookiecutter.project_name}}.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.githubpages',
    'sphinx.ext.viewcode',
    'myst_parser'
]
napoleon_google_docstring = False
napoleon_numpy_docstring = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'sphinxdoc'
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_favicon = '_static/seeq-favicon.ico'

{% if cookiecutter.project_license == 'sosg' -%}
html_logo = '_static/Seeq_logo_darkBlue_sm.png'

# # These paths are either relative to html_static_path
# # or fully qualified paths (eg. https://...)
# html_css_files = [
#     'css/style.css',
# ]
#
# html_style = 'css/style.css'

{% elif cookiecutter.project_license == 'marketplace' %}
html_logo = '_static/Seeq_logo_darkPurple_sm.png'
# html_logo = '_static/Seeq_logo_white_sm.png'

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

# This will completely replace the theme stylesheet
# html_style = 'css/yourtheme.css'

html_theme_options = {
    'style_external_links': True,
    'style_nav_header_background': '#e3e3e3',
}

{% endif %}
