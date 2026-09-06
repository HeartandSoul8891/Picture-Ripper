@echo off
:: Create the virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromiumm

echo Setup complete!
pause