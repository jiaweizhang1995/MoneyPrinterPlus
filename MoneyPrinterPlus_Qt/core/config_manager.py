"""
配置管理器 - 适配自原项目的 config.py
"""
import os
import shutil
import yaml
from typing import Dict, Any

# 支持的语言
LANGUAGES = {'zh-CN': "简体中文", 'en': "english", 'zh-TW': "繁體中文"}

# 音频提供商
AUDIO_PROVIDERS = ['Ali']

# LLM提供商  
LLM_PROVIDERS = ['Tongyi']

# 应用标题
APP_TITLE = "DONBUKLL批量视频生成 - PyQt6版本"

class ConfigManager:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_dir = os.path.join(self.script_dir, "config")
        
        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        self.config_example_file = os.path.join(self.config_dir, "config.example.yml")
        self.config_file = os.path.join(self.config_dir, "config.yml")
        
        # 保存状态标志，避免递归保存
        self._saving = False
        
        self._create_default_config_example()
        self.config = self._load_config()
    
    def _create_default_config_example(self):
        """创建默认配置示例文件"""
        if not os.path.exists(self.config_example_file):
            default_config = {
                'audio': {
                    'provider': 'Ali',
                    'Ali': {
                        'access_key_id': 'YOUR_ACCESS_KEY_ID',
                        'access_key_secret': 'YOUR_ACCESS_KEY_SECRET',
                        'app_key': 'YOUR_APP_KEY'
                    }
                },
                'llm': {
                    'provider': 'Tongyi',
                    'Tongyi': {
                        'api_key': 'YOUR_API_KEY',
                        'model_name': 'qwen-turbo'
                    }
                },
                'ui': {
                    'language': 'zh-CN'
                },
                'video_mix': {
                    'use_full_audio': True,
                    'full_audio_dir': '',
                    'scenes': [],
                    'video_config': {
                        'layout': 'portrait',  # portrait, landscape, square
                        'fps': 25,
                        'size': '1080x1920',
                        'min_segment_length': 5,
                        'max_segment_length': 10
                    },
                    'subtitles': {
                        'enable': False,
                        'font': 'Songti SC Bold',
                        'size': 8,
                        'lines': 2,
                        'position': 'bottom_center',
                        'color': '#FFFFFF',
                        'border_color': '#000000',
                        'border_width': 0
                    },
                    'output': {
                        'dir': '',
                        'videos_count': 1
                    }
                }
            }
            self._save_yaml(self.config_example_file, default_config)
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            shutil.copy(self.config_example_file, self.config_file)
        
        if os.path.exists(self.config_file):
            return self._read_yaml(self.config_file)
        return {}
    
    def save_config(self):
        """保存配置到文件"""
        if self._saving:
            return  # 避免递归保存
        
        self._saving = True
        try:
            # 创建配置的深拷贝，避免保存时的循环引用
            import copy
            config_copy = copy.deepcopy(self.config)
            self._save_yaml(self.config_file, config_copy)
        finally:
            self._saving = False
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.config
    
    def update_config(self, section: str, key: str, value: Any, auto_save: bool = True):
        """更新配置项"""
        if section not in self.config:
            self.config[section] = {}
        
        # 检查值是否真的改变了
        if self.config[section].get(key) == value:
            return  # 值没有改变，不需要保存
        
        self.config[section][key] = value
        if auto_save:
            self.save_config()
    
    def update_nested_config(self, section: str, subsection: str, key: str, value: Any, auto_save: bool = True):
        """更新嵌套配置项"""
        if section not in self.config:
            self.config[section] = {}
        if subsection not in self.config[section]:
            self.config[section][subsection] = {}
        
        # 检查值是否真的改变了
        if self.config[section][subsection].get(key) == value:
            return  # 值没有改变，不需要保存
        
        self.config[section][subsection][key] = value
        if auto_save:
            self.save_config()
    
    def get_audio_provider(self) -> str:
        """获取当前音频提供商"""
        return self.config.get('audio', {}).get('provider', 'Ali')
    
    def set_audio_provider(self, provider: str):
        """设置音频提供商"""
        self.update_config('audio', 'provider', provider)
    
    def get_llm_provider(self) -> str:
        """获取当前LLM提供商"""
        return self.config.get('llm', {}).get('provider', 'Tongyi')
    
    def set_llm_provider(self, provider: str):
        """设置LLM提供商"""
        self.update_config('llm', 'provider', provider)
    
    def get_ui_language(self) -> str:
        """获取UI语言"""
        return self.config.get('ui', {}).get('language', 'zh-CN')
    
    def set_ui_language(self, language: str):
        """设置UI语言"""
        self.update_config('ui', 'language', language)
    
    def get_audio_config(self, provider: str) -> Dict[str, Any]:
        """获取音频服务配置"""
        return self.config.get('audio', {}).get(provider, {})
    
    def get_llm_config(self, provider: str) -> Dict[str, Any]:
        """获取LLM服务配置"""
        return self.config.get('llm', {}).get(provider, {})
    
    # 视频混剪相关配置方法
    def get_video_mix_config(self) -> Dict[str, Any]:
        """获取视频混剪配置"""
        return self.config.get('video_mix', {})
    
    def get_full_audio_config(self) -> Dict[str, Any]:
        """获取完整音频配置"""
        video_mix = self.get_video_mix_config()
        return {
            'use_full_audio': video_mix.get('use_full_audio', True),
            'full_audio_dir': video_mix.get('full_audio_dir', '')
        }
    
    def set_full_audio_config(self, use_full_audio: bool, full_audio_dir: str = None):
        """设置完整音频配置"""
        self.update_config('video_mix', 'use_full_audio', use_full_audio)
        if full_audio_dir is not None:
            self.update_config('video_mix', 'full_audio_dir', full_audio_dir)
    
    def get_video_config(self) -> Dict[str, Any]:
        """获取视频配置"""
        video_mix = self.get_video_mix_config()
        return video_mix.get('video_config', {
            'layout': 'portrait',
            'fps': 25,
            'size': '1080x1920',
            'min_segment_length': 5,
            'max_segment_length': 10
        })
    
    def set_video_config(self, config: Dict[str, Any]):
        """设置视频配置"""
        if 'video_mix' not in self.config:
            self.config['video_mix'] = {}
        self.config['video_mix']['video_config'] = config
        self.save_config()
    
    def get_subtitles_config(self) -> Dict[str, Any]:
        """获取字幕配置"""
        video_mix = self.get_video_mix_config()
        return video_mix.get('subtitles', {
            'enable': False,
            'font': 'Songti SC Bold',
            'size': 8,
            'lines': 2,
            'position': 'bottom_center',
            'color': '#FFFFFF',
            'border_color': '#000000',
            'border_width': 0
        })
    
    def set_subtitles_config(self, config: Dict[str, Any]):
        """设置字幕配置"""
        if 'video_mix' not in self.config:
            self.config['video_mix'] = {}
        self.config['video_mix']['subtitles'] = config
        self.save_config()
    
    def get_output_config(self) -> Dict[str, Any]:
        """获取输出配置"""
        video_mix = self.get_video_mix_config()
        return video_mix.get('output', {
            'dir': '',
            'videos_count': 1
        })
    
    def set_output_config(self, config: Dict[str, Any]):
        """设置输出配置"""
        if 'video_mix' not in self.config:
            self.config['video_mix'] = {}
        self.config['video_mix']['output'] = config
        self.save_config()
    
    def get_scenes_config(self) -> list:
        """获取场景配置"""
        video_mix = self.get_video_mix_config()
        return video_mix.get('scenes', [])
    
    def set_scenes_config(self, scenes: list):
        """设置场景配置"""
        self.update_config('video_mix', 'scenes', scenes)
    
    def _read_yaml(self, file_path: str) -> Dict[str, Any]:
        """读取YAML文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"读取配置文件失败: {e}")
            return {}
    
    def _save_yaml(self, file_path: str, data: Dict[str, Any]):
        """保存YAML文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

# 全局配置管理器实例
config_manager = ConfigManager()