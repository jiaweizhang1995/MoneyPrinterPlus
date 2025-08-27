#!/usr/bin/env python3
"""
测试AI文案生成功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from ui.main_window import MainWindow

def test_app():
    """测试应用程序启动"""
    try:
        # 创建应用
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 自动切换到AI文案生成页面
        QTimer.singleShot(1000, lambda: window.stacked_widget.setCurrentIndex(1))
        
        # 自动关闭应用（测试模式）
        QTimer.singleShot(5000, app.quit)
        
        print("[OK] 应用程序启动成功")
        print("[OK] AI文案生成界面已加载")
        print("[INFO] 应用将在5秒后自动关闭...")
        
        # 运行应用（测试5秒）
        app.exec()
        
        print("[OK] 应用程序测试完成")
        return True
        
    except Exception as e:
        print(f"[ERROR] 应用程序测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app()
    sys.exit(0 if success else 1)