@echo off

cd /d "%~dp0"

set "LOCAL_DIR=%~dp0"
set "ADDON_SCRIPT_PATH=%LOCAL_DIR%\addon.bat"
set "ADDON_VENV_FILE=%LOCAL_DIR%\addon_venv"
set "VARIABLES_FILE=%LOCAL_DIR%\variables.bat"

:: Destination directory
set "DEST_DIR=%USERPROFILE%\.sq-addon"
set "VENV=%DEST_DIR%\.venv"
set "ADDON_VENV_FILE_LOCAL_PATH=%DEST_DIR%\bin\addon_venv"
set "ADDON_SCRIPT_LOCAL_PATH=%DEST_DIR%\bin\addon.bat"
set "VARIABLES_FILE_LOCAL_PATH=%DEST_DIR%\bin\variables.bat"

set "BIN_PATH=%DEST_DIR%\bin"

