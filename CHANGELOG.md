# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Fixed

- Fixed generated add-on deploys by importing the `package(...)` function directly in
  `addon_template/_dev_tools/addon_tasks/deploy.py` instead of importing the module and
  calling it as a function. This restores `python addon.py deploy` for full-package installs
  and updates.
