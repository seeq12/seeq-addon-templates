@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

call :CreateEnv
call :BuildProject
call :InstallProject
call :AddToPath
call :Info

echo Press any key to exit
pause >nul

exit /b


:CreateEnv
echo.
echo *************************************************************
echo   Creating virtual environment in %VENV%
echo Using shell: %COMSPEC%

if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
)

copy "%LOCAL_DIR%\requirements.txt" "%DEST_DIR%"

:: Check if python exists
where /q python
if %ERRORLEVEL% EQU 0 (
	python %LOCAL_DIR%\entrypoint.py
) else (
	echo Python is not installed. Please install Python and try again.
	exit /b 1
)
echo %VENV% > "%ADDON_VENV_FILE%"
goto :eof


:BuildProject
echo *************************************************************
if exist "%VENV%\Scripts\python.exe" (
    "%VENV%\Scripts\python.exe" -m build 2> NUL
    if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%
    )
else (
    exit /b
)
echo Build successful
goto :eof


:InstallProject
echo *************************************************************
echo Installing seeq-addon-template project
for /f "tokens=2 delims==" %%a in ('findstr /C:"version = " %LOCAL_DIR%pyproject.toml') do (
    set "version=%%~a"
    set "version=!version:"=!"
	for /f "tokens=* delims= " %%b in ("!version!") do set "version=%%b"
)
:: Check the ERRORLEVEL after set
if !ERRORLEVEL! NEQ 0 (
	echo Error: Couldn't find version from pyproject.toml.
	pause
	exit /b !ERRORLEVEL!
) else (
	echo "seeq-addon-template version: %version%"
)

echo Installing in python environment
"%VENV%\Scripts\pip.exe" install "%LOCAL_DIR%dist\addon-%version%-py3-none-any.whl" --force-reinstall > NUL

IF NOT EXIST "%BIN_PATH%" (
    echo Creating directory %BIN_PATH%
    mkdir "%BIN_PATH%"
)

echo Copying files to %BIN_PATH%
copy "%ADDON_SCRIPT_PATH%" "%ADDON_SCRIPT_LOCAL_PATH%"
copy "%ADDON_VENV_FILE%" "%ADDON_VENV_FILE_LOCAL_PATH%"
copy "%VARIABLES_FILE%" "%VARIABLES_FILE_LOCAL_PATH%"
goto :eof


:: Function to add a directory to the PATH
:AddToPath
set "DIR_TO_ADD=%BIN_PATH%"

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
echo Installation complete
echo Run `addon --help` to see the available options
echo.
echo For example, to create an example Add-on, run the command
echo   addon create <destination_dir>
echo \n************************************************************
goto :eof
