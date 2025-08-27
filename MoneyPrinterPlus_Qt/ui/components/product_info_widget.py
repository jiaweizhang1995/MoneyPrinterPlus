"""
产品信息组件 - 管理产品卖点信息
"""
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QFileDialog, QMessageBox,
                             QGroupBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.translator import tr

class ProductInfoWidget(QWidget):
    """产品信息管理组件"""
    
    # 信号：产品信息改变
    product_info_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.product_info_file = "product_selling_point.txt"
        self.setup_ui()
        self.load_product_info()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建分组框
        group_box = QGroupBox(tr("Product Information"))
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
        
        group_layout = QVBoxLayout(group_box)
        
        # 文件操作按钮
        self.create_file_buttons(group_layout)
        
        # 产品信息文本编辑器
        self.create_text_editor(group_layout)
        
        layout.addWidget(group_box)
        
    def create_file_buttons(self, parent_layout):
        """创建文件操作按钮"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 加载文件按钮
        self.load_button = QPushButton("📁 " + tr("Load File"))
        self.load_button.setToolTip(tr("Load product information from file"))
        self.load_button.clicked.connect(self.load_from_file)
        self.load_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        
        # 保存文件按钮
        self.save_button = QPushButton("💾 " + tr("Save File"))
        self.save_button.setToolTip(tr("Save product information to file"))
        self.save_button.clicked.connect(self.save_to_file)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        
        # 清空按钮
        self.clear_button = QPushButton("🗑️ " + tr("Clear"))
        self.clear_button.setToolTip(tr("Clear all product information"))
        self.clear_button.clicked.connect(self.clear_content)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
        """)
        
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()
        
        parent_layout.addLayout(button_layout)
        
    def create_text_editor(self, parent_layout):
        """创建文本编辑器"""
        # 状态标签
        self.status_label = QLabel(tr("Product selling points information"))
        self.status_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                padding: 5px;
            }
        """)
        parent_layout.addWidget(self.status_label)
        
        # 文本编辑器
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(tr("Enter product selling points here..."))
        self.text_edit.setMinimumHeight(200)
        self.text_edit.setMaximumHeight(300)
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                font-family: "Consolas", "Monaco", monospace;
                font-size: 13px;
                line-height: 1.4;
                background-color: white;
                color: #212529;
            }
            QTextEdit:focus {
                border-color: #4a90e2;
                outline: none;
            }
        """)
        
        parent_layout.addWidget(self.text_edit)
        
    def load_product_info(self):
        """加载产品信息"""
        try:
            if os.path.exists(self.product_info_file):
                with open(self.product_info_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.text_edit.setPlainText(content)
                    self.update_status(f"已加载文件: {self.product_info_file}")
            else:
                self.update_status("产品卖点文件不存在，请创建或导入")
        except Exception as e:
            self.update_status(f"加载文件失败: {str(e)}", is_error=True)
            
    def load_from_file(self):
        """从文件加载"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            tr("Select Product Information File"),
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    self.text_edit.setPlainText(content)
                    self.update_status(f"已加载文件: {os.path.basename(file_path)}")
            except Exception as e:
                self.show_error(f"加载文件失败: {str(e)}")
                
    def save_to_file(self):
        """保存到文件"""
        content = self.text_edit.toPlainText().strip()
        if not content:
            self.show_warning("没有内容需要保存")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("Save Product Information File"),
            self.product_info_file,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_status(f"已保存到文件: {os.path.basename(file_path)}")
                
                # 如果保存的是默认文件，更新文件路径
                if os.path.basename(file_path) == self.product_info_file:
                    self.product_info_file = file_path
                    
            except Exception as e:
                self.show_error(f"保存文件失败: {str(e)}")
                
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有产品信息吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.text_edit.clear()
            self.update_status("已清空产品信息")
            
    def on_text_changed(self):
        """文本改变处理"""
        content = self.text_edit.toPlainText().strip()
        word_count = len(content.split()) if content else 0
        char_count = len(content)
        
        self.update_status(f"字数: {word_count}, 字符数: {char_count}")
        
        # 发送信号
        self.product_info_changed.emit(content)
        
    def get_product_info(self):
        """获取产品信息"""
        return self.text_edit.toPlainText().strip()
        
    def set_product_info(self, content):
        """设置产品信息"""
        self.text_edit.setPlainText(content)
        
    def update_status(self, message, is_error=False):
        """更新状态"""
        if is_error:
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #dc3545;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
        else:
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #28a745;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
        self.status_label.setText(message)
        
    def show_error(self, message):
        """显示错误消息"""
        QMessageBox.critical(self, "错误", message)
        
    def show_warning(self, message):
        """显示警告消息"""
        QMessageBox.warning(self, "警告", message)
        
    def update_text(self):
        """更新界面文本（多语言支持）"""
        # 更新按钮文本
        self.load_button.setText("📁 " + tr("Load File"))
        self.save_button.setText("💾 " + tr("Save File"))
        self.clear_button.setText("🗑️ " + tr("Clear"))
        
        # 更新占位符文本
        self.text_edit.setPlaceholderText(tr("Enter product selling points here..."))
        
        # 更新工具提示
        self.load_button.setToolTip(tr("Load product information from file"))
        self.save_button.setToolTip(tr("Save product information to file"))
        self.clear_button.setToolTip(tr("Clear all product information"))