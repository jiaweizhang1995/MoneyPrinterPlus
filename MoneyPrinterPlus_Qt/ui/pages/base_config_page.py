"""
基础配置页面 - 重构自原主窗口内容
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QScrollArea, 
                             QFrame, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.config_manager import config_manager
from core.translator import tr, set_language
from ui.components.language_widget import LanguageWidget
from ui.components.audio_config_widget import AudioConfigWidget
from ui.components.llm_config_widget import LLMConfigWidget

class BaseConfigPage(QWidget):
    """基础配置页面"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_config()
        
    def setup_ui(self):
        """设置界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        
        # 页面标题
        self.create_page_header(main_layout)
        
        # 创建滚动区域
        self.create_scroll_area(main_layout)
        
        # 应用样式
        self.apply_styles()
    
    def create_page_header(self, parent_layout):
        """创建页面标题"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4a90e2, stop: 1 #357abd);
                border: 1px solid #2c5aa0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        # 主标题
        title_label = QLabel(tr("Base Config"))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 5px;
            }
        """)
        
        # 副标题
        subtitle_label = QLabel("配置系统基础参数")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #e8f4f8;
                font-size: 16px;
                background: transparent;
                border: none;
                padding: 2px;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        parent_layout.addWidget(header_frame)
    
    def create_scroll_area(self, parent_layout):
        """创建滚动区域"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 创建内容部件
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建配置组
        self.create_config_groups(content_layout)
        
        # 设置滚动区域
        scroll_area.setWidget(content_widget)
        parent_layout.addWidget(scroll_area)
    
    def create_config_groups(self, parent_layout):
        """创建配置组"""
        # 语言配置组
        self.language_group = self.create_group_box(tr("Language"), parent_layout)
        self.language_widget = LanguageWidget()
        self.language_widget.language_changed.connect(self.on_language_changed)
        self.add_widget_to_group(self.language_group, self.language_widget)
        
        # 音频配置组  
        self.audio_group = self.create_group_box(tr("Audio Provider Info"), parent_layout)
        self.audio_widget = AudioConfigWidget()
        self.add_widget_to_group(self.audio_group, self.audio_widget)
        
        # LLM配置组
        self.llm_group = self.create_group_box(tr("LLM Provider"), parent_layout)
        self.llm_widget = LLMConfigWidget()
        self.add_widget_to_group(self.llm_group, self.llm_widget)
    
    def create_group_box(self, title, parent_layout):
        """创建组框"""
        group_box = QGroupBox(title)
        group_box.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #f5f5f5;
                border-radius: 3px;
            }
        """)
        parent_layout.addWidget(group_box)
        return group_box
    
    def add_widget_to_group(self, group_box, widget):
        """向组框添加部件"""
        layout = QVBoxLayout(group_box)
        layout.addWidget(widget)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            BaseConfigPage {
                background-color: #f8f9fa;
                color: #212529;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
                color: #212529;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #f8f9fa;
                color: #212529;
            }
            QWidget {
                font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
                color: #212529;
            }
            QLabel {
                color: #212529;
            }
            QComboBox {
                color: #212529;
                background-color: white;
            }
            QComboBox QAbstractItemView {
                color: #212529;
                background-color: white;
                selection-color: white;
                selection-background-color: #4a90e2;
            }
            QLineEdit {
                color: #212529;
                background-color: white;
            }
        """)
    
    def load_config(self):
        """加载配置"""
        # 设置语言
        language = config_manager.get_ui_language()
        set_language(language)
    
    def update_text(self):
        """更新界面文本"""
        self.language_group.setTitle(tr("Language"))
        self.audio_group.setTitle(tr("Audio Provider Info"))  
        self.llm_group.setTitle(tr("LLM Provider"))
        
        # 通知子组件更新
        self.language_widget.update_text()
        self.audio_widget.update_text()
        self.llm_widget.update_text()
    
    def on_language_changed(self, language):
        """语言改变处理"""
        set_language(language)
        config_manager.set_ui_language(language)
        self.update_text()