"""
AI文案生成组件 - 主要的AI文案生成界面
"""
import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
                             QPushButton, QLabel, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QFont

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 从 ui/components/ 到 MoneyPrinterPlus_Qt/ 需要两个上级目录
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from core.translator import tr
from core.config_manager import config_manager
from ui.components.product_info_widget import ProductInfoWidget
from ui.components.prompt_template_widget import PromptTemplateWidget
from ui.components.copywriting_result_widget import CopywritingResultWidget

# 导入PyQt6专用的LLM服务
try:
    # 确保正确的导入路径
    sys.path.insert(0, project_root)
    from services.llm.llm_provider_qt import get_llm_provider
    LLM_AVAILABLE = True
    print("SUCCESS: LLM services available")
except ImportError as e:
    LLM_AVAILABLE = False
    print(f"Warning: LLM services not available - {e}")

class CopywritingGenerationThread(QThread):
    """文案生成线程"""
    
    # 信号
    generation_finished = pyqtSignal(str)  # 生成完成
    generation_error = pyqtSignal(str)     # 生成错误
    generation_progress = pyqtSignal(str)  # 生成进度
    
    def __init__(self, product_info, template):
        super().__init__()
        self.product_info = product_info
        self.template = template
        
        
    def run(self):
        """运行生成任务"""
        try:
            self.generation_progress.emit("正在连接AI服务...")
            
            # 检查配置
            llm_provider = config_manager.get_llm_provider()
            if not llm_provider:
                self.generation_error.emit("请先配置LLM服务提供商")
                return
            
            # 检查通义千问API密钥配置
            llm_config = config_manager.get_llm_config('Tongyi')
            api_key = llm_config.get('api_key', '')
            model_name = llm_config.get('model_name', '')
            
            if not api_key or api_key == 'YOUR_API_KEY':
                self.generation_error.emit("请先在基本配置中设置通义千问API Key")
                return
                
            if not model_name:
                self.generation_error.emit("请先在基本配置中设置通义千问模型名称")
                return
            
            # 检查LLM服务是否可用
            if not LLM_AVAILABLE:
                self.generation_error.emit("LLM服务不可用，请检查环境依赖")
                return
            
            # 实际通义千问生成逻辑
            self.generation_progress.emit("正在准备提示词...")
            
            # 获取LLM服务
            llm_service = get_llm_provider(llm_provider)
            
            self.generation_progress.emit("正在调用通义千问服务...")
            
            # 格式化模板
            formatted_template = self.template.format(product_info=self.product_info)
            
            self.generation_progress.emit("正在生成文案...")
            
            # 调用真实的LLM服务
            from langchain_core.prompts import PromptTemplate
            prompt_template = PromptTemplate.from_template(formatted_template)
            
            result = llm_service.generate_content(
                topic="",
                prompt_template=prompt_template,
                language="en"
            )
            
            self.generation_finished.emit(result.strip())
            
        except Exception as e:
            self.generation_error.emit(f"生成失败: {str(e)}")

