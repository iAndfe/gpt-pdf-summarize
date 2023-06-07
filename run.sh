#!/bin/bash

# Check Python & pip are installed
python --version > /dev/null 2>&1 || { echo >&2 "Please install Python before proceeding."; exit 1; }
pip --version > /dev/null 2>&1 || { echo >&2 "Please install pip before proceeding."; exit 1; }

# Check if the virtual environment exists, otherwise create it
if [ ! -d ".venv" ]; then
    python -m venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install requirements if they are not yet installed
python requirements_install_check.py > /dev/null 2>&1 || pip install -r requirements.txt

# Run the app
python app-ui.py

# Deactivate the environment
deactivate

read -n 1 -s -r -p "Press any key to continue"
