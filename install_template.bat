@echo off
setlocal

REM Get the local directory (where the script is located)
set "LOCAL_DIR=%~dp0"
set "VENV=%LOCAL_DIR%\.venv"
set "ADDON_SCRIPT_PATH=%LOCAL_DIR%\addon"
set "ADDON_VENV_FILE=%LOCAL_DIR%\addon_venv"

REM Function to create a virtual environment
:CreateEnv
echo.
echo ********* Creating Virtual Environment **********************
echo   Creating virtual environment in %VENV%
echo Using shell: %COMSPEC%
REM Check if python exists
where /q python
if %ERRORLEVEL% EQU 0 (
    python entrypoint.py
) else (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)
echo.
echo ************************************************************
echo.
echo Virtual environment created
echo.
echo ************************************************************
echo.
goto :eof

:Info
echo.
echo ************************************************************
echo.
echo  To generate your example add-on, run the command
echo.
echo    addon create <destination_dir>
echo.
echo ************************************************************
goto :eof

REM Call the function
call :CreateEnv

REM Write the path of the virtual environment to a file
echo %VENV% > "%ADDON_VENV_FILE%"

"%VENV%"\Scripts\python -m build

for /f "tokens=2 delims==" %%a in ('findstr /R "version = " pyproject.toml') do set "version=%%~a"
echo seeq-addon-template version: %version%

"%VENV%"\Scripts\pip install dist\addon-%version%-py3-none-any.whl -U

copy "%ADDON_SCRIPT_PATH%" %SystemRoot%\System32\addon
copy "%ADDON_VENV_FILE%" %SystemRoot%\System32\addon_venv

call :Info
