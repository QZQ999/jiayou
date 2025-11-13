@echo off
REM ================================================================
REM  DCA Experiment Launcher - Windows Batch Script
REM  双击此文件即可启动 DCA 实验选择界面
REM ================================================================

title DCA Experiment Launcher

echo.
echo ================================================================
echo   DCA 实验启动器
echo   Collective Assault Multi-Agent Environment
echo ================================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python！
    echo 请先安装 Python 3.7 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [检查] Python 已安装
python --version

REM 检查必要的包
echo.
echo [检查] 正在检查必要的 Python 包...
python -c "import numpy, torch" >nul 2>&1
if errorlevel 1 (
    echo [警告] 部分依赖包可能未安装
    echo 如果运行出错，请执行: pip install -r requirements.txt
    echo.
)

REM 运行启动器
echo.
echo [启动] 正在启动 DCA 实验选择器...
echo.

python run_dca.py

if errorlevel 1 (
    echo.
    echo [错误] 程序异常退出
    pause
    exit /b 1
)

echo.
echo [完成] 实验已结束
pause
