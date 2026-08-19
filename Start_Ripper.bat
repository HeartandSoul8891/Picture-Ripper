@echo off
::set HSA_OVERRIDE_GFX_VERSION=11.5.1
::set CUDA_VISIBLE_DEVICES=0
:: set HIP_VISIBLE_DEVICES=1
:: uncomment the above line to use AMD GPU, comment it to use NVIDIA GPU

::REM Activate the virtual environment
:: call .\venv\Scripts\activate.bat

::REM Run Streamlit
streamlit run main.py