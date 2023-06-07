@echo off

REM Check Python & pip are installed
python --version || (echo Please install Python before proceeding. && exit /b)
pip --version || (echo Please install pip before proceeding. && exit /b)

REM Check if the virtual environment exists, otherwise create it
IF NOT EXIST .venv (
    python -m venv .venv
)

REM Activate the virtual environment
call .venv\Scripts\activate

REM Install requirements if they are not yet installed
(requirements_install_check.py >nul 2>&1) || pip install -r requirements.txt

REM Run the app
start /b python app-ui.py

REM Open the app in a web browser
python -m webbrowser "http://localhost:7860"

REM Deactivate the environment
deactivate

pause
