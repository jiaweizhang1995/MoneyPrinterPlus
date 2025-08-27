"""
主窗口 - 基于PyQt6的现代化界面
"""
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QStackedWidget, QLabel, QFrame, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from core.config_manager import config_manager, APP_TITLE
from core.translator import tr, set_language
from ui.components.navigation_widget import NavigationWidget
from ui.pages.base_config_page import BaseConfigPage
from ui.pages.ai_copywriting_page import AICopywritingPage
from ui.pages.mix_video_page import MixVideoPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(1200, 800)
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        """设置界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 使用水平分割器
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建导航和页面区域
        self.create_navigation_area(splitter)
        self.create_content_area(splitter)
        
        # 设置分割器比例
        splitter.setSizes([160, 1040])  # 导航:内容 = 160:1040
        splitter.setChildrenCollapsible(False)  # 防止折叠
        
        main_layout.addWidget(splitter)
        
        # 应用样式
        self.apply_styles()
    
    def create_navigation_area(self, splitter):
        """创建导航区域"""
        self.navigation_widget = NavigationWidget()
        self.navigation_widget.page_changed.connect(self.on_page_changed)
        splitter.addWidget(self.navigation_widget)
        
    def create_content_area(self, splitter):
        """创建内容区域"""
        # 创建页面堆栈
        self.stacked_widget = QStackedWidget()
        
        # 添加页面
        self.setup_pages()
        
        splitter.addWidget(self.stacked_widget)
        
    def setup_pages(self):
        """设置所有页面"""
        # 基础配置页面
        self.base_config_page = BaseConfigPage()
        self.stacked_widget.addWidget(self.base_config_page)
        
        # AI文案生成页面
        self.ai_copywriting_page = AICopywritingPage()
        self.stacked_widget.addWidget(self.ai_copywriting_page)
        
        # 视频混剪页面
        self.mix_video_page = MixVideoPage()
        self.stacked_widget.addWidget(self.mix_video_page)
        
        # 去重处理页面（占位符）
        deduplication_placeholder = QLabel("去重处理页面\n敬请期待...")
        deduplication_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        deduplication_placeholder.setStyleSheet("""
            QLabel {
                font-size: 24px;
                color: #666;
                background-color: #f8f9fa;
            }
        """)
        self.stacked_widget.addWidget(deduplication_placeholder)
    
    def apply_styles(self):
        """应用全局样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
                color: #212529;
            }
            
            QSplitter::handle {
                background-color: #dee2e6;
                width: 1px;
            }
            
            QSplitter::handle:hover {
                background-color: #adb5bd;
            }
            
            QStackedWidget {
                background-color: #f8f9fa;
                border: none;
            }
        """)
    
    def load_config(self):
        """加载配置"""
        # 设置语言
        language = config_manager.get_ui_language()
        set_language(language)
        
        # 更新界面文本
        self.update_ui_text()
    
    def update_ui_text(self):
        """更新界面文本"""
        # 更新导航组件
        self.navigation_widget.update_text()
        
        # 更新基础配置页面
        self.base_config_page.update_text()
        
        # 更新AI文案生成页面
        self.ai_copywriting_page.update_text()
        
        # 更新视频混剪页面
        if hasattr(self.mix_video_page, 'update_text'):
            self.mix_video_page.update_text()
    
    def on_page_changed(self, page_index):
        """页面切换处理"""
        self.stacked_widget.setCurrentIndex(page_index)
        
    def on_language_changed(self, language):
        """语言改变处理"""
        set_language(language)
        config_manager.set_ui_language(language)
        self.update_ui_text()
        
    def closeEvent(self, event):
        """关闭事件"""
        # 保存配置
        config_manager.save_config()
        event.accept()