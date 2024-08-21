#!/bin/bash

# Get the local directory (where the script is located)

LOCAL_DIR="$(pwd)"
export LOCAL_DIR
export VENV="$LOCAL_DIR/.venv"
export ADDON_SCRIPT_PATH="$LOCAL_DIR/addon"
export ADDON_VENV_FILE="$LOCAL_DIR/addon_venv"


export ADDON_VENV_FILE_LOCAL_PATH="$HOME/.local/bin/addon_venv"
export ADDON_SCRIPT_LOCAL_PATH="$HOME/.local/bin/addon"

export PATH_START_MARKER="### MANAGED BY seeq-addon-template (DO NOT EDIT)"
export PATH_END_MARKER="### END MANAGED BY seeq-addon-template (DO NOT EDIT)"

export ADD_TO_PATH="$PATH_START_MARKER
export PATH=\"$HOME/.local/bin:\$PATH\"
$PATH_END_MARKER"
