#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试应用启动和基础功能
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_app_startup():
    """测试应用启动"""
    try:
        from PyQt6.QtWidgets import QApplication
        from ui.main_window import MainWindow
        
        print("正在创建QApplication...")
        app = QApplication(sys.argv)
        
        print("正在创建主窗口...")
        window = MainWindow()
        
        print("正在显示窗口...")
        window.show()
        
        print("应用启动成功！")
        print("窗口标题:", window.windowTitle())
        print("窗口大小:", window.size().width(), "x", window.size().height())
        
        # 测试配置加载
        from core.config_manager import config_manager
        print("当前语言:", config_manager.get_ui_language())
        print("音频提供商:", config_manager.get_audio_provider())
        print("LLM提供商:", config_manager.get_llm_provider())
        
        # 自动关闭应用
        print("2秒后自动关闭...")
        from PyQt6.QtCore import QTimer
        timer = QTimer()
        timer.singleShot(2000, app.quit)
        
        # 运行应用
        result = app.exec()
        print(f"应用正常退出，返回代码: {result}")
        return True
        
    except Exception as e:
        print(f"应用启动失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_startup()
    if success:
        print("\n✓ 应用启动测试成功！")
        print("应用可以正常启动和关闭，没有递归错误")
    else:
        print("\n✗ 应用启动测试失败")
        sys.exit(1)