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
            "product_name": "Donbukll wrapping mask",
            "brand_name": "Donbukll",
            "phrases": [
                {"main": "Donbukll", "sub": "wrapping mask"},
                {"main": "Premium", "sub": "skincare solution"}
            ],
            "styles": {
                "main_title": {
                    "font_file": "fonts/PingFang.ttc",
                    "font_size": 46,
                    "font_color": "white",
                    "font_style": "italic"
                },
                "sub_title": {
                    "font_file": "fonts/Songti.ttc", 
                    "font_size": 32,
                    "font_color": "black"
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
            
            # 内容类型设置
            if 'fancy_text_content_type' in st.session_state:
                content_type = st.session_state.get('fancy_text_content_type', 'mixed')
                display_rules = self.config.setdefault('display_rules', {})
                
                if content_type == 'phrases':
                    display_rules['phrase_weight'] = 100
                    display_rules['advantage_weight'] = 0
                elif content_type == 'advantages':
                    display_rules['phrase_weight'] = 0
                    display_rules['advantage_weight'] = 100
                else:  # mixed
                    display_rules['phrase_weight'] = 70
                    display_rules['advantage_weight'] = 30
            
            # 位置设置
            if 'fancy_text_random_position' in st.session_state:
                display_rules = self.config.setdefault('display_rules', {})
                display_rules['random_position'] = st.session_state.get('fancy_text_random_position', True)
            
            # 颜色设置
            styles = self.config.setdefault('styles', {})
            
            # 主标题样式
            main_style = styles.setdefault('main_title', {})
            if 'fancy_text_main_color' in st.session_state:
                main_style['font_color'] = st.session_state.get('fancy_text_main_color', 'white')
            
            if 'fancy_text_shadow' in st.session_state:
                shadow_config = main_style.setdefault('shadow', {})
                shadow_config['enable'] = st.session_state.get('fancy_text_shadow', True)
            
            # 副标题样式
            sub_style = styles.setdefault('sub_title', {})
            if 'fancy_text_sub_color' in st.session_state:
                sub_style['font_color'] = st.session_state.get('fancy_text_sub_color', 'black')
            
            if 'fancy_text_bg_color' in st.session_state:
                background_config = sub_style.setdefault('background', {})
                background_config['enable'] = True
                background_config['color'] = st.session_state.get('fancy_text_bg_color', 'orange')
            
            # 动画设置
            if 'fancy_text_animation' in st.session_state:
                animation_enabled = st.session_state.get('fancy_text_animation', True)
                if not animation_enabled:
                    # 禁用动画效果
                    main_style.setdefault('animation', {})['type'] = 'none'
                    sub_style.setdefault('animation', {})['type'] = 'none'
                    self.config['fade_duration'] = 0
            
            print(f"UI配置合并完成，频率: {self.config.get('frequency')}秒，时长: {self.config.get('duration')}秒")
            
        except Exception as e:
            print(f"合并UI配置时发生错误: {e}")
    
    def is_enabled(self) -> bool:
        """检查花式文本功能是否启用"""
        return self.config.get('enable', False) and st.session_state.get('enable_fancy_text', False)
    
    def should_show_text(self, current_time: float, video_duration: float) -> bool:
        """判断在当前时间点是否应该显示文本"""
        if not self.is_enabled():
            return False
        
        frequency = self.config.get('frequency', 30)
        duration = self.config.get('duration', 4)
        
        # 计算显示时间点
        show_intervals = []
        current_interval = frequency
        while current_interval + duration < video_duration:
            show_intervals.append((current_interval, current_interval + duration))
            current_interval += frequency
        
        # 检查当前时间是否在任何显示区间内
        for start_time, end_time in show_intervals:
            if start_time <= current_time <= end_time:
                return True
        
        return False
    
    def get_text_content(self) -> Tuple[str, str]:
        """获取要显示的文本内容（主标题，副标题）"""
        display_rules = self.config.get('display_rules', {})
        phrase_weight = display_rules.get('phrase_weight', 70)
        advantage_weight = display_rules.get('advantage_weight', 30)
        
        # 根据权重随机选择显示内容类型
        if random.randint(1, 100) <= phrase_weight:
            # 显示短语组合
            phrases = self.config.get('phrases', [])
            if phrases:
                selected_phrase = random.choice(phrases)
                return selected_phrase.get('main', ''), selected_phrase.get('sub', '')
        else:
            # 显示产品优势
            advantages = self.config.get('advantages', [])
            if advantages:
                selected_advantage = random.choice(advantages)
                if len(selected_advantage) >= 2:
                    # 随机组合优势文本
                    main_text = selected_advantage[0]
                    sub_text = ' '.join(selected_advantage[1:2])
                    return main_text, sub_text
        
        # 默认返回品牌名称
        brand_name = self.config.get('brand_name', 'Donbukll')
        product_name = self.config.get('product_name', 'wrapping mask')
        return brand_name, product_name
    
    def get_text_position(self, video_width: int, video_height: int, text_type: str) -> Tuple[str, str]:
        """获取文本位置（返回x, y坐标字符串）"""
        styles = self.config.get('styles', {})
        style_config = styles.get(text_type, {})
        position_config = style_config.get('position', {})
        
        # 获取显示规则配置
        display_rules = self.config.get('display_rules', {})
        use_random_position = display_rules.get('random_position', True)
        
        if use_random_position:
            # 使用随机位置预设
            position_presets = self.config.get('position_presets', {})
            position_weights = display_rules.get('position_weights', {})
            
            if position_presets and position_weights:
                # 根据权重选择位置
                positions = list(position_weights.keys())
                weights = list(position_weights.values())
                selected_position = random.choices(positions, weights=weights)[0]
                preset = position_presets.get(selected_position, {})
                
                if text_type == 'main_title':
                    y_pos = preset.get('main_y', 120)
                    x_pos = preset.get('main_x', '(w-text_w)/2')
                else:
                    y_pos = preset.get('sub_y', 180)
                    x_pos = preset.get('sub_x', '(w-text_w)/2')
                
                return self._process_position_value(x_pos, video_width, video_height, True), \
                       self._process_position_value(y_pos, video_width, video_height, False)
        
        # 使用样式配置中的固定位置
        x_pos = position_config.get('x', 'center')
        y_pos = position_config.get('y', 120 if text_type == 'main_title' else 180)
        
        return self._process_position_value(x_pos, video_width, video_height, True), \
               self._process_position_value(y_pos, video_width, video_height, False)
    
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
    
    def generate_drawtext_filter(self, main_text: str, sub_text: str, 
                               video_width: int, video_height: int,
                               start_time: float, duration: float) -> str:
        """生成FFmpeg的drawtext滤镜字符串"""
        if not main_text and not sub_text:
            return ""
        
        styles = self.config.get('styles', {})
        filters = []
        
        # 调整字体大小适配不同分辨率
        resolution_key = f"{video_width}x{video_height}"
        font_scaling = self.config.get('compatibility', {}).get('font_scaling', {})
        scale_config = font_scaling.get(resolution_key, {})
        
        # 生成主标题滤镜
        if main_text:
            main_style = styles.get('main_title', {})
            main_filter = self._generate_single_text_filter(
                main_text, main_style, video_width, video_height,
                start_time, duration, 'main_title', scale_config
            )
            if main_filter:
                filters.append(main_filter)
        
        # 生成副标题滤镜
        if sub_text:
            sub_style = styles.get('sub_title', {})
            # 副标题可能有延迟显示
            animation_config = sub_style.get('animation', {})
            delay = animation_config.get('delay', 0)
            sub_start_time = start_time + delay
            sub_duration = duration - delay
            
            if sub_duration > 0:
                sub_filter = self._generate_single_text_filter(
                    sub_text, sub_style, video_width, video_height,
                    sub_start_time, sub_duration, 'sub_title', scale_config
                )
                if sub_filter:
                    filters.append(sub_filter)
        
        return ','.join(filters) if filters else ""
    
    def _generate_single_text_filter(self, text: str, style_config: Dict, 
                                   video_width: int, video_height: int,
                                   start_time: float, duration: float,
                                   text_type: str, scale_config: Dict) -> str:
        """生成单个文本的drawtext滤镜"""
        # 基础配置
        font_file = style_config.get('font_file', 'fonts/PingFang.ttc')
        font_path = self.get_font_path(font_file)
        
        # 字体大小（支持分辨率缩放）
        if text_type == 'main_title':
            font_size = scale_config.get('main_size', style_config.get('font_size', 46))
        else:
            font_size = scale_config.get('sub_size', style_config.get('font_size', 32))
        
        font_color = style_config.get('font_color', 'white')
        
        # 获取位置
        x_pos, y_pos = self.get_text_position(video_width, video_height, text_type)
        
        # 构建基础drawtext参数
        drawtext_params = [
            f"fontfile={font_path}",
            f"text='{text}'",
            f"fontsize={font_size}",
            f"fontcolor={font_color}",
            f"x={x_pos}",
            f"y={y_pos}"
        ]
        
        # 添加时间控制
        fade_duration = self.config.get('fade_duration', 0.5)
        end_time = start_time + duration
        
        # 淡入淡出效果
        alpha_expression = f"if(lt(t,{start_time}),0,if(lt(t,{start_time + fade_duration}),(t-{start_time})/{fade_duration},if(lt(t,{end_time - fade_duration}),1,if(lt(t,{end_time}),({end_time}-t)/{fade_duration},0))))"
        drawtext_params.append(f"alpha='{alpha_expression}'")
        
        # 阴影效果
        shadow_config = style_config.get('shadow', {})
        if shadow_config.get('enable', False):
            shadow_color = shadow_config.get('color', 'black')
            shadow_x = shadow_config.get('offset_x', 2)
            shadow_y = shadow_config.get('offset_y', 2)
            drawtext_params.extend([
                f"shadowcolor={shadow_color}",
                f"shadowx={shadow_x}",
                f"shadowy={shadow_y}"
            ])
        
        # 描边效果
        outline_config = style_config.get('outline', {})
        if outline_config.get('enable', False):
            outline_color = outline_config.get('color', 'black')
            outline_width = outline_config.get('width', 1)
            drawtext_params.extend([
                f"bordercolor={outline_color}",
                f"borderw={outline_width}"
            ])
        
        # 背景框效果
        background_config = style_config.get('background', {})
        if background_config.get('enable', False):
            bg_color = background_config.get('color', 'orange')
            bg_padding = background_config.get('padding', 10)
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
        
        intervals = []
        current_time = frequency
        
        while current_time + duration <= video_duration:
            intervals.append((current_time, current_time + duration))
            current_time += frequency
        
        return intervals
    
    def generate_complete_filter_complex(self, video_duration: float, 
                                       video_width: int, video_height: int) -> str:
        """生成完整的filter_complex字符串，包含所有时间区间的文本"""
        if not self.is_enabled():
            return ""
        
        intervals = self.get_display_intervals(video_duration)
        if not intervals:
            return ""
        
        all_filters = []
        
        for start_time, end_time in intervals:
            duration = end_time - start_time
            main_text, sub_text = self.get_text_content()
            
            filter_text = self.generate_drawtext_filter(
                main_text, sub_text, video_width, video_height,
                start_time, duration
            )
            
            if filter_text:
                all_filters.append(filter_text)
        
        return ','.join(all_filters) if all_filters else ""
    
    def preview_text_style(self, text_type: str = 'main_title') -> Dict:
        """获取文本样式预览信息"""
        styles = self.config.get('styles', {})
        style_config = styles.get(text_type, {})
        
        return {
            'font_size': style_config.get('font_size', 46),
            'font_color': style_config.get('font_color', 'white'),
            'background_enabled': style_config.get('background', {}).get('enable', False),
            'background_color': style_config.get('background', {}).get('color', 'orange'),
            'shadow_enabled': style_config.get('shadow', {}).get('enable', False),
            'sample_text': self.get_text_content()
        }