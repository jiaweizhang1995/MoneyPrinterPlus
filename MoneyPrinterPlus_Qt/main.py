"""
MoneyPrinterPlus PyQt6版本主入口
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

from ui.main_window import MainWindow
from core.config_manager import APP_TITLE

class MoneyPrinterPlusApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName(APP_TITLE)
        self.setApplicationVersion("2.0.0")
        
        # 设置应用图标
        self.setup_app_icon()
        
        # 设置全局样式
        self.setup_global_style()
    
    def setup_app_icon(self):
        """设置应用图标"""
        # 这里可以设置应用图标
        # icon = QIcon("resources/icons/app.ico")
        # self.setWindowIcon(icon)
        pass
    
    def setup_global_style(self):
        """设置全局样式"""
        style = """
            /* 全局字体和基础样式 */
            * {
                font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
            }
            
            /* 工具提示样式 */
            QToolTip {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }
            
            /* 滚动条样式 */
            QScrollBar:vertical {
                background-color: #f1f1f1;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8a8;
            }
            
            QScrollBar::handle:vertical:pressed {
                background-color: #909090;
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background-color: #f1f1f1;
                height: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:horizontal {
                background-color: #c1c1c1;
                border-radius: 6px;
                min-width: 20px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background-color: #a8a8a8;
            }
            
            QScrollBar::handle:horizontal:pressed {
                background-color: #909090;
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """
        self.setStyleSheet(style)

def main():
    """主函数"""
    try:
        # 创建应用
        app = MoneyPrinterPlusApp(sys.argv)
        
        # 创建主窗口
        window = MainWindow()
        window.show()
        
        # 运行应用
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"应用启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()