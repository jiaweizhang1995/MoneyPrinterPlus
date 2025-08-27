"""
文案结果组件 - 显示和编辑生成的AI文案
"""
import os
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QGroupBox, QFileDialog,
                             QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCursor

from core.translator import tr

class CopywritingResultWidget(QWidget):
    """文案结果组件"""
    
    # 信号：文案改变
    copywriting_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建分组框
        group_box = QGroupBox(tr("Generated Copywriting"))
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
        
        # 操作按钮栏
        self.create_action_buttons(group_layout)
        
        # 生成进度条（初始隐藏）
        self.create_progress_bar(group_layout)
        
        # 文案结果编辑器
        self.create_result_editor(group_layout)
        
        # 统计信息
        self.create_statistics(group_layout)
        
        layout.addWidget(group_box)
        
    def create_action_buttons(self, parent_layout):
        """创建操作按钮"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 复制按钮
        self.copy_button = QPushButton("📋 " + tr("Copy"))
        self.copy_button.setToolTip(tr("Copy copywriting to clipboard"))
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
            QPushButton:pressed {
                background-color: #117a8b;
            }
        """)
        
        # 保存按钮
        self.save_button = QPushButton("💾 " + tr("Save"))
        self.save_button.setToolTip(tr("Save copywriting to file"))
        self.save_button.clicked.connect(self.save_to_file)
        self.save_button.setStyleSheet("""
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
        
        # 清空按钮
        self.clear_button = QPushButton("🗑️ " + tr("Clear"))
        self.clear_button.setToolTip(tr("Clear copywriting content"))
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
        
        # 重新生成按钮
        self.regenerate_button = QPushButton("🔄 " + tr("Regenerate"))
        self.regenerate_button.setToolTip(tr("Regenerate copywriting"))
        self.regenerate_button.clicked.connect(self.request_regenerate)
        self.regenerate_button.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e8660c;
            }
            QPushButton:pressed {
                background-color: #d65a00;
            }
        """)
        
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.regenerate_button)
        button_layout.addStretch()
        
        parent_layout.addLayout(button_layout)
        
    def create_progress_bar(self, parent_layout):
        """创建进度条"""
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)  # 初始隐藏
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e9ecef;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                color: white;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4a90e2, stop: 1 #357abd);
                border-radius: 3px;
            }
        """)
        
        parent_layout.addWidget(self.progress_bar)
        
    def create_result_editor(self, parent_layout):
        """创建结果编辑器"""
        # 状态标签
        self.status_label = QLabel(tr("AI generated copywriting will appear here"))
        self.status_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                padding: 5px;
                font-style: italic;
            }
        """)
        parent_layout.addWidget(self.status_label)
        
        # 文案编辑器
        self.result_edit = QTextEdit()
        self.result_edit.setPlaceholderText(tr("Generated copywriting will appear here..."))
        self.result_edit.setMinimumHeight(300)
        self.result_edit.textChanged.connect(self.on_text_changed)
        self.result_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 15px;
                font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                background-color: white;
                color: #212529;
            }
            QTextEdit:focus {
                border-color: #4a90e2;
                outline: none;
            }
        """)
        
        parent_layout.addWidget(self.result_edit)
        
    def create_statistics(self, parent_layout):
        """创建统计信息"""
        stats_layout = QHBoxLayout()
        
        # 字数统计
        self.word_count_label = QLabel("字数: 0")
        self.word_count_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                padding: 2px 8px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 3px;
            }
        """)
        
        # 字符统计
        self.char_count_label = QLabel("字符数: 0")
        self.char_count_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                padding: 2px 8px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 3px;
            }
        """)
        
        # 最后更新时间
        self.last_updated_label = QLabel("最后更新: --")
        self.last_updated_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                padding: 2px 8px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 3px;
            }
        """)
        
        stats_layout.addWidget(self.word_count_label)
        stats_layout.addWidget(self.char_count_label)
        stats_layout.addWidget(self.last_updated_label)
        stats_layout.addStretch()
        
        parent_layout.addLayout(stats_layout)
        
    def show_generating_progress(self, show=True):
        """显示/隐藏生成进度"""
        if show:
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # 无限进度条
            self.progress_bar.setFormat("正在生成AI文案...")
            self.regenerate_button.setEnabled(False)
        else:
            self.progress_bar.setVisible(False)
            self.regenerate_button.setEnabled(True)
            
    def set_copywriting(self, content):
        """设置文案内容"""
        self.result_edit.setPlainText(content)
        if content.strip():
            self.update_last_updated()
            self.status_label.setText("✅ " + tr("Copywriting generated successfully"))
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #28a745;
                    font-size: 12px;
                    padding: 5px;
                    font-weight: bold;
                }
            """)
        else:
            self.status_label.setText(tr("AI generated copywriting will appear here"))
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #6c757d;
                    font-size: 12px;
                    padding: 5px;
                    font-style: italic;
                }
            """)
            
    def get_copywriting(self):
        """获取文案内容"""
        return self.result_edit.toPlainText().strip()
        
    def append_text(self, text):
        """追加文本（用于流式生成）"""
        cursor = self.result_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text)
        self.result_edit.setTextCursor(cursor)
        self.result_edit.ensureCursorVisible()
        
    def on_text_changed(self):
        """文本改变处理"""
        content = self.result_edit.toPlainText()
        word_count = len(content.split()) if content.strip() else 0
        char_count = len(content)
        
        self.word_count_label.setText(f"字数: {word_count}")
        self.char_count_label.setText(f"字符数: {char_count}")
        
        # 发送信号
        self.copywriting_changed.emit(content)
        
    def copy_to_clipboard(self):
        """复制到剪贴板"""
        content = self.get_copywriting()
        if content:
            from PyQt6.QtGui import QGuiApplication
            clipboard = QGuiApplication.clipboard()
            clipboard.setText(content)
            self.show_temporary_message("已复制到剪贴板", success=True)
        else:
            QMessageBox.warning(self, "警告", "没有内容可以复制")
            
    def save_to_file(self):
        """保存到文件"""
        content = self.get_copywriting()
        if not content:
            QMessageBox.warning(self, "警告", "没有内容需要保存")
            return
            
        # 生成默认文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"copywriting_{timestamp}.txt"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("Save Copywriting"),
            default_filename,
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.show_temporary_message(f"已保存到: {os.path.basename(file_path)}", success=True)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件失败: {str(e)}")
                
    def clear_content(self):
        """清空内容"""
        if self.get_copywriting():
            reply = QMessageBox.question(
                self,
                "确认清空",
                "确定要清空当前文案内容吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.result_edit.clear()
                self.show_temporary_message("已清空文案内容", success=True)
        else:
            QMessageBox.information(self, "提示", "当前没有内容需要清空")
            
    def request_regenerate(self):
        """请求重新生成"""
        # 这里会发送信号给父组件来重新生成
        self.parent().parent().parent().generate_copywriting()
        
    def update_last_updated(self):
        """更新最后更新时间"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.last_updated_label.setText(f"最后更新: {current_time}")
        
    def show_temporary_message(self, message, success=True, duration=3000):
        """显示临时消息"""
        color = "#28a745" if success else "#dc3545"
        self.status_label.setText(f"{'✅' if success else '❌'} {message}")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 12px;
                padding: 5px;
                font-weight: bold;
            }}
        """)
        
        # 设置定时器恢复默认状态
        QTimer.singleShot(duration, self.reset_status_message)
        
    def reset_status_message(self):
        """重置状态消息"""
        if self.get_copywriting():
            self.status_label.setText("✅ " + tr("Copywriting generated successfully"))
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #28a745;
                    font-size: 12px;
                    padding: 5px;
                    font-weight: bold;
                }
            """)
        else:
            self.status_label.setText(tr("AI generated copywriting will appear here"))
            self.status_label.setStyleSheet("""
                QLabel {
                    color: #6c757d;
                    font-size: 12px;
                    padding: 5px;
                    font-style: italic;
                }
            """)
            
    def update_text(self):
        """更新界面文本（多语言支持）"""
        # 更新按钮文本
        self.copy_button.setText("📋 " + tr("Copy"))
        self.save_button.setText("💾 " + tr("Save"))
        self.clear_button.setText("🗑️ " + tr("Clear"))
        self.regenerate_button.setText("🔄 " + tr("Regenerate"))
        
        # 更新工具提示
        self.copy_button.setToolTip(tr("Copy copywriting to clipboard"))
        self.save_button.setToolTip(tr("Save copywriting to file"))
        self.clear_button.setToolTip(tr("Clear copywriting content"))
        self.regenerate_button.setToolTip(tr("Regenerate copywriting"))
        
        # 更新占位符
        self.result_edit.setPlaceholderText(tr("Generated copywriting will appear here..."))