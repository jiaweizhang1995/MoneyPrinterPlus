#!/bin/bash
echo "启动 MoneyPrinterPlus PyQt6版本..."
echo
echo "使用虚拟环境: ../venv/bin/python"
echo

../venv/bin/python main.py

if [ $? -ne 0 ]; then
    echo
    echo "启动失败，请检查："
    echo "1. 虚拟环境是否存在: ../venv/"
    echo "2. PyQt6是否已安装: ../venv/bin/pip list | grep PyQt6"
    echo "3. 依赖是否完整: ../venv/bin/pip install -r requirements_qt.txt"
    read -p "按任意键继续..."
else
    echo "应用已正常关闭"
fi