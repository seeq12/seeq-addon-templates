@echo off
setlocal

REM Get the local directory (where the .bat file is located)
set "LOCAL_DIR=%~dp0"
set "VENV=%LOCAL_DIR%\.venv"
set "UTILS=%LOCAL_DIR%\{{project_name}}\_dev_tools\utils.py"

:CREATE_ENV
echo.
echo ********* Creating Virtual Environment **********************
echo   Creating virtual environment in %VENV%
python entrypoint.py
echo.
echo ************************************************************
echo.
echo Virtual environment created. To activate the environment, run:
echo.
echo   %VENV%\Scripts\activate
echo.
echo ************************************************************
goto :EOF

:ADDONENV
call :CREATE_ENV
goto :EOF
