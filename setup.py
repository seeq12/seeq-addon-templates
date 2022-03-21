# coding: utf-8
print('hello')


# import re
# from parver import Version, ParseError
# import setuptools
#
# # Use the following command from a terminal window to generate the whl with source code
# # python setup.py bdist_wheel
#
# namespace = 'seeq.*'
#
# with open("README.md", "r") as fh:
#     long_description = fh.read()
#
# version_scope = {'__builtins__': None}
# with open("seeq/addons/my-open-source-app/_version.py", "r+") as f:
#     version_file = f.read()
#     version_line = re.search(r"__version__ = (.*)", version_file)
#     if version_line is None:
#         raise ValueError(f"Invalid version. Expected __version__ = 'xx.xx.xx', but got \n{version_file}")
#     version = version_line.group(1).replace(" ", "").strip('\n').strip("'").strip('"')
#     print(f"version: {version}")
#     try:
#         Version.parse(version)
#         exec(version_line.group(0), version_scope)
#     except ParseError as e:
#         print(str(e))
#         raise
#
# # The metadata included here will be visible in PyPI if the artifact is published
# setup_args = dict(
#     name='seeq-my-open-source-app',
#     version=version_scope['__version__'],
#     author="",
#     author_email="",
#     license='Apache License 2.0',
#     platforms=["Linux", "Windows"],
#     description="MyAddOnClassName",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/seeq12/seeq-my-open-source-app",
#     packages=setuptools.find_namespace_packages(include=[namespace]),
#     include_package_data=True,
#     zip_safe=False,
#     install_requires=[
#         "ipywidgets>=7.6.3",
#         'ipyvuetify>=1.5.1',
#         'numpy>=1.19.5',
#         'pandas>=1.2.1',
#         'plotly>=4.5.0',
#     ],
#     classifiers=[
#         "Programming Language :: Python :: 3.7",
#         "License :: OSI Approved :: Apache Software License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.7',
# )
#
# setuptools.setup(**setup_args)
#
