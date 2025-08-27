"""
导航组件 - 侧边栏菜单导航
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QListWidget, QListWidgetItem, 
                             QLabel, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from core.translator import tr

class NavigationWidget(QWidget):
    """侧边栏导航组件"""
    
    # 信号：页面切换
    page_changed = pyqtSignal(int)  # 发送页面索引
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_navigation_items()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题区域
        self.create_title_section(layout)
        
        # 导航列表
        self.create_navigation_list(layout)
        
        # 应用样式
        self.apply_styles()
        
    def create_title_section(self, parent_layout):
        """创建标题区域"""
        title_frame = QFrame()
        title_frame.setObjectName("titleFrame")
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(10, 15, 10, 15)
        
        # 应用标题
        title_label = QLabel("MoneyPrinter+")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 版本标签
        version_label = QLabel("v2.0.0")
        version_label.setObjectName("versionLabel")  
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(version_label)
        
        parent_layout.addWidget(title_frame)
        
    def create_navigation_list(self, parent_layout):
        """创建导航列表"""
        self.nav_list = QListWidget()
        self.nav_list.setObjectName("navList")
        
        # 设置列表属性
        self.nav_list.setFrameShape(QFrame.Shape.NoFrame)
        self.nav_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.nav_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.nav_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 连接信号
        self.nav_list.currentRowChanged.connect(self.on_item_clicked)
        
        parent_layout.addWidget(self.nav_list)
        
    def setup_navigation_items(self):
        """设置导航项目"""
        # 导航项目数据：(文本键，图标，描述)
        nav_items = [
            ("Base Config", "⚙️", "基础配置设置"),
            ("AI Copywriting", "✨", "AI智能文案生成"),  
            ("Mix Video", "🎬", "视频混剪处理"),
            ("Deduplication Process", "🔧", "视频去重处理"),
        ]
        
        for i, (text_key, icon, description) in enumerate(nav_items):
            # 使用简单的文本项目而不是自定义部件
            item_text = f"{icon} {tr(text_key)}"
            item = QListWidgetItem(item_text)
            
            # 设置项目样式
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 添加到列表
            self.nav_list.addItem(item)
        
        # 默认选中第一项
        self.nav_list.setCurrentRow(0)
        
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            NavigationWidget {
                background-color: #f8f9fa;
                border-right: 1px solid #dee2e6;
                min-width: 160px;
                max-width: 160px;
            }
            
            /* 标题区域 */
            #titleFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e9ecef, stop: 1 #f8f9fa);
                border-bottom: 1px solid #dee2e6;
            }
            
            #titleLabel {
                color: #212529;
                font-size: 16px;
                font-weight: bold;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
            }
            
            #versionLabel {
                color: #6c757d;
                font-size: 11px;
            }
            
            /* 导航列表 */
            QListWidget#navList {
                background-color: transparent;
                border: none;
                outline: none;
                color: black;
                font-size: 13px;
                font-weight: bold;
            }
            
            QListWidget#navList::item {
                border: none;
                padding: 15px 8px;
                margin: 2px 8px;
                border-radius: 6px;
                background-color: transparent;
                color: black;
                text-align: center;
            }
            
            QListWidget#navList::item:selected {
                background-color: #3498db;
                border: 2px solid #2980b9;
                color: white;
                font-weight: bold;
            }
            
            QListWidget#navList::item:hover {
                background-color: rgba(52, 152, 219, 0.4);
                border: 1px solid #3498db;
                color: white;
            }
        """)
        
    def on_item_clicked(self, current_row):
        """导航项目点击处理"""
        if current_row >= 0:
            self.page_changed.emit(current_row)
    
    def set_current_page(self, page_index):
        """设置当前页面"""
        if 0 <= page_index < self.nav_list.count():
            self.nav_list.setCurrentRow(page_index)
    
    def update_text(self):
        """更新界面文本（多语言支持）"""
        # 重新设置导航项目文本
        nav_items = [
            ("Base Config", "⚙️"),
            ("AI Copywriting", "✨"), 
            ("Mix Video", "🎬"),
            ("Deduplication Process", "🔧"),
        ]
        
        for i, (text_key, icon) in enumerate(nav_items):
            item = self.nav_list.item(i)
            if item:
                item_text = f"{icon} {tr(text_key)}"
                item.setText(item_text)