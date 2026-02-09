@echo off
:: 强制使用 UTF-8 编码防止乱码
chcp 65001 > nul
@echo off
title 零售异质图分析系统 - 启动器

echo ======================================================
echo       零售异质图多维决策模拟器 - 一键启动脚本
echo ======================================================
echo.

:: 1. 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9 或更高版本！
    pause
    exit
)

:: 2. 检查并安装必要的库
echo [1/2] 正在检查依赖库 (Streamlit, Torch, Pyvis)...
echo 提示：如果是首次运行，可能需要 1-3 分钟，请稍候...
echo.

:: 使用清华镜像源加速安装
python -m pip install --upgrade pip -q
python -m pip install streamlit torch pyvis pandas -i https://pypi.tuna.tsinghua.edu.cn/simple -q

if %errorlevel% neq 0 (
    echo.
    echo [错误] 依赖库安装失败！请检查网络连接。
    pause
    exit
)

:: 3. 运行程序
echo.
echo [2/2] 环境准备就绪，正在启动系统...
echo.
streamlit run app.py

pause