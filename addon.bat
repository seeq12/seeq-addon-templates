@echo off
setlocal enabledelayedexpansion

call %USERPROFILE%\.sq-addon\bin\variables.bat

REM Read the virtual environment path from a file
for /F "tokens=*" %%A in (%ADDON_VENV_FILE_LOCAL_PATH%) do (
    set "VENV=%%A"
    REM Trim trailing spaces by reassigning the value
    for /l %%B in (240,-1,0) do if "!VENV:~%%B,1!"==" " set "VENV=!VENV:~0,%%B!"
)

echo "%VENV%\Scripts\python"

REM Run the addon command with all passed arguments
"%VENV%\Scripts\python" "%VENV%\Scripts\addon.exe" %*
