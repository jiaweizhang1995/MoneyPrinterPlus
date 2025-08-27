"""
LLM配置组件
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                             QLabel, QLineEdit, QGroupBox, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer

from core.config_manager import config_manager, LLM_PROVIDERS
from core.translator import tr

class LLMConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_config_widget = None
        
        # 延迟保存定时器
        self.save_timer = QTimer()
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self._delayed_save)
        self.save_timer.setInterval(1000)  # 1秒延迟
        
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # 提供商选择区域
        self.create_provider_selection(layout)
        
        # 配置详情区域
        self.create_config_details(layout)
    
    def create_provider_selection(self, parent_layout):
        """创建提供商选择区域"""
        provider_frame = QFrame()
        provider_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        
        provider_layout = QHBoxLayout(provider_frame)
        
        # 标签
        provider_label = QLabel(tr("LLM Provider"))
        provider_label.setMinimumWidth(150)
        provider_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #333;
                background: transparent;
                border: none;
            }
        """)
        
        # 提供商下拉框
        self.provider_combo = QComboBox()
        self.provider_combo.setMinimumWidth(200)
        self.provider_combo.addItems(LLM_PROVIDERS)
        self.provider_combo.setStyleSheet("""
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
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                color: #212529;
                selection-background-color: #4a90e2;
                selection-color: white;
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
        
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        
        provider_layout.addWidget(provider_label)
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        
        parent_layout.addWidget(provider_frame)
    
    def create_config_details(self, parent_layout):
        """创建配置详情区域"""
        # 配置容器
        self.config_container = QWidget()
        config_layout = QVBoxLayout(self.config_container)
        config_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建各提供商配置组
        self.config_groups = {}
        for provider in LLM_PROVIDERS:
            group = self.create_provider_config(provider)
            self.config_groups[provider] = group
            config_layout.addWidget(group)
            group.setVisible(False)  # 初始隐藏
        
        parent_layout.addWidget(self.config_container)
    
    def create_provider_config(self, provider):
        """创建提供商配置"""
        group = QGroupBox(provider)
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout(group)
        
        # 信息提示
        info_label = QLabel(f"{provider} 配置信息")
        info_label.setStyleSheet(self.get_info_style())
        layout.addWidget(info_label)
        
        # 配置表单
        form_layout = QGridLayout()
        row = 0
        
        # API Key (除了Ollama外都需要)
        if provider != 'Ollama':
            form_layout.addWidget(QLabel(tr("API Key")), row, 0)
            api_key_input = QLineEdit()
            api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            api_key_input.setStyleSheet(self.get_input_style())
            api_key_input.textChanged.connect(
                lambda text, p=provider: self.save_llm_config(p, 'api_key', text)
            )
            form_layout.addWidget(api_key_input, row, 1)
            setattr(self, f"{provider.lower()}_api_key", api_key_input)
            row += 1
        
        # Secret Key (仅Qianfan需要)
        if provider == 'Qianfan':
            form_layout.addWidget(QLabel(tr("Secret Key")), row, 0)
            secret_key_input = QLineEdit()
            secret_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            secret_key_input.setStyleSheet(self.get_input_style())
            secret_key_input.textChanged.connect(
                lambda text, p=provider: self.save_llm_config(p, 'secret_key', text)
            )
            form_layout.addWidget(secret_key_input, row, 1)
            setattr(self, f"{provider.lower()}_secret_key", secret_key_input)
            row += 1
        
        # Base URL (Azure, DeepSeek, Ollama需要)
        if provider in ['Azure', 'DeepSeek', 'Ollama']:
            form_layout.addWidget(QLabel(tr("Base Url")), row, 0)
            base_url_input = QLineEdit()
            if provider != 'Ollama':
                base_url_input.setEchoMode(QLineEdit.EchoMode.Password)
            base_url_input.setStyleSheet(self.get_input_style())
            base_url_input.textChanged.connect(
                lambda text, p=provider: self.save_llm_config(p, 'base_url', text)
            )
            form_layout.addWidget(base_url_input, row, 1)
            setattr(self, f"{provider.lower()}_base_url", base_url_input)
            row += 1
        
        # Model Name (所有提供商都需要)
        form_layout.addWidget(QLabel(tr("Model Name")), row, 0)
        model_name_input = QLineEdit()
        model_name_input.setStyleSheet(self.get_input_style())
        model_name_input.textChanged.connect(
            lambda text, p=provider: self.save_llm_config(p, 'model_name', text)
        )
        form_layout.addWidget(model_name_input, row, 1)
        setattr(self, f"{provider.lower()}_model_name", model_name_input)
        
        layout.addLayout(form_layout)
        return group
    
    def get_group_style(self):
        """获取组框样式"""
        return """
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 2px solid #d0d0d0;
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px 0 6px;
                background-color: white;
                color: #4a90e2;
            }
        """
    
    def get_info_style(self):
        """获取信息提示样式"""
        return """
            QLabel {
                background-color: #e8f4fd;
                border: 1px solid #bee5eb;
                border-radius: 4px;
                padding: 8px 12px;
                color: #0c5460;
                font-size: 12px;
            }
        """
    
    def get_input_style(self):
        """获取输入框样式"""
        return """
            QLineEdit {
                padding: 8px 12px;
                font-size: 13px;
                border: 2px solid #e0e0e0;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                outline: none;
            }
            QLineEdit:hover {
                border-color: #4a90e2;
            }
        """
    
    def load_config(self):
        """加载配置"""
        # 设置当前提供商
        current_provider = config_manager.get_llm_provider()
        index = self.provider_combo.findText(current_provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        
        # 加载各提供商配置
        for provider in LLM_PROVIDERS:
            self.load_provider_config(provider)
        
        # 显示当前提供商配置
        self.show_current_provider_config()
    
    def load_provider_config(self, provider):
        """加载提供商配置"""
        config = config_manager.get_llm_config(provider)
        
        # API Key
        if hasattr(self, f"{provider.lower()}_api_key"):
            widget = getattr(self, f"{provider.lower()}_api_key")
            widget.setText(config.get('api_key', ''))
        
        # Secret Key (Qianfan)
        if hasattr(self, f"{provider.lower()}_secret_key"):
            widget = getattr(self, f"{provider.lower()}_secret_key")
            widget.setText(config.get('secret_key', ''))
        
        # Base URL
        if hasattr(self, f"{provider.lower()}_base_url"):
            widget = getattr(self, f"{provider.lower()}_base_url")
            widget.setText(config.get('base_url', ''))
        
        # Model Name
        if hasattr(self, f"{provider.lower()}_model_name"):
            widget = getattr(self, f"{provider.lower()}_model_name")
            widget.setText(config.get('model_name', ''))
    
    def on_provider_changed(self, provider):
        """提供商改变处理"""
        config_manager.set_llm_provider(provider)
        self.show_current_provider_config()
    
    def show_current_provider_config(self):
        """显示当前提供商配置"""
        current_provider = self.provider_combo.currentText()
        
        # 隐藏所有配置组
        for provider, group in self.config_groups.items():
            group.setVisible(provider == current_provider)
    
    def save_llm_config(self, provider, key, value):
        """保存LLM配置"""
        config_manager.update_nested_config('llm', provider, key, value, auto_save=False)
        # 延迟保存，避免频繁写入
        self.save_timer.start()
    
    def _delayed_save(self):
        """延迟保存配置"""
        config_manager.save_config()
    
    def update_text(self):
        """更新界面文本"""
        # 更新标签文本
        pass