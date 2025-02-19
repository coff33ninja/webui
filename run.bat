@echo off
cd /d "%~dp0"

if not exist venv (
    echo Virtual environment not found! Creating one...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
)

echo Activating virtual environment...
call venv\Scripts\activate
venv\Scripts\python.exe webui_wrapper.py
pause
