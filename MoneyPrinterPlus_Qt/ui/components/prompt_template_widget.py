"""
提示词模板组件 - 管理AI文案生成的提示词模板
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QGroupBox, QComboBox,
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.translator import tr

class PromptTemplateWidget(QWidget):
    """提示词模板组件"""
    
    # 信号：模板改变
    template_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_default_templates()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # 创建分组框
        group_box = QGroupBox(tr("Prompt Template"))
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
        
        # 模板选择和操作按钮
        self.create_template_controls(group_layout)
        
        # 模板编辑器
        self.create_template_editor(group_layout)
        
        layout.addWidget(group_box)
        
    def create_template_controls(self, parent_layout):
        """创建模板控制器"""
        control_layout = QHBoxLayout()
        control_layout.setSpacing(10)
        
        # 模板选择下拉框
        template_label = QLabel(tr("Template:"))
        template_label.setStyleSheet("QLabel { font-weight: bold; }")
        
        self.template_combo = QComboBox()
        self.template_combo.setMinimumWidth(200)
        self.template_combo.currentTextChanged.connect(self.on_template_selected)
        self.template_combo.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                border: 2px solid #e9ecef;
                border-radius: 4px;
                background-color: white;
                color: #212529;
                font-size: 13px;
            }
            QComboBox:focus {
                border-color: #4a90e2;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                width: 0;
                height: 0;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
            }
        """)
        
        # 重置按钮
        self.reset_button = QPushButton("🔄 " + tr("Reset"))
        self.reset_button.setToolTip(tr("Reset to default template"))
        self.reset_button.clicked.connect(self.reset_template)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        
        # 导入按钮
        self.import_button = QPushButton("📥 " + tr("Import"))
        self.import_button.setToolTip(tr("Import template from file"))
        self.import_button.clicked.connect(self.import_template)
        self.import_button.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 6px 12px;
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
        
        # 导出按钮
        self.export_button = QPushButton("📤 " + tr("Export"))
        self.export_button.setToolTip(tr("Export template to file"))
        self.export_button.clicked.connect(self.export_template)
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #fd7e14;
                color: white;
                border: none;
                padding: 6px 12px;
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
        
        control_layout.addWidget(template_label)
        control_layout.addWidget(self.template_combo)
        control_layout.addWidget(self.reset_button)
        control_layout.addWidget(self.import_button)
        control_layout.addWidget(self.export_button)
        control_layout.addStretch()
        
        parent_layout.addLayout(control_layout)
        
    def create_template_editor(self, parent_layout):
        """创建模板编辑器"""
        # 说明标签
        info_label = QLabel("💡 " + tr("Customize your AI copywriting prompt template"))
        info_label.setStyleSheet("""
            QLabel {
                color: #17a2b8;
                font-size: 12px;
                padding: 5px;
                background-color: #d1ecf1;
                border: 1px solid #bee5eb;
                border-radius: 4px;
            }
        """)
        parent_layout.addWidget(info_label)
        
        # 模板编辑器
        self.template_edit = QTextEdit()
        self.template_edit.setPlaceholderText(tr("Enter your prompt template here..."))
        self.template_edit.setMinimumHeight(300)
        self.template_edit.textChanged.connect(self.on_template_changed)
        self.template_edit.setStyleSheet("""
            QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 12px;
                font-family: "Consolas", "Monaco", monospace;
                font-size: 13px;
                line-height: 1.5;
                background-color: white;
                color: #212529;
            }
            QTextEdit:focus {
                border-color: #4a90e2;
                outline: none;
            }
        """)
        
        parent_layout.addWidget(self.template_edit)
        
        # 字符统计标签
        self.char_count_label = QLabel("字符数: 0")
        self.char_count_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 11px;
                padding: 2px 5px;
            }
        """)
        parent_layout.addWidget(self.char_count_label)
        
    def setup_default_templates(self):
        """设置默认模板"""
        self.templates = {
            "TikTok广告文案": """You are a professional TikTok advertising copywriter. Based on the following product information, create a natural, conversational TikTok advertising video script.

Product Information:
{product_info}

IMPORTANT: Your output must be in the EXACT same format as the example below - a continuous, natural speaking script without any sections, headings, or formatting. 

