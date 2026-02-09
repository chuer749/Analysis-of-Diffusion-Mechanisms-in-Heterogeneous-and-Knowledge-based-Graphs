@echo off
title 零售图谱启动器-官方源版

echo ======================================================
echo       Retail Hetero-Graph System Launcher
echo ======================================================
echo.

:: 1. 检查 Python 环境
echo [1/3] Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! 
    pause
    exit
)

:: 2. 使用官方源安装依赖
echo [2/3] Installing dependencies from official PyPI...
echo It might take a few minutes depending on connection speed.
echo.

:: 升级 pip
python -m pip install --upgrade pip --user

:: 安装核心库
python -m pip install streamlit torch pyvis pandas --user

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed. Please check your internet connection.
    pause
    exit
)

:: 3. 运行程序
echo.
echo [3/3] Starting system...
echo.

cd /d %~dp0
python -m streamlit run app.py

pause