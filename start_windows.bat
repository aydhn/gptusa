@echo off
setlocal EnableDelayedExpansion

echo ========================================================
echo USA Signal Bot - Windows Startup Orchestrator
echo ========================================================

:: 1. Check Root Directory
if not exist "usa_signal_bot" (
    echo [ERROR] Must be run from the repository root directory.
    pause
    goto :EOF
)

:: 2. Check Python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    goto :EOF
)

:: 3 & 4. Check/Create virtualenv
if not exist ".venv" (
    echo [INFO] Creating virtual environment (.venv)...
    python -c "import venv; venv.create('.venv', with_pip=True)"
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        goto :EOF
    )
)

:: 5 & 6. Verify and Use .venv
set "PYTHON_EXE=.venv\Scripts\python.exe"
if not exist "!PYTHON_EXE!" (
    echo [ERROR] Virtual environment is corrupted. Deleting and recreating...
    rmdir /s /q .venv
    python -c "import venv; venv.create('.venv', with_pip=True)"
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to recreate virtual environment.
        pause
        goto :EOF
    )
)

:: 7. Update pip, setuptools, wheel
echo [INFO] Updating pip, setuptools, and wheel...
"!PYTHON_EXE!" -m pip install --upgrade pip setuptools wheel >nul 2>&1

:: 8 & 9. Install Dependencies
echo [INFO] Checking dependencies...
if exist "requirements.txt" (
    "!PYTHON_EXE!" -m pip install -r requirements.txt >nul 2>&1
)
:: Also install the project itself in editable mode so imports work
if exist "setup.py" (
    "!PYTHON_EXE!" -m pip install -e . >nul 2>&1
)

:: 10 & 11. Env/Config Wizard (basic)
if not exist "config\runtime.env" (
    echo [INFO] Missing config\runtime.env, creating template...
    if not exist "config" mkdir config
    echo # Runtime configuration > config\runtime.env
    echo RUNTIME_MODE=PAPER >> config\runtime.env
    echo # Add your API keys here >> config\runtime.env
    echo [WARN] Please configure config\runtime.env before production use.
)

:: 13. Ensure .gitignore excludes
findstr /C:".venv" .gitignore >nul 2>&1
if !errorlevel! neq 0 echo .venv>> .gitignore
findstr /C:"logs/" .gitignore >nul 2>&1
if !errorlevel! neq 0 echo logs/>> .gitignore
findstr /C:".env" .gitignore >nul 2>&1
if !errorlevel! neq 0 echo *.env>> .gitignore

:: Setup logs
if not exist "logs" mkdir logs
echo [INFO] Starting logs at logs\windows_startup.log
echo Startup Sequence Started > logs\windows_startup.log

:: 14 & 15. Tests and Healthcheck
echo [INFO] Running pre-flight smoke tests...
"!PYTHON_EXE!" -m pytest tests/test_smoke.py >> logs\windows_startup.log 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Smoke tests failed. See logs\windows_startup.log
    pause
    goto :EOF
)

echo [INFO] Running healthchecks...
"!PYTHON_EXE!" scripts\windows_healthcheck.py >> logs\healthcheck.log 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Healthcheck failed. See logs\healthcheck.log
    pause
    goto :EOF
)

:: 18. Supervisor Start
echo [INFO] Starting supervisor...
"!PYTHON_EXE!" scripts\windows_supervisor.py
if !errorlevel! neq 0 (
    echo [ERROR] Supervisor exited with error. See logs\errors.log
    pause
    goto :EOF
)

echo [INFO] Shutdown complete.
