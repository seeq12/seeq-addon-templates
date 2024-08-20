@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"

set "LOCAL_DIR=%~dp0"
set "VENV=%LOCAL_DIR%.venv"
set "ADDON_VENV_FILE=%LOCAL_DIR%\addon_venv"
set "ADDON_TEMPLATE_FOLDER=seeqAddonsTemplate"

call :RemoveFromPath

if exist "%ADDON_VENV_FILE%" del %ADDON_VENV_FILE%
if exist "%VENV%" rd /s /q %VENV%
if exist "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%" rd /s /q "%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%"
pause
exit /b


:: Function to add a directory to the PATH
:RemoveFromPath
set "DIR_TO_REMOVE=%USERPROFILE%\%ADDON_TEMPLATE_FOLDER%"

for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%B"

:: Check if the directory is in the User Path
echo !USER_PATH! | findstr /I /C:"%DIR_TO_REMOVE%" >nul

if !ERRORLEVEL! EQU 0 (

	set "NEW_PATH=!USER_PATH:%DIR_TO_REMOVE%=!"
	if "!NEW_PATH:~0,1!"==";" set "NEW_PATH=!NEW_PATH:~1!"
    reg add "HKCU\Environment" /v Path /t REG_EXPAND_SZ /d "!NEW_PATH!" /f
	setx Path "!NEW_PATH!"
	echo %DIR_TO_REMOVE% has been removed from your PATH

) else (
	echo User path is clean
)

goto :eof
