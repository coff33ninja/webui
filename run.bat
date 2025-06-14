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

REM Check Python version (only allow 3.13.x)
python -c "import sys; assert sys.version_info[:2] == (3, 11), 'Python 3.11.x is required'" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python 3.11.x is required
    echo Current Python version:
    python --version
    pause
    exit /b 1
)

REM Detect virtual environment directory
set VENV_DIR=
if exist .venv (
    set VENV_DIR=.venv
) else if exist venv (
    set VENV_DIR=venv
)

REM Create virtual environment if neither exists
if not defined VENV_DIR (
    echo No virtual environment found! Creating .venv...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
    set VENV_DIR=.venv
    echo Installing dependencies...
    call .venv\Scripts\activate
    pip install --upgrade --requirement requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Virtual environment found in %VENV_DIR%. Activating...
)

REM Activate virtual environment and run the application
call %VENV_DIR%\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if Python executable exists in venv
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo ERROR: Python executable not found in virtual environment: %VENV_DIR%\Scripts\python.exe
    echo The virtual environment in "%VENV_DIR%" might be corrupted.
    echo Please try deleting the "%VENV_DIR%" directory and re-running this script.
    pause
    exit /b 1
)

echo Starting WebUI...
%VENV_DIR%\Scripts\python.exe main.py
if %ERRORLEVEL% neq 0 (
    echo Application exited with error code %ERRORLEVEL%
    pause
    exit /b 1
)
