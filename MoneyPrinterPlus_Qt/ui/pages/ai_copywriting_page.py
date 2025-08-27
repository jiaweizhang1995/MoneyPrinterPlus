"""
AI文案生成页面
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.translator import tr
from ui.components.ai_copywriting_widget import AICopywritingWidget

class AICopywritingPage(QWidget):
    """AI文案生成页面"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 页面标题
        self.create_page_header(main_layout)
        
        # AI文案生成组件
        self.ai_copywriting_widget = AICopywritingWidget()
        main_layout.addWidget(self.ai_copywriting_widget)
        
        # 应用样式
        self.apply_styles()
        
    def create_page_header(self, parent_layout):
        """创建页面标题"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.Box)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #6f42c1, stop: 1 #5a32a3);
                border: 1px solid #4c2a85;
                border-bottom: none;
                padding: 15px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # 主标题
        title_label = QLabel("✨ " + tr("AI Copywriting"))
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 5px 0px;
            }
        """)
        
        # 副标题
        subtitle_label = QLabel("智能AI文案生成，让创意文字触手可及")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                background: transparent;
                border: none;
                padding: 2px 0px;
                font-weight: 400;
            }
        """)
        
        # 功能说明
        description_label = QLabel("💡 基于产品卖点信息，使用先进的AI技术生成高质量营销文案")
        description_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        description_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                background: transparent;
                border: none;
                padding: 5px 0px 0px 0px;
                font-style: italic;
            }
        """)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        header_layout.addWidget(description_label)
        
        parent_layout.addWidget(header_frame)
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            AICopywritingPage {
                background-color: #f8f9fa;
                color: #212529;
            }
        """)
        
    def update_text(self):
        """更新界面文本（多语言支持）"""
        # 更新AI文案生成组件
        self.ai_copywriting_widget.update_text()