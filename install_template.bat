@echo off
setlocal enabledelayedexpansion

:: Get the local directory (where the script is located)
set "LOCAL_DIR=%~dp0"
set "VENV=%LOCAL_DIR%.venv"
set "ADDON_SCRIPT_PATH=%LOCAL_DIR%\addon.bat"
set "ADDON_VENV_FILE=%LOCAL_DIR%\addon_venv"
set "ADDON_TEMPLATE_FOLDER=seeqAddonsTemplate"

:: Create a virtual environment
call :CreateEnv

:: Write the path of the virtual environment to a file

echo %VENV% > "%ADDON_VENV_FILE%"

if exist "%ADDON_VENV_FILE%" ("%VENV%\Scripts\python.exe" -m build) else (exit /b)

for /f "tokens=2 delims==" %%a in ('findstr /C:"version = " pyproject.toml') do (
	echo %%a
    set "version=%%~a"
    set "version=!version:"=!"
	for /f "tokens=* delims= " %%b in ("!version!") do set "version=%%b"
)
echo "seeq-addon-template version: %version%"

"%VENV%\Scripts\pip.exe" install "dist\addon-%version%-py3-none-any.whl" --force-reinstall


mkdir "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%"
copy "%ADDON_SCRIPT_PATH%" "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%\addon.bat"
copy "%ADDON_VENV_FILE%" "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%\addon_venv"

call :AddToPath
call :Info

echo Press any key to exit
pause >nul


:: Function to create a virtual environment
:CreateEnv
echo.
echo ********* Creating Virtual Environment **********************
echo   Creating virtual environment in %VENV%
echo Using shell: %COMSPEC%
:: Check if python exists
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

:: Function to add a directory to the PATH
:AddToPath
set "DIR_TO_ADD=%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%"

REM Check if the directory is already in the PATH
echo %PATH% | findstr /I /C:"%DIR_TO_ADD%" >nul

REM If the directory is not in the PATH, add it
if %ERRORLEVEL% NEQ 0 (
    setx /M PATH "%PATH%;%DIR_TO_ADD%"
    echo %DIR_TO_ADD% added to PATH
) else (
    echo %DIR_TO_ADD% is already in the PATH
)

goto :eof


:Info
echo.
echo ************************************************************
echo.
echo  To generate your example add-on, run the command
echo.
echo    addon create "<destination_dir>"
echo.
echo ************************************************************
goto :eof
