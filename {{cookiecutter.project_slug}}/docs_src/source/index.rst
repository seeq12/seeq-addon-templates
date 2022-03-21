..
    documentation master file, created by
    sphinx-quickstart on Sun Oct 10 15:56:25 2021.
    However, it has been adapted for SOSG projects.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.

Welcome to {{cookiecutter.project_name|upper}} documentation
==============================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Introduction <introduction.md>
   Installation <installation.md>
   User Guide <user_guide.md>
   Use Cases <use_cases.md>
{%+ if cookiecutter.project_license == 'open-source' %}
   Code Documentation <docstrings.rst>
{% endif %}
   Changelog <changelog.md>
   License <license.md>
   Citation <citation.md>
{%+ if cookiecutter.project_license == 'open-source' %}
   View on GitHub <github.md>
{% endif %}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


