#  Copyright © [2024] 程序那些事
#
#  All rights reserved. This software and associated documentation files (the "Software") are provided for personal and educational use only. Commercial use of the Software is strictly prohibited unless explicit permission is obtained from the author.
#
#  Permission is hereby granted to any person to use, copy, and modify the Software for non-commercial purposes, provided that the following conditions are met:
#
#  1. The original copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
#  2. Modifications, if any, must retain the original copyright information and must not imply that the modified version is an official version of the Software.
#  3. Any distribution of the Software or its modifications must retain the original copyright notice and include this permission notice.
#
#  For commercial use, including but not limited to selling, distributing, or using the Software as part of any commercial product or service, you must obtain explicit authorization from the author.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Author: 程序那些事
#  email: flydean@163.com
#  Website: [www.flydean.com](http://www.flydean.com)
#  GitHub: [https://github.com/ddean2009/MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus)
#
#  All rights reserved.
#

import os
import platform
import random
import yaml
from typing import Dict, List, Tuple, Optional
import streamlit as st

from tools.file_utils import read_yaml

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# 配置文件路径
fancy_text_config_file = os.path.join(script_dir, "../../config/fancy_text_overlays.yml")
fancy_text_config_file = os.path.abspath(fancy_text_config_file)

# 字体目录
font_dir = os.path.join(script_dir, "../../fonts")
font_dir = os.path.abspath(font_dir)

