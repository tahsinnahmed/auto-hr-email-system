@echo off
cd /d "%~dp0"

IF NOT EXIST venv (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    echo [SETUP] Activating virtual environment...
    call venv\Scripts\activate.bat
    echo [SETUP] Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo [SETUP] Setup complete.
    echo.
) ELSE (
    call venv\Scripts\activate.bat
)

python start.py
pause