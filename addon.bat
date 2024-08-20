@echo off
setlocal enabledelayedexpansion

set "ADDON_TEMPLATE_FOLDER=seeqAddonsTemplate"
set "ADDON_VENV_FILE=%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%\addon_venv"
echo %ADDON_VENV_FILE%

REM Read the virtual environment path from a file
for /F "tokens=*" %%A in (%ADDON_VENV_FILE%) do (
    set "VENV=%%A"
    REM Trim trailing spaces by reassigning the value
    for /l %%B in (240,-1,0) do if "!VENV:~%%B,1!"==" " set "VENV=!VENV:~0,%%B!"
)

echo "%VENV%\Scripts\python"

REM Run the addon command with all passed arguments
"%VENV%\Scripts\python" "%VENV%\Scripts\addon.exe" %*
