@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1

where py >nul 2>nul
if errorlevel 1 goto install_python
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto install_python
goto python_ready

:install_python
where winget >nul 2>nul
if errorlevel 1 goto python_required
echo Python 3.10 or newer is required. Starting a one-time user-scope Python 3.13 installation...
winget install --id Python.Python.3.13 --exact --scope user --accept-source-agreements
if errorlevel 1 goto python_required
where py >nul 2>nul
if errorlevel 1 goto restart_launcher
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
if errorlevel 1 goto restart_launcher

:python_ready
if not exist ".venv\Scripts\python.exe" (
  echo Setting up the PDF Naming Assistant...
  py -3 -m venv .venv
  if errorlevel 1 goto setup_failed
)

".venv\Scripts\python.exe" -c "import importlib.metadata as m; assert m.version('pypdf') == '6.19.0' and m.version('python-dotenv') == '1.2.4'" >nul 2>nul
if errorlevel 1 (
  echo Installing the pinned Python dependencies or correcting their versions...
  ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
  if errorlevel 1 goto setup_failed
)

".venv\Scripts\python.exe" backend\launcher.py
set APP_EXIT_CODE=%ERRORLEVEL%
pause
exit /b %APP_EXIT_CODE%

:python_required
echo Python 3.10 or newer is required. Install it from https://www.python.org/downloads/windows/ and try again.
start "" "https://www.python.org/downloads/windows/"
pause
exit /b 1

:restart_launcher
echo Python was installed, but this window cannot find it yet. Close this window, then double-click the launcher again.
pause
exit /b 1

:setup_failed
echo Setup or model startup failed. Review the message above, fix the issue, then try again.
pause
exit /b 1
