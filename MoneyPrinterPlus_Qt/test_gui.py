#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的PyQt6 GUI测试
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_pyqt6_import():
    """测试PyQt6导入"""
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
        from PyQt6.QtCore import Qt
        print("[OK] PyQt6导入成功")
        return True
    except ImportError as e:
        print(f"[ERROR] PyQt6导入失败: {e}")
        return False

def test_simple_window():
    """测试简单窗口"""
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
        from PyQt6.QtCore import Qt
        
        app = QApplication(sys.argv)
        
        # 创建主窗口
        window = QMainWindow()
        window.setWindowTitle("MoneyPrinterPlus PyQt6测试")
        window.setMinimumSize(400, 300)
        
        # 中央部件
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        
        # 布局
        layout = QVBoxLayout(central_widget)
        
        # 标签
        label = QLabel("MoneyPrinterPlus PyQt6版本测试")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; padding: 20px;")
        layout.addWidget(label)
        
        status_label = QLabel("如果您能看到这个窗口，说明PyQt6工作正常！")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet("font-size: 14px; color: green;")
        layout.addWidget(status_label)
        
        # 显示窗口
        window.show()
        print("[OK] 测试窗口创建成功")
        
        # 运行应用（这里我们不调用exec()来避免阻塞）
        # app.exec()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 创建测试窗口失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始PyQt6 GUI测试...")
    
    # 测试导入
    if not test_pyqt6_import():
        return False
    
    # 测试简单窗口
    if not test_simple_window():
        return False
    
    print("\n[OK] PyQt6 GUI测试完成！")
    print("所有基础功能正常，可以运行完整的应用")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)