class AICopywritingWidget(QWidget):
    """AI文案生成主组件"""
    
    def __init__(self):
        super().__init__()
        self.generation_thread = None
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建分割器
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧面板 - 产品信息和模板
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右侧面板 - 结果显示
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # 设置分割器比例 (左:右 = 1:1)
        main_splitter.setSizes([500, 500])
        main_splitter.setChildrenCollapsible(False)
        
        layout.addWidget(main_splitter)
        
        # 底部生成按钮
        self.create_generate_section(layout)
        
    def create_left_panel(self, parent=None):
        """创建左侧面板"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(10, 10, 5, 10)
        left_layout.setSpacing(15)
        
        # 产品信息组件
        self.product_info_widget = ProductInfoWidget()
        left_layout.addWidget(self.product_info_widget)
        
        # 提示词模板组件
        self.prompt_template_widget = PromptTemplateWidget()
        left_layout.addWidget(self.prompt_template_widget)
        
        return left_widget
        
    def create_right_panel(self, parent=None):
        """创建右侧面板"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 10, 10, 10)
        right_layout.setSpacing(15)
        
        # 文案结果组件
        self.copywriting_result_widget = CopywritingResultWidget()
        right_layout.addWidget(self.copywriting_result_widget)
        
        return right_widget
        
    def create_generate_section(self, parent_layout):
        """创建生成区域"""
        generate_frame = QFrame()
        generate_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-top: 2px solid #e9ecef;
                padding: 15px;
            }
        """)
        
        generate_layout = QHBoxLayout(generate_frame)
        generate_layout.setContentsMargins(20, 15, 20, 15)
        
        # 状态信息
        self.status_info = QLabel("💡 " + tr("Configure product information and template, then click generate"))
        self.status_info.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        
        generate_layout.addWidget(self.status_info)
        generate_layout.addStretch()
        
        # 生成按钮
        self.generate_button = QPushButton("✨ " + tr("Generate AI Copywriting"))
        self.generate_button.setMinimumSize(200, 45)
        self.generate_button.clicked.connect(self.generate_copywriting)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #4a90e2, stop: 1 #357abd);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #357abd, stop: 1 #2c5aa0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #2c5aa0, stop: 1 #1a365d);
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
        """)
        
        generate_layout.addWidget(self.generate_button)
        
        parent_layout.addWidget(generate_frame)
        
    def connect_signals(self):
        """连接信号"""
        # 产品信息变化
        self.product_info_widget.product_info_changed.connect(self.update_generate_button_state)
        
        # 模板变化
        self.prompt_template_widget.template_changed.connect(self.update_generate_button_state)
        
        # 初始状态更新
        self.update_generate_button_state()
        
    def update_generate_button_state(self):
        """更新生成按钮状态"""
        product_info = self.product_info_widget.get_product_info()
        template = self.prompt_template_widget.get_template()
        
        has_product_info = bool(product_info.strip())
        has_template = bool(template.strip())
        
        if has_product_info and has_template:
            self.generate_button.setEnabled(True)
            self.status_info.setText("✅ " + tr("Ready to generate copywriting"))
            self.status_info.setStyleSheet("""
                QLabel {
                    color: #28a745;
                    font-size: 14px;
                    font-weight: 500;
                }
            """)
        else:
            self.generate_button.setEnabled(False)
            missing = []
            if not has_product_info:
                missing.append(tr("product information"))
            if not has_template:
                missing.append(tr("prompt template"))
                
            self.status_info.setText("⚠️ " + tr("Please provide: ") + ", ".join(missing))
            self.status_info.setStyleSheet("""
                QLabel {
                    color: #dc3545;
                    font-size: 14px;
                    font-weight: 500;
                }
            """)
            
    def generate_copywriting(self):
        """生成文案"""
        if self.generation_thread and self.generation_thread.isRunning():
            QMessageBox.information(self, "提示", "正在生成中，请稍等...")
            return
            
        product_info = self.product_info_widget.get_product_info()
        template = self.prompt_template_widget.get_template()
        
        if not product_info.strip():
            QMessageBox.warning(self, "警告", "请先输入产品信息")
            return
            
        if not template.strip():
            QMessageBox.warning(self, "警告", "请先配置提示词模板")
            return
            
        # 检查通义千问配置
        llm_provider = config_manager.get_llm_provider()
        if not llm_provider:
            QMessageBox.warning(self, "警告", "请先在基本配置中设置LLM服务提供商")
            return
            
        # 检查API Key配置
        llm_config = config_manager.get_llm_config('Tongyi')
        api_key = llm_config.get('api_key', '')
        model_name = llm_config.get('model_name', '')
        
        if not api_key or api_key == 'YOUR_API_KEY':
            QMessageBox.warning(self, "配置错误", 
                "通义千问API Key未配置，无法生成文案！\n\n"
                "请先完成配置：\n"
                "1. 点击左侧导航的'基本配置'\n"  
                "2. 在'LLM大模型配置'中设置通义千问API Key\n"
                "3. 重新回到此页面生成文案")
            return
            
        if not model_name:
            QMessageBox.warning(self, "配置错误", 
                "通义千问模型名称未配置！\n\n"
                "请在基本配置中设置模型名称（如：qwen-turbo）")
            return
                
        # 开始生成
        self.start_generation(product_info, template)
        
    def start_generation(self, product_info, template):
        """开始生成"""
        # 创建生成线程
        self.generation_thread = CopywritingGenerationThread(product_info, template)
        self.generation_thread.generation_finished.connect(self.on_generation_finished)
        self.generation_thread.generation_error.connect(self.on_generation_error)
        self.generation_thread.generation_progress.connect(self.on_generation_progress)
        
        # 更新UI状态
        self.generate_button.setEnabled(False)
        self.copywriting_result_widget.show_generating_progress(True)
        
        # 开始生成
        self.generation_thread.start()
        
    @pyqtSlot(str)
    def on_generation_finished(self, result):
        """生成完成"""
        self.generate_button.setEnabled(True)
        self.copywriting_result_widget.show_generating_progress(False)
        self.copywriting_result_widget.set_copywriting(result)
        
        self.status_info.setText("🎉 " + tr("Copywriting generated successfully!"))
        self.status_info.setStyleSheet("""
            QLabel {
                color: #28a745;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
    @pyqtSlot(str)
    def on_generation_error(self, error_message):
        """生成错误"""
        self.generate_button.setEnabled(True)
        self.copywriting_result_widget.show_generating_progress(False)
        
        self.status_info.setText("❌ " + error_message)
        self.status_info.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        
        QMessageBox.critical(self, "生成失败", error_message)
        
    @pyqtSlot(str)
    def on_generation_progress(self, progress_message):
        """生成进度更新"""
        self.status_info.setText("⏳ " + progress_message)
        self.status_info.setStyleSheet("""
            QLabel {
                color: #17a2b8;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        
    def update_text(self):
        """更新界面文本（多语言支持）"""
        # 更新子组件文本
        self.product_info_widget.update_text()
        self.prompt_template_widget.update_text()
        self.copywriting_result_widget.update_text()
        
        # 更新按钮文本
        self.generate_button.setText("✨ " + tr("Generate AI Copywriting"))
        
        # 更新状态
        self.update_generate_button_state()