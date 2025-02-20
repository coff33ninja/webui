@echo off
setlocal enabledelayedexpansion

REM Change to script directory
cd /d "%~dp0"

REM Check Python installation
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.11 or newer from https://www.python.org/
    pause
    exit /b 1
)

REM Check Python version
python -c "import sys; assert sys.version_info >= (3, 11), 'Python 3.11 or newer is required'" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python 3.11 or newer is required
    echo Current Python version:
    python --version
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Virtual environment not found! Creating one...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Installing dependencies...
    call venv\Scripts\activate
    pip install --upgrade --requirement requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Virtual environment found. Activating...
)

REM Activate virtual environment and run the application
call venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Starting WebUI...
venv\Scripts\python.exe main.py
if %ERRORLEVEL% neq 0 (
    echo Application exited with error code %ERRORLEVEL%
    pause
)
