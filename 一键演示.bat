@echo off
title ÁãÊÛÍ¼Æ×Æô¶¯Æ÷

echo ======================================================
echo       Retail Hetero-Graph System Launcher
echo ======================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.9+.
    pause
    exit
)

:: 2. Install Dependencies
echo [1/2] Checking dependencies...
echo Please wait, this may take 1-3 minutes...
echo.

python -m pip install --upgrade pip -q
python -m pip install streamlit torch pyvis pandas -i https://pypi.tuna.tsinghua.edu.cn/simple -q

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed! Please check your network.
    pause
    exit
)

:: 3. Run App
echo.
echo [2/2] Environment ready. Starting system...
echo.

cd /d %~dp0
streamlit run app.py

pause