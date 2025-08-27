#!/usr/bin/env python3
"""
专门测试导航组件的显示效果
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer

from ui.components.navigation_widget import NavigationWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("测试导航组件")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加导航组件
        self.nav_widget = NavigationWidget()
        layout.addWidget(self.nav_widget)
        
        # 添加内容区域
        content_label = QLabel("导航测试\n如果左侧导航文字可见，说明修复成功")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_label.setStyleSheet("font-size: 16px; padding: 20px;")
        layout.addWidget(content_label)
        
        # 设置比例
        layout.setStretchFactor(self.nav_widget, 0)
        layout.setStretchFactor(content_label, 1)

def main():
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    print("测试窗口已打开")
    print("请检查左侧导航栏的文字是否可见")
    
    # 3秒后自动关闭
    QTimer.singleShot(3000, app.quit)
    
    app.exec()
    print("测试完成")

if __name__ == "__main__":
    main()