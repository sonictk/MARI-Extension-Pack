@echo on
REM Batch script for deleting all python compiled files

echo. Removing all *.pyc files recursively from %~dp0...

cd "%~dp0"

del /s /q /f *.pyc
if errorlevel 1 exit /b 1

echo. Success!

:end

PAUSE