class FancyTextService:
    def __init__(self):
        """初始化花式文本服务"""
        self.config = self._load_config()
        self.font_dir = font_dir
        self._prepare_font_paths()
        # 合并UI配置
        self._merge_ui_config()
    
    def _load_config(self) -> Dict:
        """加载花式文本配置"""
        try:
            if os.path.exists(fancy_text_config_file):
                config = read_yaml(fancy_text_config_file)
                return config.get('fancy_text', {})
            else:
                print(f"警告：花式文本配置文件不存在: {fancy_text_config_file}")
                return self._get_default_config()
        except Exception as e:
            print(f"加载花式文本配置失败: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "enable": True,
            "frequency": 30,
            "duration": 4,
            "display_count": 1,
            "default_phrases": [
                "Deep Moisturizing Care",
                "Natural Organic Formula", 
                "24 Hour Lasting Effect",
                "Anti-Aging Collagen Boost",
                "Professional Skincare Solution"
            ],
            "phrase_style": {
                "font_file": "fonts/PingFang.ttc",
                "font_size": 70,
                "font_color": "white",
                "font_style": "bold",
                "line_spacing": 50,
                "shadow": {
                    "enable": True,
                    "color": "black",
                    "offset_x": 3,
                    "offset_y": 3
                },
                "background": {
                    "enable": True,
                    "color": "orange",
                    "padding": 15
                }
            }
        }
    
    def _prepare_font_paths(self):
        """处理字体路径（Windows兼容性）"""
        if platform.system() == "Windows":
            # Windows路径需要特殊处理，用于FFmpeg
            self.font_dir_escaped = self.font_dir.replace("\\", "\\\\\\\\")
            self.font_dir_escaped = self.font_dir_escaped.replace(":", "\\\\:")
        else:
            self.font_dir_escaped = self.font_dir
    
    def _merge_ui_config(self):
        """合并UI配置到主配置中"""
        try:
            # 从session_state获取UI配置值并覆盖默认配置
            
            # 基础显示设置
            if 'fancy_text_frequency' in st.session_state:
                self.config['frequency'] = st.session_state.get('fancy_text_frequency', 25)
            
            if 'fancy_text_duration' in st.session_state:
                self.config['duration'] = st.session_state.get('fancy_text_duration', 4)
            
            if 'fancy_text_display_count' in st.session_state:
                self.config['display_count'] = st.session_state.get('fancy_text_display_count', 1)
            
            # 位置设置
            if 'fancy_text_random_position' in st.session_state:
                display_rules = self.config.setdefault('display_rules', {})
                display_rules['random_position'] = st.session_state.get('fancy_text_random_position', True)
            
            # 短语样式设置
            phrase_style = self.config.setdefault('phrase_style', {})
            
            if 'fancy_text_font_color' in st.session_state:
                phrase_style['font_color'] = st.session_state.get('fancy_text_font_color', 'white')
            
            if 'fancy_text_font_size' in st.session_state:
                phrase_style['font_size'] = st.session_state.get('fancy_text_font_size', 70)
            
            if 'fancy_text_line_spacing' in st.session_state:
                phrase_style['line_spacing'] = st.session_state.get('fancy_text_line_spacing', 50)
            
            if 'fancy_text_shadow' in st.session_state:
                shadow_config = phrase_style.setdefault('shadow', {})
                shadow_config['enable'] = st.session_state.get('fancy_text_shadow', True)
            
            if 'fancy_text_bg_color' in st.session_state:
                background_config = phrase_style.setdefault('background', {})
                background_config['enable'] = True
                background_config['color'] = st.session_state.get('fancy_text_bg_color', 'orange')
            
            # 开头字幕设置
            if 'fancy_text_show_at_start' in st.session_state:
                self.config['show_at_start'] = st.session_state.get('fancy_text_show_at_start', True)
            
            # 动画设置
            if 'fancy_text_animation' in st.session_state:
                animation_enabled = st.session_state.get('fancy_text_animation', True)
                if not animation_enabled:
                    self.config['fade_duration'] = 0
            
            print(f"UI配置合并完成，频率: {self.config.get('frequency')}秒，时长: {self.config.get('duration')}秒，显示条数: {self.config.get('display_count')}")
            
        except Exception as e:
            print(f"合并UI配置时发生错误: {e}")
    
    def is_enabled(self) -> bool:
        """检查花式文本功能是否启用"""
        return self.config.get('enable', False) and st.session_state.get('enable_fancy_text', False)
    
    def should_show_text(self, current_time: float, video_duration: float) -> bool:
        """判断在当前时间点是否应该显示文本"""
        if not self.is_enabled():
            return False
        
        show_intervals = self.get_display_intervals(video_duration)
        
        # 检查当前时间是否在任何显示区间内
        for start_time, end_time in show_intervals:
            if start_time <= current_time <= end_time:
                return True
        
        return False
    
    def get_phrases_from_file(self) -> List[str]:
        """从选择的txt文件中读取短语列表"""
        file_path = st.session_state.get('fancy_text_phrases_file', '')
        
        if not file_path or not os.path.exists(file_path):
            return self.config.get('default_phrases', [
                "Deep Moisturizing Care",
                "Natural Organic Formula", 
                "24 Hour Lasting Effect",
                "Anti-Aging Collagen Boost",
                "Professional Skincare Solution"
            ])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                phrases = [line.strip() for line in f if line.strip()]
            return phrases if phrases else self.config.get('default_phrases', [])
        except Exception as e:
            print(f"读取短语文件失败: {e}")
            return self.config.get('default_phrases', [])

    def get_phrases_list(self) -> List[str]:
        """获取当前可用的短语列表（优先从文件读取）"""
        return self.get_phrases_from_file()
    
    def get_display_phrases(self) -> List[str]:
        """获取本次要显示的短语列表"""
        all_phrases = self.get_phrases_list()
        if not all_phrases:
            return ["No phrases available"]
        
        display_count = self.config.get('display_count', 1)
        display_count = min(display_count, len(all_phrases), 5)  # 最多5条
        
        # 随机选择短语
        return random.sample(all_phrases, display_count)
    
    
    def get_phrases_position(self, video_width: int, video_height: int, phrase_count: int, selected_position_preset: str = None) -> Tuple[str, str]:
        """获取短语显示位置（返回起始x, y坐标字符串）"""
        phrase_style = self.config.get('phrase_style', {})
        position_config = phrase_style.get('position', {})
        
        # 获取显示规则配置
        display_rules = self.config.get('display_rules', {})
        use_random_position = display_rules.get('random_position', True)
        
        if use_random_position and selected_position_preset:
            # 使用位置预设
            position_presets = self.config.get('position_presets', {})
            preset = position_presets.get(selected_position_preset, {})
            x_pos = preset.get('x', 'center')
            y_pos = preset.get('y', 'center')
        else:
            # 使用样式配置中的固定位置
            x_pos = position_config.get('x', 'center')
            y_pos = position_config.get('y', 'center')
        
        # 如果是多行显示，调整起始Y位置以确保居中
        if phrase_count > 1:
            line_spacing = phrase_style.get('line_spacing', 50)
            font_size = phrase_style.get('font_size', 70)
            
            # 计算总高度
            total_height = phrase_count * font_size + (phrase_count - 1) * line_spacing
            
            # 调整Y位置以居中显示
            if y_pos == 'center':
                y_pos = f'(h-{total_height})/2'
            elif isinstance(y_pos, str) and 'center' in y_pos:
                # 处理 "center-60" 这样的格式
                offset = 0
                if '+' in y_pos:
                    offset = int(y_pos.split('+')[1])
                elif '-' in y_pos:
                    offset = -int(y_pos.split('-')[1])
                y_pos = f'(h-{total_height})/2{offset:+d}'
        
        return self._process_position_value(x_pos, video_width, video_height, True), \
               self._process_position_value(y_pos, video_width, video_height, False)
    
    def select_random_position_preset(self) -> str:
        """选择随机位置预设"""
        display_rules = self.config.get('display_rules', {})
        position_weights = display_rules.get('position_weights', {})
        
        if position_weights:
            positions = list(position_weights.keys())
            weights = list(position_weights.values())
            return random.choices(positions, weights=weights)[0]
        
        return 'top_center'  # 默认位置
    
    def _process_position_value(self, pos_value, video_width: int, video_height: int, is_x: bool) -> str:
        """处理位置数值，转换为FFmpeg可用的表达式"""
        if isinstance(pos_value, str):
            if pos_value == 'center':
                return '(w-text_w)/2' if is_x else '(h-text_h)/2'
            elif pos_value == 'left':
                return '50' if is_x else str(pos_value)
            elif pos_value == 'right':
                return 'w-text_w-50' if is_x else str(pos_value)
            elif 'center' in pos_value:
                # 处理 "center+30" 或 "center-30" 格式
                if '+' in pos_value:
                    offset = int(pos_value.split('+')[1])
                    base = '(w-text_w)/2' if is_x else '(h-text_h)/2'
                    return f'{base}+{offset}'
                elif '-' in pos_value:
                    offset = int(pos_value.split('-')[1])
                    base = '(w-text_w)/2' if is_x else '(h-text_h)/2'
                    return f'{base}-{offset}'
            elif 'width' in pos_value:
                # 处理 "width-200" 格式
                offset = int(pos_value.split('-')[1])
                return f'w-{offset}'
            elif 'height' in pos_value:
                # 处理 "height-200" 格式
                offset = int(pos_value.split('-')[1])
                return f'h-{offset}'
        
        return str(pos_value)
    
    def get_font_path(self, font_file: str) -> str:
        """获取字体文件的完整路径"""
        if os.path.isabs(font_file):
            font_path = font_file
        else:
            font_path = os.path.join(self.font_dir, os.path.basename(font_file))
        
        # Windows路径处理
        if platform.system() == "Windows":
            font_path = font_path.replace("\\", "\\\\\\\\")
            font_path = font_path.replace(":", "\\\\:")
        
        return font_path
    
    def generate_drawtext_filter(self, phrases: List[str], 
                               video_width: int, video_height: int,
                               start_time: float, duration: float) -> str:
        """生成FFmpeg的drawtext滤镜字符串（支持多行短语）"""
        if not phrases:
            return ""
        
        # 为这组短语选择统一的位置预设
        self._current_position_preset = self.select_random_position_preset()
        
        # 调整字体大小适配不同分辨率
        resolution_key = f"{video_width}x{video_height}"
        font_scaling = self.config.get('compatibility', {}).get('font_scaling', {})
        scale_config = font_scaling.get(resolution_key, {})
        
        phrase_style = self.config.get('phrase_style', {})
        filters = []
        
        # 获取起始位置
        start_x, start_y = self.get_phrases_position(video_width, video_height, len(phrases), self._current_position_preset)
        
        # 为每个短语生成滤镜
        for i, phrase in enumerate(phrases):
            phrase_filter = self._generate_phrase_filter(
                phrase, phrase_style, video_width, video_height,
                start_time, duration, scale_config, start_x, start_y, i
            )
            if phrase_filter:
                filters.append(phrase_filter)
        
        # 清理临时变量
        if hasattr(self, '_current_position_preset'):
            delattr(self, '_current_position_preset')
        
        return ','.join(filters) if filters else ""
    
    def _generate_phrase_filter(self, phrase: str, phrase_style: Dict, 
                              video_width: int, video_height: int,
                              start_time: float, duration: float,
                              scale_config: Dict, start_x: str, start_y: str, line_index: int) -> str:
        """生成单个短语的drawtext滤镜"""
        # 基础配置
        font_file = phrase_style.get('font_file', 'fonts/PingFang.ttc')
        font_path = self.get_font_path(font_file)
        
        # 字体大小（优先使用分辨率适配的大小）
        font_size = scale_config.get('font_size', phrase_style.get('font_size', 70))
        font_color = phrase_style.get('font_color', 'white')
        
        # 计算当前行的Y位置
        line_spacing = scale_config.get('line_spacing', phrase_style.get('line_spacing', 50))
        current_y = start_y
        if line_index > 0:
            # 如果start_y是表达式，需要特殊处理
            if '(' in start_y:
                current_y = f"{start_y}+{line_index * (font_size + line_spacing)}"
            else:
                current_y = f"{start_y}+{line_index * (font_size + line_spacing)}"
        
        # 构建基础drawtext参数
        drawtext_params = [
            f"fontfile={font_path}",
            f"text='{phrase}'",
            f"fontsize={font_size}",
            f"fontcolor={font_color}",
            f"x={start_x}",
            f"y={current_y}"
        ]
        
        # 添加时间控制
        fade_duration = self.config.get('fade_duration', 0.5)
        end_time = start_time + duration
        
        # 淡入淡出效果
        if fade_duration > 0:
            alpha_expression = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + fade_duration}),(t-{start_time})/{fade_duration},if(lt(t,{end_time - fade_duration}),1,if(lt(t,{end_time}),({end_time}-t)/{fade_duration},0))))"
            drawtext_params.append(f"alpha='{alpha_expression}'")
        else:
            # 无动画效果，直接显示
            drawtext_params.append(f"enable='between(t,{start_time},{end_time})'")
        
        # 阴影效果
        shadow_config = phrase_style.get('shadow', {})
        if shadow_config.get('enable', False):
            shadow_color = shadow_config.get('color', 'black')
            shadow_x = shadow_config.get('offset_x', 3)
            shadow_y = shadow_config.get('offset_y', 3)
            drawtext_params.extend([
                f"shadowcolor={shadow_color}",
                f"shadowx={shadow_x}",
                f"shadowy={shadow_y}"
            ])
        
        # 描边效果
        outline_config = phrase_style.get('outline', {})
        if outline_config.get('enable', False):
            outline_color = outline_config.get('color', 'gray')
            outline_width = outline_config.get('width', 1)
            drawtext_params.extend([
                f"bordercolor={outline_color}",
                f"borderw={outline_width}"
            ])
        
        # 背景框效果
        background_config = phrase_style.get('background', {})
        if background_config.get('enable', False):
            bg_color = background_config.get('color', 'orange')
            bg_padding = background_config.get('padding', 15)
            drawtext_params.extend([
                "box=1",
                f"boxcolor={bg_color}",
                f"boxborderw={bg_padding}"
            ])
        
        return "drawtext=" + ":".join(drawtext_params)
    
    def get_display_intervals(self, video_duration: float) -> List[Tuple[float, float]]:
        """获取所有文本显示的时间区间"""
        if not self.is_enabled():
            return []
        
        frequency = self.config.get('frequency', 30)
        duration = self.config.get('duration', 4)
        show_at_start = self.config.get('show_at_start', True)
        
        intervals = []
        
        # 如果启用开头字幕，在开始时显示
        if show_at_start and video_duration >= duration:
            intervals.append((0, duration))
        
        # 按频率添加后续显示区间
        current_time = frequency
        while current_time + duration <= video_duration:
            intervals.append((current_time, current_time + duration))
            current_time += frequency
        
        return intervals
    
    def generate_complete_filter_complex(self, video_duration: float, 
                                       video_width: int, video_height: int) -> str:
        """生成完整的filter_complex字符串，包含所有时间区间的短语"""
        if not self.is_enabled():
            return ""
        
        intervals = self.get_display_intervals(video_duration)
        if not intervals:
            return ""
        
        all_filters = []
        
        for start_time, end_time in intervals:
            duration = end_time - start_time
            phrases = self.get_display_phrases()
            
            filter_text = self.generate_drawtext_filter(
                phrases, video_width, video_height,
                start_time, duration
            )
            
            if filter_text:
                all_filters.append(filter_text)
        
        return ','.join(all_filters) if all_filters else ""
    
    def preview_phrase_style(self) -> Dict:
        """获取短语样式预览信息"""
        phrase_style = self.config.get('phrase_style', {})
        
        return {
            'font_size': phrase_style.get('font_size', 70),
            'font_color': phrase_style.get('font_color', 'white'),
            'background_enabled': phrase_style.get('background', {}).get('enable', False),
            'background_color': phrase_style.get('background', {}).get('color', 'orange'),
            'shadow_enabled': phrase_style.get('shadow', {}).get('enable', False),
            'sample_phrases': self.get_phrases_list()[:3] if self.get_phrases_list() else ["Sample Phrase"]
        }