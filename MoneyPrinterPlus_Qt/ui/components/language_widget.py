"""
语言选择组件
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLabel
from PyQt6.QtCore import pyqtSignal

from core.config_manager import config_manager, LANGUAGES
from core.translator import tr

class LanguageWidget(QWidget):
    language_changed = pyqtSignal(str)  # 语言变更信号
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 语言选择行
        lang_layout = QHBoxLayout()
        
        # 标签
        self.label = QLabel(tr("Language"))
        self.label.setMinimumWidth(120)
        self.label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #333;
            }
        """)
        
        # 语言下拉框
        self.language_combo = QComboBox()
        self.language_combo.setMinimumWidth(200)
        self.language_combo.setStyleSheet("""
            QComboBox {
                padding: 8px 12px;
                font-size: 13px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                color: #212529;
                selection-background-color: #4a90e2;
            }
            QComboBox:hover {
                border-color: #4a90e2;
            }
            QComboBox:focus {
                border-color: #4a90e2;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background-color: white;
            }
            QComboBox::down-arrow {
                image: none;
                border: 2px solid #666;
                width: 6px;
                height: 6px;
                border-top: none;
                border-right: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                color: #212529;
                selection-background-color: #4a90e2;
                selection-color: white;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                color: #212529;
                background-color: white;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item:selected {
                color: white;
                background-color: #4a90e2;
            }
        """)
        
        # 填充语言选项
        self.populate_languages()
        
        # 连接信号
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
        
        # 布局
        lang_layout.addWidget(self.label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        layout.addLayout(lang_layout)
    
    def populate_languages(self):
        """填充语言选项"""
        self.language_combo.clear()
        for code, name in LANGUAGES.items():
            display_text = f"{code} - {name}"
            self.language_combo.addItem(display_text, code)
    
    def load_config(self):
        """加载配置"""
        current_language = config_manager.get_ui_language()
        
        # 临时断开信号连接，避免触发change事件
        self.language_combo.currentTextChanged.disconnect()
        
        # 设置当前选中的语言
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == current_language:
                self.language_combo.setCurrentIndex(i)
                break
        
        # 重新连接信号
        self.language_combo.currentTextChanged.connect(self.on_language_changed)
    
    def on_language_changed(self, text):
        """语言改变处理"""
        if text:
            # 获取语言代码
            current_index = self.language_combo.currentIndex()
            if current_index >= 0:
                language_code = self.language_combo.itemData(current_index)
                if language_code:
                    self.language_changed.emit(language_code)
    
    def update_text(self):
        """更新界面文本"""
        self.label.setText(tr("Language"))
        
        # 临时断开信号连接
        self.language_combo.currentTextChanged.disconnect()
        
        # 重新填充选项（保持当前选择）
        current_data = None
        if self.language_combo.currentIndex() >= 0:
            current_data = self.language_combo.itemData(self.language_combo.currentIndex())
        
        self.populate_languages()
        
        # 恢复选择
        if current_data:
            for i in range(self.language_combo.count()):
                if self.language_combo.itemData(i) == current_data:
                    self.language_combo.setCurrentIndex(i)
                    break
        
        # 重新连接信号
        self.language_combo.currentTextChanged.connect(self.on_language_changed)