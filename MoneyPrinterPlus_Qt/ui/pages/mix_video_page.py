"""
视频混剪页面 - PyQt6版本
移植自原项目 pages/02_mix_video.py
"""
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, 
                             QGroupBox, QLabel, QCheckBox, QLineEdit, QPushButton,
                             QSlider, QComboBox, QSpinBox, QProgressBar, QTextEdit,
                             QFrame, QGridLayout, QSizePolicy, QFileDialog, QSpacerItem,
                             QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor

from core.config_manager import config_manager
from core.translator import tr

class MixVideoPage(QWidget):
    """视频混剪页面"""
    
    def __init__(self):
        super().__init__()
        self.scene_number = 4  # 默认场景数量
        self.scene_widgets = []  # 存储场景相关组件
        self.setup_ui()
        self.load_config()
        self.setup_connections()
    
    def setup_ui(self):
        """设置界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # 滚动内容容器
        scroll_content = QWidget()
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setContentsMargins(0, 0, 20, 0)  # 为滚动条留空间
        content_layout.setSpacing(15)
        
        # 添加各个配置组
        self.create_header(content_layout)
        self.create_full_audio_group(content_layout)
        self.create_scene_management_group(content_layout)
        self.create_video_config_group(content_layout)
        self.create_subtitle_group(content_layout)
        self.create_output_config_group(content_layout)
        self.create_video_generation_group(content_layout)
        self.create_usage_statistics_group(content_layout)
        
        # 设置滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        # 应用样式
        self.apply_styles()
    
    def create_header(self, layout):
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
        title_label = QLabel(tr("Mix Video"))
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
        subtitle_label = QLabel("配置视频混剪参数")
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
        layout.addWidget(header_frame)
    
    def create_full_audio_group(self, layout):
        """创建完整音频配置组"""
        group = QGroupBox("🎵 " + tr("Complete Audio Configuration"))
        group_layout = QVBoxLayout(group)
        
        # 完整音频复选框（默认启用）
        self.use_full_audio_cb = QCheckBox(tr("Use complete audio"))
        self.use_full_audio_cb.setChecked(True)  # 默认启用
        self.use_full_audio_cb.setToolTip(tr("Skip TTS synthesis and use MP3 audio files directly"))
        group_layout.addWidget(self.use_full_audio_cb)
        
        # 音频目录配置
        audio_dir_layout = QHBoxLayout()
        audio_dir_layout.addWidget(QLabel(tr("Audio directory:")))
        
        self.full_audio_dir_edit = QLineEdit()
        self.full_audio_dir_edit.setPlaceholderText(tr("Select directory containing MP3 files"))
        self.full_audio_dir_edit.setToolTip(tr("System will randomly select MP3 files from this directory"))
        audio_dir_layout.addWidget(self.full_audio_dir_edit, 1)
        
        self.audio_dir_browse_btn = QPushButton(tr("Browse"))
        self.audio_dir_browse_btn.clicked.connect(self.browse_audio_directory)
        audio_dir_layout.addWidget(self.audio_dir_browse_btn)
        
        group_layout.addLayout(audio_dir_layout)
        
        # 信息提示
        info_label = QLabel(tr("💡 Complete audio mode is enabled by default. Subtitle generation will be automatically disabled."))
        info_label.setStyleSheet("color: #007acc; font-style: italic; margin: 10px 0px;")
        info_label.setWordWrap(True)
        group_layout.addWidget(info_label)
        
        layout.addWidget(group)
    
    def create_scene_management_group(self, layout):
        """创建场景管理组"""
        group = QGroupBox("🎬 " + tr("Video Scene Management"))
        group_layout = QVBoxLayout(group)
        
        # 场景控制按钮
        scene_control_layout = QHBoxLayout()
        
        self.add_scene_btn = QPushButton(tr("Add Scene"))
        self.add_scene_btn.clicked.connect(self.add_scene)
        scene_control_layout.addWidget(self.add_scene_btn)
        
        self.delete_scene_btn = QPushButton(tr("Delete Scene"))
        self.delete_scene_btn.clicked.connect(self.delete_scene)
        scene_control_layout.addWidget(self.delete_scene_btn)
        
        scene_control_layout.addStretch()
        group_layout.addLayout(scene_control_layout)
        
        # 场景容器
        self.scenes_container = QWidget()
        self.scenes_layout = QVBoxLayout(self.scenes_container)
        self.scenes_layout.setContentsMargins(0, 10, 0, 0)
        
        # 初始化场景
        self.init_scenes()
        
        group_layout.addWidget(self.scenes_container)
        layout.addWidget(group)
    
    def create_video_config_group(self, layout):
        """创建视频配置组"""
        group = QGroupBox("📹 " + tr("Video Configuration"))
        group_layout = QGridLayout(group)
        
        # 视频布局
        group_layout.addWidget(QLabel(tr("Video layout:")), 0, 0)
        self.video_layout_combo = QComboBox()
        self.video_layout_combo.addItems([tr("Portrait"), tr("Landscape"), tr("Square")])
        self.video_layout_combo.setCurrentIndex(0)  # 默认竖屏
        group_layout.addWidget(self.video_layout_combo, 0, 1)
        
        # 视频帧率
        group_layout.addWidget(QLabel(tr("Video FPS:")), 0, 2)
        self.video_fps_combo = QComboBox()
        self.video_fps_combo.addItems(["20", "25", "30"])
        self.video_fps_combo.setCurrentIndex(1)  # 默认25fps
        group_layout.addWidget(self.video_fps_combo, 0, 3)
        
        # 视频分辨率
        group_layout.addWidget(QLabel(tr("Video size:")), 1, 0)
        self.video_size_combo = QComboBox()
        self.update_video_size_options()  # 根据布局更新分辨率选项
        group_layout.addWidget(self.video_size_combo, 1, 1)
        
        # 片段时长
        group_layout.addWidget(QLabel(tr("Min segment length:")), 1, 2)
        self.min_segment_spin = QSpinBox()
        self.min_segment_spin.setMinimum(5)
        self.min_segment_spin.setMaximum(10)
        self.min_segment_spin.setValue(5)
        self.min_segment_spin.setSuffix("s")
        group_layout.addWidget(self.min_segment_spin, 1, 3)
        
        group_layout.addWidget(QLabel(tr("Max segment length:")), 2, 0)
        self.max_segment_spin = QSpinBox()
        self.max_segment_spin.setMinimum(5)
        self.max_segment_spin.setMaximum(30)
        self.max_segment_spin.setValue(10)
        self.max_segment_spin.setSuffix("s")
        group_layout.addWidget(self.max_segment_spin, 2, 1)
        
        layout.addWidget(group)
    
    def create_subtitle_group(self, layout):
        """创建固定字幕配置组"""
        group = QGroupBox("📝 " + tr("Fixed Subtitle Configuration"))
        group_layout = QVBoxLayout(group)
        
        # 启用固定字幕
        self.enable_fixed_subtitles_cb = QCheckBox(tr("Enable fixed subtitles"))
        self.enable_fixed_subtitles_cb.setChecked(False)
        self.enable_fixed_subtitles_cb.setToolTip(tr("Load txt file and display subtitles from start to end"))
        group_layout.addWidget(self.enable_fixed_subtitles_cb)
        
        # 字幕文件选择
        subtitle_file_layout = QHBoxLayout()
        subtitle_file_layout.addWidget(QLabel(tr("Subtitle file:")))
        
        self.subtitle_file_edit = QLineEdit()
        self.subtitle_file_edit.setPlaceholderText(tr("Select txt subtitle file"))
        self.subtitle_file_edit.setToolTip(tr("UTF-8 encoded txt file, max 3 lines will be displayed"))
        subtitle_file_layout.addWidget(self.subtitle_file_edit, 1)
        
        self.subtitle_file_browse_btn = QPushButton(tr("Browse"))
        self.subtitle_file_browse_btn.clicked.connect(self.browse_subtitle_file)
        subtitle_file_layout.addWidget(self.subtitle_file_browse_btn)
        
        group_layout.addLayout(subtitle_file_layout)
        
        # 字幕样式配置
        style_layout = QGridLayout()
        
        # 字体
        style_layout.addWidget(QLabel(tr("Font:")), 0, 0)
        self.subtitle_font_combo = QComboBox()
        fonts = ["Arial", "Arial Bold", "Times New Roman", "Helvetica", "Verdana", "Calibri"]
        self.subtitle_font_combo.addItems(fonts)
        style_layout.addWidget(self.subtitle_font_combo, 0, 1)
        
        # 字体大小
        style_layout.addWidget(QLabel(tr("Font size:")), 0, 2)
        self.subtitle_size_spin = QSpinBox()
        self.subtitle_size_spin.setMinimum(20)
        self.subtitle_size_spin.setMaximum(100)
        self.subtitle_size_spin.setValue(48)
        self.subtitle_size_spin.setSuffix("px")
        style_layout.addWidget(self.subtitle_size_spin, 0, 3)
        
        # 字体颜色
        style_layout.addWidget(QLabel(tr("Font color:")), 1, 0)
        self.subtitle_color_btn = QPushButton()
        self.subtitle_color_btn.setStyleSheet("background-color: #FFFFFF; border: 1px solid #ccc;")
        self.subtitle_color_btn.setText("#FFFFFF")
        self.subtitle_color_btn.clicked.connect(self.choose_subtitle_color)
        style_layout.addWidget(self.subtitle_color_btn, 1, 1)
        
        # 行间距
        style_layout.addWidget(QLabel(tr("Line spacing:")), 1, 2)
        self.subtitle_line_spacing_spin = QSpinBox()
        self.subtitle_line_spacing_spin.setMinimum(10)
        self.subtitle_line_spacing_spin.setMaximum(100)
        self.subtitle_line_spacing_spin.setValue(40)
        self.subtitle_line_spacing_spin.setSuffix("px")
        style_layout.addWidget(self.subtitle_line_spacing_spin, 1, 3)
        
        group_layout.addLayout(style_layout)
        
        # 提示信息
        info_layout = QVBoxLayout()
        info_label = QLabel(tr("💡 Fixed subtitles will be displayed in the upper center of the video (randomly select max 3 lines)"))
        info_label.setStyleSheet("color: #007acc; font-style: italic; margin: 10px 0px;")
        info_label.setWordWrap(True)
        info_layout.addWidget(info_label)
        
        format_label = QLabel(tr("📄 File format: UTF-8 encoded txt file, system will randomly select up to 3 lines from the file"))
        format_label.setStyleSheet("color: #666; font-size: 12px; margin: 5px 0px;")
        format_label.setWordWrap(True)
        info_layout.addWidget(format_label)
        
        group_layout.addLayout(info_layout)
        layout.addWidget(group)
    
    def create_output_config_group(self, layout):
        """创建输出配置组"""
        group = QGroupBox("📁 " + tr("Output Configuration"))
        group_layout = QVBoxLayout(group)
        
        # 输出目录配置
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(QLabel(tr("Output directory:")))
        
        self.output_dir_edit = QLineEdit()
        # 设置默认输出目录
        default_output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../final"))
        self.output_dir_edit.setText(default_output_dir)
        self.output_dir_edit.setPlaceholderText(tr("Video save directory path"))
        output_dir_layout.addWidget(self.output_dir_edit, 1)
        
        self.output_dir_browse_btn = QPushButton(tr("Browse"))
        self.output_dir_browse_btn.clicked.connect(self.browse_output_directory)
        output_dir_layout.addWidget(self.output_dir_browse_btn)
        
        group_layout.addLayout(output_dir_layout)
        
        # 提示信息
        output_info = QLabel(tr("💡 Generated videos will be saved to the specified directory with date-based naming (YYYY-MM-DD_NN.mp4)"))
        output_info.setStyleSheet("color: #007acc; font-style: italic; margin: 10px 0px;")
        output_info.setWordWrap(True)
        group_layout.addWidget(output_info)
        
        layout.addWidget(group)
    
    def create_video_generation_group(self, layout):
        """创建视频生成控制组"""
        group = QGroupBox("🎬 " + tr("Video Generation"))
        group_layout = QVBoxLayout(group)
        
        # 生成数量控制
        generation_control_layout = QHBoxLayout()
        generation_control_layout.addWidget(QLabel(tr("Number of videos:")))
        
        self.videos_count_spin = QSpinBox()
        self.videos_count_spin.setMinimum(1)
        self.videos_count_spin.setMaximum(100)
        self.videos_count_spin.setValue(1)
        generation_control_layout.addWidget(self.videos_count_spin)
        
        generation_control_layout.addStretch()
        
        # 生成按钮
        self.generate_btn = QPushButton(tr("Generate Video"))
        self.generate_btn.setObjectName("primaryButton")
        self.generate_btn.clicked.connect(self.generate_video)
        generation_control_layout.addWidget(self.generate_btn)
        
        group_layout.addLayout(generation_control_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        group_layout.addWidget(self.progress_bar)
        
        # 状态显示
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setVisible(False)
        group_layout.addWidget(self.status_text)
        
        # 结果显示
        self.result_label = QLabel()
        self.result_label.setStyleSheet("color: #28a745; font-weight: bold; margin: 10px 0px;")
        self.result_label.setWordWrap(True)
        self.result_label.setVisible(False)
        group_layout.addWidget(self.result_label)
        
        layout.addWidget(group)
    
    def create_usage_statistics_group(self, layout):
        """创建视频使用统计组"""
        group = QGroupBox("📊 " + tr("Video Usage Statistics"))
        group_layout = QVBoxLayout(group)
        
        # 统计信息显示区域
        stats_layout = QHBoxLayout()
        
        # 总文件数
        self.total_files_label = QLabel("0")
        self.total_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_info_1 = QVBoxLayout()
        stats_info_1.addWidget(QLabel(tr("Total files")))
        stats_info_1.addWidget(self.total_files_label)
        stats_layout.addLayout(stats_info_1)
        
        # 可用文件数
        self.available_files_label = QLabel("0")
        self.available_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.available_files_label.setStyleSheet("color: #28a745; font-weight: bold;")
        stats_info_2 = QVBoxLayout()
        stats_info_2.addWidget(QLabel(tr("Available files")))
        stats_info_2.addWidget(self.available_files_label)
        stats_layout.addLayout(stats_info_2)
        
        # 已达上限文件数
        self.exceeded_files_label = QLabel("0")
        self.exceeded_files_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.exceeded_files_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        stats_info_3 = QVBoxLayout()
        stats_info_3.addWidget(QLabel(tr("Exceeded files")))
        stats_info_3.addWidget(self.exceeded_files_label)
        stats_layout.addLayout(stats_info_3)
        
        group_layout.addLayout(stats_layout)
        
        # 管理按钮
        management_layout = QHBoxLayout()
        
        self.refresh_stats_btn = QPushButton(tr("Refresh Statistics"))
        self.refresh_stats_btn.clicked.connect(self.refresh_statistics)
        management_layout.addWidget(self.refresh_stats_btn)
        
        self.reset_usage_btn = QPushButton(tr("Reset All Records"))
        self.reset_usage_btn.clicked.connect(self.reset_usage_records)
        management_layout.addWidget(self.reset_usage_btn)
        
        self.export_records_btn = QPushButton(tr("Export Records"))
        self.export_records_btn.clicked.connect(self.export_records)
        management_layout.addWidget(self.export_records_btn)
        
        management_layout.addStretch()
        group_layout.addLayout(management_layout)
        
        # 警告提示
        self.usage_warning_label = QLabel()
        self.usage_warning_label.setStyleSheet("color: #dc3545; font-weight: bold; margin: 10px 0px;")
        self.usage_warning_label.setWordWrap(True)
        self.usage_warning_label.setVisible(False)
        group_layout.addWidget(self.usage_warning_label)
        
        layout.addWidget(group)
    
    def init_scenes(self):
        """初始化场景"""
        for i in range(self.scene_number):
            self.add_scene_widget(i + 1)
    
    def add_scene_widget(self, scene_num):
        """添加场景组件"""
        scene_frame = QFrame()
        scene_frame.setFrameShape(QFrame.Shape.StyledPanel)
        scene_frame.setFrameShadow(QFrame.Shadow.Raised)
        scene_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
                background-color: white;
            }
        """)
        
        scene_layout = QVBoxLayout(scene_frame)
        
        # 场景标题
        scene_title = QLabel(f"{tr('Scene')} {scene_num}")
        scene_title.setStyleSheet("font-weight: bold; color: #212529; margin-bottom: 10px;")
        scene_layout.addWidget(scene_title)
        
        # 视频资源目录
        resource_layout = QHBoxLayout()
        resource_layout.addWidget(QLabel(tr("Resource folder:")))
        
        resource_edit = QLineEdit()
        resource_edit.setPlaceholderText(tr("Select video resource folder path"))
        resource_layout.addWidget(resource_edit, 1)
        
        resource_browse_btn = QPushButton(tr("Browse"))
        resource_browse_btn.clicked.connect(lambda: self.browse_scene_resource(resource_edit))
        resource_layout.addWidget(resource_browse_btn)
        
        scene_layout.addLayout(resource_layout)
        
        # 为资源编辑框添加自动保存
        resource_edit.textChanged.connect(self.save_config)
        
        # 存储组件引用
        self.scene_widgets.append({
            'frame': scene_frame,
            'title': scene_title,
            'resource_edit': resource_edit,
            'browse_btn': resource_browse_btn
        })
        
        self.scenes_layout.addWidget(scene_frame)
    
    def setup_connections(self):
        """设置信号连接"""
        # 完整音频复选框变化
        self.use_full_audio_cb.toggled.connect(self.on_full_audio_toggled)
        self.use_full_audio_cb.toggled.connect(self.save_config)
        self.full_audio_dir_edit.textChanged.connect(self.save_config)
        
        # 视频布局变化
        self.video_layout_combo.currentTextChanged.connect(self.update_video_size_options)
        self.video_layout_combo.currentTextChanged.connect(self.save_config)
        self.video_fps_combo.currentTextChanged.connect(self.save_config)
        self.min_segment_spin.valueChanged.connect(self.save_config)
        self.max_segment_spin.valueChanged.connect(self.save_config)
        
        
        # 固定字幕配置变化
        self.enable_fixed_subtitles_cb.toggled.connect(self.save_config)
        self.subtitle_file_edit.textChanged.connect(self.save_config)
        self.subtitle_font_combo.currentTextChanged.connect(self.save_config)
        self.subtitle_size_spin.valueChanged.connect(self.save_config)
        self.subtitle_line_spacing_spin.valueChanged.connect(self.save_config)
        
        # 输出配置变化
        self.output_dir_edit.textChanged.connect(self.save_config)
        self.videos_count_spin.valueChanged.connect(self.save_config)
    
    def load_config(self):
        """加载配置"""
        try:
            # 加载完整音频配置
            full_audio_config = config_manager.get_full_audio_config()
            self.use_full_audio_cb.setChecked(full_audio_config.get('use_full_audio', True))
            self.full_audio_dir_edit.setText(full_audio_config.get('full_audio_dir', ''))
            
            
            # 加载视频配置
            video_config = config_manager.get_video_config()
            layout = video_config.get('layout', 'portrait')
            layout_index = {'portrait': 0, 'landscape': 1, 'square': 2}.get(layout, 0)
            self.video_layout_combo.setCurrentIndex(layout_index)
            
            fps = video_config.get('fps', 25)
            fps_index = [20, 25, 30].index(fps) if fps in [20, 25, 30] else 1
            self.video_fps_combo.setCurrentIndex(fps_index)
            
            self.min_segment_spin.setValue(video_config.get('min_segment_length', 5))
            self.max_segment_spin.setValue(video_config.get('max_segment_length', 10))
            
            
            # 加载固定字幕配置
            fixed_subtitle_config = config_manager.get_fixed_subtitles_config()
            self.enable_fixed_subtitles_cb.setChecked(fixed_subtitle_config.get('enable', False))
            self.subtitle_file_edit.setText(fixed_subtitle_config.get('file_path', ''))
            
            # 加载字体和样式配置
            font = fixed_subtitle_config.get('font', 'Arial')
            if font in [self.subtitle_font_combo.itemText(i) for i in range(self.subtitle_font_combo.count())]:
                self.subtitle_font_combo.setCurrentText(font)
            
            self.subtitle_size_spin.setValue(fixed_subtitle_config.get('font_size', 48))
            self.subtitle_line_spacing_spin.setValue(fixed_subtitle_config.get('line_spacing', 40))
            
            # 设置颜色按钮
            color = fixed_subtitle_config.get('font_color', '#FFFFFF')
            self.subtitle_color_btn.setStyleSheet(f"background-color: {color}; border: 1px solid #ccc;")
            self.subtitle_color_btn.setText(color)
                
            # 加载输出配置
            output_config = config_manager.get_output_config()
            output_dir = output_config.get('dir', '')
            if not output_dir:
                # 设置默认输出目录
                output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../final"))
            self.output_dir_edit.setText(output_dir)
            self.videos_count_spin.setValue(output_config.get('videos_count', 1))
            
            # 加载场景配置
            scenes_config = config_manager.get_scenes_config()
            if scenes_config:
                # 清除现有场景
                for scene in self.scene_widgets:
                    scene['frame'].setParent(None)
                    scene['frame'].deleteLater()
                self.scene_widgets.clear()
                
                # 加载保存的场景
                for i, scene_data in enumerate(scenes_config):
                    self.add_scene_widget(i + 1)
                    if i < len(self.scene_widgets):
                        self.scene_widgets[i]['resource_edit'].setText(scene_data.get('resource_dir', ''))
            
            
            # 刷新统计信息
            self.refresh_statistics()
            
        except Exception as e:
            print(f"加载配置失败: {e}")
            # 如果加载失败，使用默认值
    
    def save_config(self):
        """保存配置"""
        try:
            # 保存完整音频配置
            config_manager.set_full_audio_config(
                self.use_full_audio_cb.isChecked(),
                self.full_audio_dir_edit.text()
            )
            
            
            # 保存视频配置
            layout_map = {0: 'portrait', 1: 'landscape', 2: 'square'}
            fps_list = [20, 25, 30]
            
            video_config = {
                'layout': layout_map.get(self.video_layout_combo.currentIndex(), 'portrait'),
                'fps': fps_list[self.video_fps_combo.currentIndex()],
                'size': self.video_size_combo.currentData() or self.video_size_combo.currentText(),
                'min_segment_length': self.min_segment_spin.value(),
                'max_segment_length': self.max_segment_spin.value()
            }
            config_manager.set_video_config(video_config)
            
            
            # 保存固定字幕配置
            fixed_subtitle_config = {
                'enable': self.enable_fixed_subtitles_cb.isChecked(),
                'file_path': self.subtitle_file_edit.text(),
                'font': self.subtitle_font_combo.currentText(),
                'font_size': self.subtitle_size_spin.value(),
                'font_color': self.subtitle_color_btn.text(),
                'line_spacing': self.subtitle_line_spacing_spin.value()
            }
            config_manager.set_fixed_subtitles_config(fixed_subtitle_config)
            
            # 保存输出配置
            output_config = {
                'dir': self.output_dir_edit.text(),
                'videos_count': self.videos_count_spin.value()
            }
            config_manager.set_output_config(output_config)
            
            # 保存场景配置
            scenes_config = []
            for scene in self.scene_widgets:
                scenes_config.append({
                    'resource_dir': scene['resource_edit'].text()
                })
            config_manager.set_scenes_config(scenes_config)
            
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    # 事件处理方法
    def browse_audio_directory(self):
        """浏览音频目录"""
        directory = QFileDialog.getExistingDirectory(
            self, tr("Select Audio Directory"), self.full_audio_dir_edit.text())
        if directory:
            self.full_audio_dir_edit.setText(directory)
    
    def browse_output_directory(self):
        """浏览输出目录"""
        directory = QFileDialog.getExistingDirectory(
            self, tr("Select Output Directory"), self.output_dir_edit.text())
        if directory:
            self.output_dir_edit.setText(directory)
    
    def browse_scene_resource(self, edit_widget):
        """浏览场景资源目录"""
        directory = QFileDialog.getExistingDirectory(
            self, tr("Select Scene Resource Directory"), edit_widget.text())
        if directory:
            edit_widget.setText(directory)
    
    def browse_subtitle_file(self):
        """浏览字幕文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, tr("Select Subtitle File"), 
            self.subtitle_file_edit.text(),
            "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.subtitle_file_edit.setText(file_path)
    
    def choose_subtitle_color(self):
        """选择字幕颜色"""
        from PyQt6.QtWidgets import QColorDialog
        from PyQt6.QtGui import QColor
        
        # 获取当前颜色
        current_color = self.subtitle_color_btn.text()
        try:
            color = QColor(current_color)
        except:
            color = QColor("#FFFFFF")
        
        # 打开颜色选择对话框
        new_color = QColorDialog.getColor(color, self, tr("Choose Subtitle Color"))
        if new_color.isValid():
            hex_color = new_color.name().upper()
            self.subtitle_color_btn.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #ccc;")
            self.subtitle_color_btn.setText(hex_color)
            self.save_config()
    
    def add_scene(self):
        """添加场景"""
        if len(self.scene_widgets) < 4:  # 最多4个场景
            scene_num = len(self.scene_widgets) + 1
            self.add_scene_widget(scene_num)
            self.save_config()  # 自动保存
        else:
            QMessageBox.warning(self, tr("Warning"), tr("Maximum number of scenes reached (4)"))
    
    def delete_scene(self):
        """删除场景"""
        if len(self.scene_widgets) > 1:  # 至少保留1个场景
            # 移除最后一个场景
            last_scene = self.scene_widgets.pop()
            last_scene['frame'].setParent(None)
            last_scene['frame'].deleteLater()
            self.save_config()  # 自动保存
        else:
            QMessageBox.warning(self, tr("Warning"), tr("At least one scene is required"))
    
    def on_full_audio_toggled(self, checked):
        """完整音频选项切换"""
        # 固定字幕不受完整音频模式影响，可以独立启用
        pass
    
    def update_video_size_options(self):
        """更新视频分辨率选项"""
        layout = self.video_layout_combo.currentText()
        self.video_size_combo.clear()
        
        if tr("Portrait") in layout:
            sizes = {"1080x1920": "1080p", "720x1280": "720p", "480x960": "480p", "360x720": "360p"}
        elif tr("Landscape") in layout:
            sizes = {"1920x1080": "1080p", "1280x720": "720p", "960x480": "480p", "720x360": "360p"}
        else:  # Square
            sizes = {"1080x1080": "1080p", "720x720": "720p", "480x480": "480p", "360x360": "360p"}
        
        for size, label in sizes.items():
            self.video_size_combo.addItem(label, size)
    
    def generate_video(self):
        """生成视频"""
        try:
            # 首先保存当前配置
            self.save_config()
            
            # 显示进度条和状态
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_text.setVisible(True)
            self.status_text.clear()
            self.result_label.setVisible(False)
            
            # 禁用生成按钮
            self.generate_btn.setEnabled(False)
            
            # 获取视频混剪服务
            from services.video_mix_service import get_video_mix_service
            
            video_service = get_video_mix_service()
            
            # 启动生成任务
            success = video_service.generate_video(
                progress_callback=self.on_progress_updated,
                status_callback=self.on_status_updated,
                error_callback=self.on_generation_error,
                completion_callback=self.on_generation_complete
            )
            
            if not success:
                self.on_generation_error("无法启动视频生成任务")
                
        except Exception as e:
            self.on_generation_error(f"生成视频时发生错误: {str(e)}")
    
    def on_progress_updated(self, progress):
        """进度更新处理"""
        self.progress_bar.setValue(progress)
    
    def on_status_updated(self, status):
        """状态更新处理"""
        self.status_text.append(status)
        # 自动滚动到底部
        self.status_text.verticalScrollBar().setValue(
            self.status_text.verticalScrollBar().maximum()
        )
    
    def on_generation_error(self, error_msg):
        """生成错误处理"""
        self.status_text.append(f"❌ 错误: {error_msg}")
        
        # 显示错误结果
        self.result_label.setText(f"❌ {error_msg}")
        self.result_label.setStyleSheet("color: #dc3545; font-weight: bold; margin: 10px 0px;")
        self.result_label.setVisible(True)
        
        # 恢复生成按钮
        self.generate_btn.setEnabled(True)
        
        # 延迟隐藏进度
        QTimer.singleShot(5000, self.hide_progress)
    
    def on_generation_complete(self, output_file=None):
        """生成完成处理"""
        self.progress_bar.setValue(100)
        
        if output_file:
            self.status_text.append(f"✅ 视频生成完成: {output_file}")
            # 显示成功结果
            self.result_label.setText(f"✅ 视频生成成功！\n文件保存到: {os.path.basename(output_file)}")
        else:
            self.status_text.append(tr("Video generation completed!"))
            self.result_label.setText(tr("✅ Video generated successfully! Check the output directory."))
        
        self.result_label.setStyleSheet("color: #28a745; font-weight: bold; margin: 10px 0px;")
        self.result_label.setVisible(True)
        
        # 恢复生成按钮
        self.generate_btn.setEnabled(True)
        
        # 刷新统计信息（因为可能使用了视频文件）
        self.refresh_statistics()
        
        # 隐藏进度条
        QTimer.singleShot(5000, self.hide_progress)
    
    def hide_progress(self):
        """隐藏进度显示"""
        self.progress_bar.setVisible(False)
        self.status_text.setVisible(False)
    
    def refresh_statistics(self):
        """刷新使用统计"""
        try:
            from tools.video_usage_tracker import get_video_usage_tracker
            
            tracker = get_video_usage_tracker()
            stats = tracker.get_usage_statistics()
            
            # 更新统计标签
            self.total_files_label.setText(str(stats['total_files']))
            self.available_files_label.setText(str(stats['available_files']))
            self.exceeded_files_label.setText(str(stats['exceeded_files']))
            
            # 更新警告信息
            self.usage_warning_label.setVisible(False)
            
            if stats['total_files'] > 0:
                if stats['available_files'] == 0:
                    self.usage_warning_label.setText(
                        "⚠️ " + tr("All video files have reached usage limit! Recommend resetting records or adding new video materials.")
                    )
                    self.usage_warning_label.setVisible(True)
                else:
                    available_ratio = stats['available_files'] / stats['total_files']
                    if available_ratio < 0.3:  # 30%阈值
                        self.usage_warning_label.setText(
                            f"⚠️ " + tr("Available video files are low ({:.1%}), consider resetting some usage records.").format(available_ratio)
                        )
                        self.usage_warning_label.setVisible(True)
            elif stats['total_files'] == 0:
                # 没有任何使用记录，不显示警告
                pass
                
        except Exception as e:
            print(f"刷新统计失败: {e}")
            self.total_files_label.setText("Error")
            self.available_files_label.setText("Error")
            self.exceeded_files_label.setText("Error")
    
    def reset_usage_records(self):
        """重置使用记录"""
        reply = QMessageBox.question(self, tr("Confirm"), 
                                   tr("Are you sure you want to reset all video usage records?"))
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from tools.video_usage_tracker import get_video_usage_tracker
                
                tracker = get_video_usage_tracker()
                tracker.reset_usage_records()
                
                QMessageBox.information(self, tr("Success"), tr("All video usage records have been reset!"))
                self.refresh_statistics()
                
            except Exception as e:
                print(f"重置记录失败: {e}")
                QMessageBox.warning(self, tr("Error"), tr("Failed to reset usage records: ") + str(e))
    
    def export_records(self):
        """导出记录"""
        from datetime import datetime
        
        default_filename = f"video_usage_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filename, _ = QFileDialog.getSaveFileName(
            self, tr("Export Usage Records"), 
            default_filename,
            "JSON Files (*.json)")
        if filename:
            try:
                import json
                from tools.video_usage_tracker import get_video_usage_tracker
                
                tracker = get_video_usage_tracker()
                export_data = tracker.export_records()
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, tr("Success"), tr("Records exported successfully!"))
                
            except Exception as e:
                print(f"导出记录失败: {e}")
                QMessageBox.warning(self, tr("Error"), tr("Failed to export records: ") + str(e))
    
    def apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            MixVideoPage {
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
                background-color: transparent;
            }
            
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                color: #212529;
                border: 2px solid #d0d0d0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: transparent;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: #f5f5f5;
                border-radius: 3px;
                color: #212529;
            }
            
            QLabel {
                color: #212529;
                background-color: transparent;
            }
            
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #357abd;
            }
            
            QPushButton:pressed {
                background-color: #2c5aa0;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            QLineEdit, QComboBox, QSpinBox {
                padding: 6px;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background-color: white;
                color: #212529;
            }
            
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #4a90e2;
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
            
            QComboBox::drop-down {
                border: none;
                background-color: transparent;
            }
            
            QComboBox::down-arrow {
                image: none;
                border: 1px solid #666;
                width: 8px;
                height: 8px;
            }
            
            QCheckBox {
                color: #212529;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #d0d0d0;
                border-radius: 2px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4a90e2;
                border-color: #4a90e2;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #d0d0d0;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                margin: 2px 0;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            
            QSlider::handle:horizontal:hover {
                background: #4a90e2;
            }
            
            QProgressBar {
                border: 2px solid #d0d0d0;
                border-radius: 5px;
                text-align: center;
                background-color: white;
                color: #212529;
            }
            
            QProgressBar::chunk {
                background-color: #4a90e2;
                border-radius: 3px;
            }
            
            QTextEdit {
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                background-color: white;
                color: #212529;
                padding: 6px;
            }
            
            QFrame {
                color: #212529;
                background-color: transparent;
            }
        """)