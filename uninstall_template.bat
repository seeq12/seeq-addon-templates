@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
call variables.bat

call :RemoveFiles
call :RemoveFromPath

echo Press any key to exit
pause >nul

exit /b


:RemoveFiles
if exist "%DEST_DIR%" (
  echo Removing %DEST_DIR%
  rd /s /q "%DEST_DIR%"
  echo Successfully remove files in %DEST_DIR%
)
goto :eof


:: Function to remove a directory to the PATH
:RemoveFromPath
set "DIR_TO_REMOVE=%BIN_PATH%"

:: Get the current user path
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USER_PATH=%%B"

:: Check if the directory is already in the User Path
echo !USER_PATH! | find /I "%DIR_TO_REMOVE%" >nul
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
