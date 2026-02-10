@echo off
title Graph_Project_Launcher

:: ------------------------------------------
:: 1. Check Python
:: ------------------------------------------
echo Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.9 or higher.
    pause
    exit
)

:: ------------------------------------------
:: 2. Setup Virtual Environment (Sandbox)
:: ------------------------------------------
cd /d "%~dp0"
if not exist "venv" (
    echo Creating a private virtual environment...
    python -m venv venv
)

echo Activating sandbox...
call venv\Scripts\activate

:: ------------------------------------------
:: 3. Install Dependencies
:: ------------------------------------------
echo Installing required libraries...
echo This will NOT affect your global Python environment.
python -m pip install --upgrade pip -q
python -m pip install streamlit torch pyvis pandas -q

if %errorlevel% neq 0 (
    echo [ERROR] Installation failed. Please check your internet connection.
    pause
    exit
)

:: ------------------------------------------
:: 4. Run Application
:: ------------------------------------------
echo Starting the system...
python -m streamlit run app.py

pause