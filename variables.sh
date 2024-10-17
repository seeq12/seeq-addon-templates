#!/bin/bash

# Get the local directory (where the script is located)
LOCAL_DIR="$(pwd)"

if [[ "$(uname)" == "MINGW"* ]] || [[ "$(uname)" == "CYGWIN"* ]] || [[ "$(uname)" == "MSYS"* ]]; then
    OS="Windows"
else
    OS="NotWindows"
fi

export LOCAL_DIR
export ADDON_VENV_FILE="$LOCAL_DIR/addon_venv"

# Destination directory
export DEST_DIR="$HOME/.sq-addon"
export VENV="$DEST_DIR/.venv"
export ADDON_VENV_FILE_LOCAL_PATH="$DEST_DIR/bin/addon_venv"

if [[ "$OS" == "Windows" ]]; then
  export ADDON_SCRIPT_PATH="$LOCAL_DIR/addon.bat"
  export VARIABLES_FILE="$LOCAL_DIR/variables.bat"
  export ADDON_SCRIPT_LOCAL_PATH="$DEST_DIR/bin/addon.bat"
  export VARIABLES_FILE_LOCAL_PATH="$DEST_DIR/bin/variables.bat"
else
  export ADDON_SCRIPT_PATH="$LOCAL_DIR/addon"
  export VARIABLES_FILE="$LOCAL_DIR/variables.sh"
  export ADDON_SCRIPT_LOCAL_PATH="$DEST_DIR/bin/addon"
  export VARIABLES_FILE_LOCAL_PATH="$DEST_DIR/bin/variables.sh"
fi

export PATH_START_MARKER="### MANAGED BY seeq-addon-template (DO NOT EDIT)"
export PATH_END_MARKER="### END MANAGED BY seeq-addon-template (DO NOT EDIT)"

export ADD_TO_PATH="$PATH_START_MARKER
export PATH=\"$DEST_DIR/bin:\$PATH\"
$PATH_END_MARKER"
