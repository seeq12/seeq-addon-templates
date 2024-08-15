@echo off
setlocal

set "ADDON_VENV_FILE=%SystemRoot%\System32\addon_venv"

REM Read the virtual environment path from a file
for /F "tokens=*" %%A in (%ADDON_VENV_FILE%) do set "VENV=%%A"

REM Run the addon command with all passed arguments
"%VENV%"\Scripts\python "%VENV%"\Scripts\addon %*
