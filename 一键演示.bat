@echo off
title Graph_Launcher

:: 1. Check Python
echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found!
    pause
    exit
)

:: 2. Install
echo Installing libraries, please wait...
python -m pip install --upgrade pip --user
python -m pip install streamlit torch pyvis pandas --user

:: 3. Run
echo Starting Streamlit...
cd /d "%~dp0"
python -m streamlit run app.py

pause