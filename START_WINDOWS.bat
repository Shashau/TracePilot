@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto usepython
py -3.12 -c "import sys; assert sys.maxsize > 2**32" >nul 2>nul
if errorlevel 1 goto usepython
py -3.12 bootstrap.py %*
goto finished
:usepython
python -c "import sys; assert sys.version_info[:2] == (3,12) and sys.maxsize > 2**32" >nul 2>nul
if errorlevel 1 goto missing
python bootstrap.py %*
goto finished
:missing
echo Install Python 3.12 64-bit from python.org, then run this file again.
echo During installation, select Add Python to PATH and the Python launcher.
echo Extract the entire ZIP first. Do not run from inside the compressed folder.
pause
exit /b 1
:finished
if errorlevel 1 (
  echo.
  echo TracePilot stopped with an error. Read the message above.
  pause
  exit /b 1
)
endlocal
