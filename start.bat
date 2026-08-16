@echo off
REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run Streamlit
streamlit run main.py

REM Deactivate the virtual environment (optional)
REM deactivate