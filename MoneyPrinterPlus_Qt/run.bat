@echo off
echo 启动 MoneyPrinterPlus PyQt6版本...
echo.
echo 使用虚拟环境: ..\venv\Scripts\python.exe
echo.
..\venv\Scripts\python.exe main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 启动失败，请检查：
    echo 1. 虚拟环境是否存在: ..\venv\
    echo 2. PyQt6是否已安装: ..\venv\Scripts\pip.exe list ^| findstr PyQt6
    echo 3. 依赖是否完整: ..\venv\Scripts\pip.exe install -r requirements_qt.txt
    pause
) else (
    echo 应用已正常关闭
)