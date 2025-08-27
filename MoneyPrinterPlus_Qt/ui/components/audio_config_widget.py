"""
音频服务配置组件
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QLabel, QLineEdit, QGroupBox, QGridLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer

from core.config_manager import config_manager, AUDIO_PROVIDERS
from core.translator import tr

class AudioConfigWidget(QWidget):
    def __init__(self):
        super().__init__()
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
        provider_label = QLabel(tr("Remote Audio Provider"))
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
        self.provider_combo.addItems(AUDIO_PROVIDERS)
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
        
        # Azure配置
        self.azure_group = self.create_azure_config()
        config_layout.addWidget(self.azure_group)
        
        # Ali配置
        self.ali_group = self.create_ali_config()
        config_layout.addWidget(self.ali_group)
        
        # Tencent配置
        self.tencent_group = self.create_tencent_config()
        config_layout.addWidget(self.tencent_group)
        
        parent_layout.addWidget(self.config_container)
    
    def create_azure_config(self):
        """创建Azure配置"""
        group = QGroupBox("Azure")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout(group)
        
        # 信息提示
        info_label = QLabel(tr("Audio Azure config"))
        info_label.setStyleSheet(self.get_info_style())
        layout.addWidget(info_label)
        
        # 配置表单
        form_layout = QGridLayout()
        
        # Speech Key
        form_layout.addWidget(QLabel(tr("Speech Key")), 0, 0)
        self.azure_speech_key = QLineEdit()
        self.azure_speech_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.azure_speech_key.setStyleSheet(self.get_input_style())
        self.azure_speech_key.textChanged.connect(
            lambda text: self.save_audio_config('Azure', 'speech_key', text)
        )
        form_layout.addWidget(self.azure_speech_key, 0, 1)
        
        # Service Region
        form_layout.addWidget(QLabel(tr("Service Region")), 0, 2)
        self.azure_service_region = QLineEdit()
        self.azure_service_region.setEchoMode(QLineEdit.EchoMode.Password)
        self.azure_service_region.setStyleSheet(self.get_input_style())
        self.azure_service_region.textChanged.connect(
            lambda text: self.save_audio_config('Azure', 'service_region', text)
        )
        form_layout.addWidget(self.azure_service_region, 0, 3)
        
        layout.addLayout(form_layout)
        return group
    
    def create_ali_config(self):
        """创建Ali配置"""
        group = QGroupBox("Ali")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout(group)
        
        # 信息提示
        info_label = QLabel(tr("Audio Ali config"))
        info_label.setStyleSheet(self.get_info_style())
        layout.addWidget(info_label)
        
        # 配置表单
        form_layout = QGridLayout()
        
        # Access Key ID
        form_layout.addWidget(QLabel(tr("Access Key ID")), 0, 0)
        self.ali_access_key_id = QLineEdit()
        self.ali_access_key_id.setEchoMode(QLineEdit.EchoMode.Password)
        self.ali_access_key_id.setStyleSheet(self.get_input_style())
        self.ali_access_key_id.textChanged.connect(
            lambda text: self.save_audio_config('Ali', 'access_key_id', text)
        )
        form_layout.addWidget(self.ali_access_key_id, 0, 1)
        
        # Access Key Secret
        form_layout.addWidget(QLabel(tr("Access Key Secret")), 1, 0)
        self.ali_access_key_secret = QLineEdit()
        self.ali_access_key_secret.setEchoMode(QLineEdit.EchoMode.Password)
        self.ali_access_key_secret.setStyleSheet(self.get_input_style())
        self.ali_access_key_secret.textChanged.connect(
            lambda text: self.save_audio_config('Ali', 'access_key_secret', text)
        )
        form_layout.addWidget(self.ali_access_key_secret, 1, 1)
        
        # App Key
        form_layout.addWidget(QLabel(tr("App Key")), 2, 0)
        self.ali_app_key = QLineEdit()
        self.ali_app_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.ali_app_key.setStyleSheet(self.get_input_style())
        self.ali_app_key.textChanged.connect(
            lambda text: self.save_audio_config('Ali', 'app_key', text)
        )
        form_layout.addWidget(self.ali_app_key, 2, 1)
        
        layout.addLayout(form_layout)
        return group
    
    def create_tencent_config(self):
        """创建Tencent配置"""
        group = QGroupBox("Tencent")
        group.setStyleSheet(self.get_group_style())
        
        layout = QVBoxLayout(group)
        
        # 信息提示
        info_label = QLabel(tr("Audio Tencent config"))
        info_label.setStyleSheet(self.get_info_style())
        layout.addWidget(info_label)
        
        # 配置表单
        form_layout = QGridLayout()
        
        # Access Key ID
        form_layout.addWidget(QLabel(tr("Access Key ID")), 0, 0)
        self.tencent_access_key_id = QLineEdit()
        self.tencent_access_key_id.setEchoMode(QLineEdit.EchoMode.Password)
        self.tencent_access_key_id.setStyleSheet(self.get_input_style())
        self.tencent_access_key_id.textChanged.connect(
            lambda text: self.save_audio_config('Tencent', 'access_key_id', text)
        )
        form_layout.addWidget(self.tencent_access_key_id, 0, 1)
        
        # Access Key Secret
        form_layout.addWidget(QLabel(tr("Access Key Secret")), 1, 0)
        self.tencent_access_key_secret = QLineEdit()
        self.tencent_access_key_secret.setEchoMode(QLineEdit.EchoMode.Password)
        self.tencent_access_key_secret.setStyleSheet(self.get_input_style())
        self.tencent_access_key_secret.textChanged.connect(
            lambda text: self.save_audio_config('Tencent', 'access_key_secret', text)
        )
        form_layout.addWidget(self.tencent_access_key_secret, 1, 1)
        
        # App ID
        form_layout.addWidget(QLabel("App ID"), 2, 0)
        self.tencent_app_key = QLineEdit()
        self.tencent_app_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.tencent_app_key.setStyleSheet(self.get_input_style())
        self.tencent_app_key.textChanged.connect(
            lambda text: self.save_audio_config('Tencent', 'app_key', text)
        )
        form_layout.addWidget(self.tencent_app_key, 2, 1)
        
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
        current_provider = config_manager.get_audio_provider()
        index = self.provider_combo.findText(current_provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        
        # 加载各提供商配置
        self.load_azure_config()
        self.load_ali_config()
        self.load_tencent_config()
        
        # 显示当前提供商配置
        self.show_current_provider_config()
    
    def load_azure_config(self):
        """加载Azure配置"""
        config = config_manager.get_audio_config('Azure')
        self.azure_speech_key.setText(config.get('speech_key', ''))
        self.azure_service_region.setText(config.get('service_region', ''))
    
    def load_ali_config(self):
        """加载Ali配置"""
        config = config_manager.get_audio_config('Ali')
        self.ali_access_key_id.setText(config.get('access_key_id', ''))
        self.ali_access_key_secret.setText(config.get('access_key_secret', ''))
        self.ali_app_key.setText(config.get('app_key', ''))
    
    def load_tencent_config(self):
        """加载Tencent配置"""
        config = config_manager.get_audio_config('Tencent')
        self.tencent_access_key_id.setText(config.get('access_key_id', ''))
        self.tencent_access_key_secret.setText(config.get('access_key_secret', ''))
        self.tencent_app_key.setText(config.get('app_key', ''))
    
    def on_provider_changed(self, provider):
        """提供商改变处理"""
        config_manager.set_audio_provider(provider)
        self.show_current_provider_config()
    
    def show_current_provider_config(self):
        """显示当前提供商配置"""
        current_provider = self.provider_combo.currentText()
        
        # 隐藏所有配置组
        self.azure_group.setVisible(False)
        self.ali_group.setVisible(False)
        self.tencent_group.setVisible(False)
        
        # 显示当前提供商配置
        if current_provider == 'Azure':
            self.azure_group.setVisible(True)
        elif current_provider == 'Ali':
            self.ali_group.setVisible(True)
        elif current_provider == 'Tencent':
            self.tencent_group.setVisible(True)
    
    def save_audio_config(self, provider, key, value):
        """保存音频配置"""
        config_manager.update_nested_config('audio', provider, key, value, auto_save=False)
        # 延迟保存，避免频繁写入
        self.save_timer.start()
    
    def _delayed_save(self):
        """延迟保存配置"""
        config_manager.save_config()
    
    def update_text(self):
        """更新界面文本"""
        # 更新标签文本
        for child in self.findChildren(QLabel):
            # 根据需要更新特定标签的文本
            pass