Example format (DO NOT use any other format):
I've been using it for a few weeks now and I'm obsessed. It's so easy to use. You just apply your toner as usual and then you use the silicone jelly brush to evenly apply a layer of mask. It forms a unique collagen film that acts as a protective barrier, locking in moisture like a fortress. It keeps your skin moisturized and soft throughout the day. It restores skin elasticity and fights sagging and dullness. You can leave it on overnight for best results or wait 15-20 minutes if you're in a hurry. It's so easy to use and it's so effective. I'm gonna link it below if you want to try it out. It's so affordable and it's so worth it. It's gonna make your skin look so much confident and radiant. So, go ahead and buy it now.

Requirements:
1. Write as if someone is speaking naturally to the camera (30-60 seconds of speech)
2. Start with personal experience/testimonial 
3. Explain how to use the product
4. Highlight key benefits and effects
5. End with strong call-to-action
6. Use casual, conversational language with contractions (I'm, it's, you're, etc.)
7. NO sections, headings, bullet points, or formatting - just continuous natural speech
8. Must sound authentic and spontaneous like a real person recommending a product

Generate ONLY the continuous speaking script - nothing else. Please respond in English only.""",

            "产品介绍文案": """请基于以下产品信息，创建一个专业的产品介绍文案：

产品信息：
{product_info}

要求：
1. 突出产品的核心卖点和优势
2. 使用吸引人的语言描述产品特点
3. 包含使用场景和用户体验
4. 添加合理的行动号召
5. 文案风格专业且易于理解
6. 长度控制在100-200字之内

请生成完整的产品介绍文案。""",

            "社交媒体文案": """基于以下产品信息，创建适合社交媒体的推广文案：

产品信息：
{product_info}

要求：
1. 语言轻松活泼，符合社交媒体风格
2. 包含相关的表情符号和话题标签
3. 突出产品的实用性和价值
4. 激发用户的分享欲望
5. 长度适中，适合快速阅读
6. 包含互动元素（如提问、号召等）

请生成完整的社交媒体文案。""",
            
            "自定义模板": ""
        }
        
        # 填充下拉框
        self.template_combo.addItems(list(self.templates.keys()))
        
        # 设置默认模板
        self.template_combo.setCurrentText("TikTok广告文案")
        self.template_edit.setPlainText(self.templates["TikTok广告文案"])
        
    def on_template_selected(self, template_name):
        """模板选择处理"""
        if template_name in self.templates:
            self.template_edit.setPlainText(self.templates[template_name])
            
    def on_template_changed(self):
        """模板改变处理"""
        content = self.template_edit.toPlainText()
        char_count = len(content)
        self.char_count_label.setText(f"字符数: {char_count}")
        
        # 发送信号
        self.template_changed.emit(content)
        
    def reset_template(self):
        """重置模板"""
        current_template = self.template_combo.currentText()
        if current_template in self.templates:
            self.template_edit.setPlainText(self.templates[current_template])
            
    def import_template(self):
        """导入模板"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("Import Prompt Template"),
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.template_edit.setPlainText(content)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入模板失败: {str(e)}")
                
    def export_template(self):
        """导出模板"""
        content = self.template_edit.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "警告", "没有内容需要导出")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("Export Prompt Template"),
            "prompt_template.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                QMessageBox.information(self, "成功", f"模板已导出到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出模板失败: {str(e)}")
                
    def get_template(self):
        """获取当前模板"""
        return self.template_edit.toPlainText().strip()
        
    def set_template(self, template):
        """设置模板"""
        self.template_edit.setPlainText(template)
        
    def update_text(self):
        """更新界面文本（多语言支持）"""
        # 更新按钮文本
        self.reset_button.setText("🔄 " + tr("Reset"))
        self.import_button.setText("📥 " + tr("Import"))
        self.export_button.setText("📤 " + tr("Export"))
        
        # 更新工具提示
        self.reset_button.setToolTip(tr("Reset to default template"))
        self.import_button.setToolTip(tr("Import template from file"))
        self.export_button.setToolTip(tr("Export template to file"))
        
        # 更新占位符
        self.template_edit.setPlaceholderText(tr("Enter your prompt template here..."))