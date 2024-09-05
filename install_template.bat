@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "LOCAL_DIR=%~dp0"
set "ADDON_SCRIPT_PATH=%LOCAL_DIR%\addon.bat"
set "ADDON_VENV_FILE=%LOCAL_DIR%\addon_venv"

set "ADDON_TEMPLATE_FOLDER=seeqAddonsTemplate"
set "VENV=%ADDON_TEMPLATE_FOLDER%\.venv"

call :CreateEnv

echo %VENV% > "%ADDON_VENV_FILE%"

if exist "%ADDON_VENV_FILE%" ("%VENV%\Scripts\python.exe" -m build) else (exit /b)

for /f "tokens=2 delims==" %%a in ('findstr /C:"version = " %LOCAL_DIR%pyproject.toml') do (
    set "version=%%~a"
    set "version=!version:"=!"
	for /f "tokens=* delims= " %%b in ("!version!") do set "version=%%b"
)

:: Check the ERRORLEVEL after setx
if !ERRORLEVEL! NEQ 0 (
	echo Error: Couldn't find version from pyproject.toml.
	pause
	exit /b !ERRORLEVEL!
) else (
	echo "seeq-addon-template version: %version%"
)


"%VENV%\Scripts\pip.exe" install "%LOCAL_DIR%dist\addon-%version%-py3-none-any.whl" --force-reinstall


mkdir "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%"
copy "%ADDON_SCRIPT_PATH%" "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%\addon.bat"
copy "%ADDON_VENV_FILE%" "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%\addon_venv"

call :AddToPath
call :Info

echo Press any key to exit
pause >nul

exit /b


:: Function to create a virtual environment
:CreateEnv
echo.
echo ********* Creating Virtual Environment **********************
echo   Creating virtual environment in %VENV%
echo Using shell: %COMSPEC%
:: Check if python exists
where /q python
if %ERRORLEVEL% EQU 0 (
	python %LOCAL_DIR%\entrypoint.py
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

for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%B"

:: Check if the directory is already in the User Path
echo !USER_PATH! | findstr /I /C:"%DIR_TO_ADD%" >nul

if !ERRORLEVEL! EQU 0 (
    echo %DIR_TO_ADD% is already in the User Path
) else (
    set "NEW_PATH=!USER_PATH!;%DIR_TO_ADD%"
    reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!NEW_PATH!" /f
    echo %DIR_TO_ADD% has been added to the User Path
	setx Path "!NEW_PATH!"
)

goto :eof


:Info
echo.
echo ************************************************************
echo.
echo  Installation complete
echo.
echo  Run `addon --help` to see the available options
echo.
echo  For example, to create an example Add-on, run the command
echo     addon create <destination_dir>
echo \n************************************************************
goto :eof
