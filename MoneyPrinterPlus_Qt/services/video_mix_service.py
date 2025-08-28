"""
视频混剪服务 - PyQt6版本
集成原项目的视频混剪业务逻辑
"""
import os
import sys
import threading
import time
import random
import subprocess
from typing import Dict, List, Optional
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from datetime import datetime

from core.config_manager import config_manager


class VideoMixWorker(QThread):
    """视频生成工作线程"""
    
    # 信号定义
    progress_updated = pyqtSignal(int)  # 进度更新
    status_updated = pyqtSignal(str)    # 状态更新
    error_occurred = pyqtSignal(str)    # 错误发生
    generation_completed = pyqtSignal(str)  # 生成完成
    
    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.is_cancelled = False
    
    def run(self):
        """执行视频生成"""
        try:
            self.status_updated.emit("开始视频生成...")
            self.progress_updated.emit(0)
            
            # 验证配置
            if not self._validate_config():
                return
            
            # 执行真实的视频处理
            output_file = self._process_video()
            if output_file:
                self.generation_completed.emit(output_file)
            
        except Exception as e:
            self.error_occurred.emit(f"生成视频时发生错误: {str(e)}")
    
    def cancel(self):
        """取消生成"""
        self.is_cancelled = True
    
    def _validate_config(self) -> bool:
        """验证配置"""
        try:
            # 检查完整音频配置
            if self.config.get('use_full_audio', False):
                audio_dir = self.config.get('full_audio_dir', '')
                if not audio_dir or not os.path.isdir(audio_dir):
                    self.error_occurred.emit("请设置有效的音频目录")
                    return False
                
                # 检查是否有MP3文件
                mp3_files = [f for f in os.listdir(audio_dir) if f.lower().endswith('.mp3')]
                if not mp3_files:
                    self.error_occurred.emit("音频目录中未找到MP3文件")
                    return False
            
            # 检查场景配置
            scenes = self.config.get('scenes', [])
            if not scenes:
                self.error_occurred.emit("请至少配置一个场景")
                return False
            
            # 检查场景资源目录
            for i, scene in enumerate(scenes):
                resource_dir = scene.get('resource_dir', '')
                if not resource_dir or not os.path.isdir(resource_dir):
                    self.error_occurred.emit(f"场景 {i+1} 的资源目录无效")
                    return False
            
            # 检查输出目录
            output_dir = self.config.get('output', {}).get('dir', '')
            if output_dir and not os.path.isdir(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    self.error_occurred.emit(f"无法创建输出目录: {str(e)}")
                    return False
            
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"配置验证失败: {str(e)}")
            return False
    
    def _process_video(self) -> str:
        """处理视频混剪"""
        try:
            # 步骤1: 选择场景视频
            self.status_updated.emit("选择场景视频...")
            self.progress_updated.emit(10)
            video_files = self._select_scene_videos()
            if not video_files:
                self.error_occurred.emit("未找到可用的视频文件")
                return None
            
            if self.is_cancelled:
                return None
                
            # 步骤2: 选择音频文件
            self.status_updated.emit("选择音频文件...")
            self.progress_updated.emit(20)
            audio_file = self._select_audio_file()
            if not audio_file:
                self.error_occurred.emit("未找到可用的音频文件")
                return None
                
            if self.is_cancelled:
                return None
            
            # 步骤3: 视频标准化
            self.status_updated.emit("标准化视频文件...")
            self.progress_updated.emit(40)
            normalized_videos = self._normalize_videos(video_files)
            if not normalized_videos:
                self.error_occurred.emit("视频标准化失败")
                return None
                
            if self.is_cancelled:
                return None
            
            # 步骤4: 合成最终视频
            self.status_updated.emit("合成最终视频...")
            self.progress_updated.emit(70)
            output_file = self._merge_final_video(normalized_videos, audio_file)
            
            if self.is_cancelled:
                return None
                
            self.status_updated.emit("视频生成完成!")
            self.progress_updated.emit(100)
            return output_file
            
        except Exception as e:
            raise Exception(f"处理视频失败: {str(e)}")
    
    def _select_scene_videos(self) -> List[str]:
        """选择场景视频"""
        video_files = []
        scenes = self.config.get('scenes', [])
        
        for scene in scenes:
            resource_dir = scene.get('resource_dir', '')
            if os.path.isdir(resource_dir):
                # 获取目录中的所有视频文件
                media_files = [os.path.join(resource_dir, f) for f in os.listdir(resource_dir) 
                              if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
                if media_files:
                    # 随机选择一个文件
                    selected_video = random.choice(media_files)
                    video_files.append(selected_video)
                    print(f"选择视频: {selected_video}")
        
        return video_files
    
    def _select_audio_file(self) -> Optional[str]:
        """选择音频文件"""
        if not self.config.get('use_full_audio', True):
            return None
            
        audio_dir = self.config.get('full_audio_dir', '')
        if not audio_dir or not os.path.isdir(audio_dir):
            return None
            
        # 获取所有MP3文件
        mp3_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) 
                    if f.lower().endswith('.mp3')]
        
        if mp3_files:
            selected_audio = random.choice(mp3_files)
            print(f"选择音频: {selected_audio}")
            return selected_audio
        
        return None
    
    def _normalize_videos(self, video_files: List[str]) -> List[str]:
        """标准化视频文件"""
        normalized_videos = []
        video_config = self.config.get('video_config', {})
        
        # 获取目标分辨率
        size = video_config.get('size', '1080x1920')
        target_width, target_height = map(int, size.split('x'))
        fps = video_config.get('fps', 25)
        
        work_dir = self._get_work_dir()
        
        for i, video_file in enumerate(video_files):
            if self.is_cancelled:
                return []
                
            try:
                # 生成临时文件名
                temp_filename = f"normalized_{i}_{int(time.time())}.mp4"
                output_file = os.path.join(work_dir, temp_filename)
                
                # 构造ffmpeg命令
                cmd = [
                    'ffmpeg',
                    '-i', video_file,
                    '-vf', f'scale={target_width}:{target_height}:force_original_aspect_ratio=decrease,pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2',
                    '-r', str(fps),
                    '-c:v', 'libx264',
                    '-preset', 'fast',
                    '-y',
                    output_file
                ]
                
                print(f"执行FFmpeg命令: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', check=True)
                normalized_videos.append(output_file)
                print(f"视频标准化完成: {output_file}")
                    
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg处理失败: {e.stderr}")
                raise Exception(f"FFmpeg处理失败: {e.stderr}")
            except Exception as e:
                print(f"处理视频 {video_file} 失败: {str(e)}")
                raise
        
        return normalized_videos
    
    def _merge_final_video(self, video_files: List[str], audio_file: Optional[str]) -> str:
        """合成最终视频 - 采用原项目的两步法：先合并视频，再添加音频"""
        output_file = self._generate_output_filename()
        work_dir = self._get_work_dir()
        
        try:
            # 步骤1: 合并视频（不带音频），参考原项目的实现方式
            temp_video_file = os.path.join(work_dir, f"temp_merged_{int(time.time())}.mp4")
            filelist_path = os.path.join(work_dir, f"filelist_{int(time.time())}.txt")
            
            with open(filelist_path, 'w', encoding='utf-8') as f:
                for video_file in video_files:
                    escaped_path = video_file.replace('\\', '/')
                    f.write(f"file '{escaped_path}'\n")
            
            # 检查是否需要添加固定字幕
            subtitle_filters = self._generate_subtitle_filters()
            
            # 先合并视频（无音频）
            if subtitle_filters:
                # 带字幕的视频合并
                video_merge_cmd = [
                    'ffmpeg',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', filelist_path,
                    '-vf', subtitle_filters,
                    '-c:v', 'libx264',
                    '-fflags', '+genpts',  # 参考原项目的参数
                    '-y',
                    temp_video_file
                ]
            else:
                # 无字幕的视频合并（参考原项目）
                video_merge_cmd = [
                    'ffmpeg',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', filelist_path,
                    '-c', 'copy',
                    '-fflags', '+genpts',  # 参考原项目的参数
                    '-y',
                    temp_video_file
                ]
            
            print(f"步骤1 - 合并视频: {' '.join(video_merge_cmd)}")
            result = subprocess.run(video_merge_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', check=True)
            print(f"视频合并完成: {temp_video_file}")
            
            # 步骤2: 添加音频（参考原项目的add_music函数）
            if audio_file:
                audio_add_cmd = [
                    'ffmpeg',
                    '-i', temp_video_file,  # 输入视频文件
                    '-i', audio_file,       # 输入音频文件
                    '-c:v', 'copy',         # 复制视频流编码
                    '-c:a', 'aac',          # 使用AAC编码音频流
                    '-strict', 'experimental',  # 启用AAC编码
                    '-map', '0:v:0',        # 选择第一个输入文件的视频流
                    '-map', '1:a:0',        # 选择第二个输入文件的音频流
                    '-shortest',            # 使用最短的流的长度
                    '-y',
                    output_file
                ]
                
                print(f"步骤2 - 添加音频: {' '.join(audio_add_cmd)}")
                result = subprocess.run(audio_add_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', check=True)
                print(f"音频添加完成: {output_file}")
                
                # 删除临时视频文件
                if os.path.exists(temp_video_file):
                    os.remove(temp_video_file)
            else:
                # 无音频时，直接重命名临时文件
                if os.path.exists(temp_video_file):
                    os.rename(temp_video_file, output_file)
                    print(f"无音频视频生成完成: {output_file}")
            
            # 清理临时文件
            try:
                os.remove(filelist_path)
                for temp_file in video_files:
                    if os.path.exists(temp_file) and work_dir in temp_file:
                        os.remove(temp_file)
            except:
                pass  # 忽略清理错误
            
            return output_file
                
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg处理错误: {e.stderr}")
            # 清理可能的临时文件
            temp_video_file = os.path.join(work_dir, f"temp_merged_{int(time.time())}.mp4")
            if os.path.exists(temp_video_file):
                os.remove(temp_video_file)
            raise Exception(f"FFmpeg处理失败: {e.stderr}")
        except Exception as e:
            print(f"合成视频失败: {str(e)}")
            raise
    
    def _generate_subtitle_filters(self) -> Optional[str]:
        """生成固定字幕滤镜，基于原项目FancyTextService的实现方案"""
        try:
            # 获取固定字幕配置
            fixed_subtitles_config = self.config.get('fixed_subtitles', {})
            if not fixed_subtitles_config.get('enable', False):
                return None
                
            # 获取字幕文件路径
            subtitle_file = fixed_subtitles_config.get('file_path', '')
            if not subtitle_file or not os.path.isfile(subtitle_file):
                return None
            
            # 读取字幕内容
            subtitle_lines = self._read_subtitle_file(subtitle_file)
            if not subtitle_lines:
                return None
            
            # 基于原项目方案：使用字体文件路径和完整的drawtext参数
            font_size = fixed_subtitles_config.get('font_size', 48)
            font_color = fixed_subtitles_config.get('font_color', '#FFFFFF')
            line_spacing = fixed_subtitles_config.get('line_spacing', 40)
            
            # 获取字体文件路径（使用原项目的方法）
            font_path = self._get_font_path_from_original_project()
            
            # 生成drawtext滤镜（参考原项目的方式）
            drawtext_filters = []
            
            # 基础Y位置（中间偏上）
            base_y = "h*0.2"
            
            for i, line in enumerate(subtitle_lines):
                if not line.strip():
                    continue
                
                # 计算当前行的Y位置
                if i == 0:
                    current_y = base_y
                else:
                    current_y = f"{base_y}+{i * line_spacing}"
                
                # 构造drawtext参数（参考原项目的完整实现）
                drawtext_params = [
                    f"fontfile={font_path}" if font_path else "",
                    f"text='{self._escape_text_for_ffmpeg(line)}'",
                    f"fontsize={font_size}",
                    f"fontcolor={font_color}",
                    "x=(w-text_w)/2",  # 水平居中
                    f"y={current_y}"
                ]
                
                # 移除空参数
                drawtext_params = [param for param in drawtext_params if param]
                
                drawtext_filter = "drawtext=" + ":".join(drawtext_params)
                drawtext_filters.append(drawtext_filter)
            
            # 组合多个drawtext滤镜
            return ','.join(drawtext_filters) if drawtext_filters else None
                
        except Exception as e:
            print(f"生成字幕滤镜失败: {str(e)}")
            return None
    
    def _read_subtitle_file(self, file_path: str) -> List[str]:
        """读取字幕文件，随机选择最多3行"""
        try:
            # 尝试多种编码方式
            encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                # 如果所有编码都失败，使用默认编码并忽略错误
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            
            # 清理换行符并过滤空行
            all_lines = []
            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    all_lines.append(clean_line)
            
            # 如果文件为空，返回空列表
            if not all_lines:
                return []
            
            # 随机选择最多3行
            max_lines = min(3, len(all_lines))
            selected_lines = random.sample(all_lines, max_lines)
            
            return selected_lines
            
        except Exception as e:
            print(f"读取字幕文件失败 {file_path}: {str(e)}")
            return []
    
    def _get_font_path_from_original_project(self) -> Optional[str]:
        """获取字体文件路径，基于原项目的方法"""
        try:
            # 获取项目根目录下的字体目录
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_dir = os.path.dirname(script_dir)
            font_dir = os.path.join(project_dir, "fonts")
            
            # 查找可用的字体文件（优先使用PingFang，然后是其他字体）
            font_files = [
                "PingFang.ttc",
                "Songti.ttc", 
                "STSong.ttf",
                "Arial.ttf",
                "arial.ttf"
            ]
            
            for font_file in font_files:
                font_path = os.path.join(font_dir, font_file)
                if os.path.isfile(font_path):
                    # Windows路径处理（参考原项目的处理方式）
                    if os.name == 'nt':  # Windows系统
                        font_path = font_path.replace("\\", "\\\\\\\\")
                        font_path = font_path.replace(":", "\\\\:")
                    return font_path
            
            # 如果没找到字体文件，返回None让FFmpeg使用默认字体
            return None
            
        except Exception as e:
            print(f"获取字体路径失败: {str(e)}")
            return None
    
    def _escape_text_for_ffmpeg(self, text: str) -> str:
        """为FFmpeg转义文本中的特殊字符（基于原项目的方法）"""
        # 基于原项目FancyTextService的转义方式
        # 只转义必要的字符，避免过度转义
        text = text.replace("'", r"\'")
        text = text.replace(":", r"\:")
        return text

    def _get_work_dir(self) -> str:
        """获取工作目录"""
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_dir = os.path.dirname(script_dir)
        work_dir = os.path.join(project_dir, "work")
        os.makedirs(work_dir, exist_ok=True)
        return work_dir
        
    def _generate_output_filename(self) -> str:
        """生成输出文件名"""
        
        output_config = self.config.get('output', {})
        output_dir = output_config.get('dir', '')
        
        if not output_dir:
            # 使用项目根目录下的final文件夹作为默认输出目录
            # 从 MoneyPrinterPlus_Qt/services/video_mix_service.py 导航到 MoneyPrinterPlus/final
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # MoneyPrinterPlus_Qt
            project_dir = os.path.dirname(script_dir)  # MoneyPrinterPlus
            output_dir = os.path.join(project_dir, "final")
            os.makedirs(output_dir, exist_ok=True)
        
        # 生成基于日期的文件名
        today = datetime.now().strftime('%Y-%m-%d')
        
        # 找到今天的最大序号
        existing_files = [f for f in os.listdir(output_dir) 
                         if f.startswith(f"mix_{today}_") and f.endswith('.mp4')]
        
        if existing_files:
            # 提取序号并找到最大值
            numbers = []
            for f in existing_files:
                try:
                    num_str = f.replace(f"mix_{today}_", "").replace('.mp4', '')
                    numbers.append(int(num_str))
                except:
                    pass
            next_num = max(numbers) + 1 if numbers else 1
        else:
            next_num = 1
        
        filename = f"mix_{today}_{next_num:02d}.mp4"
        return os.path.join(output_dir, filename)


class VideoMixService(QObject):
    """视频混剪服务"""
    
    def __init__(self):
        super().__init__()
        self.worker_thread = None
    
    def generate_video(self, progress_callback=None, status_callback=None, 
                      error_callback=None, completion_callback=None):
        """开始生成视频"""
        if self.worker_thread and self.worker_thread.isRunning():
            if error_callback:
                error_callback("已有视频生成任务在运行中")
            return False
        
        try:
            # 获取当前配置
            config = self._get_generation_config()
            
            # 创建工作线程
            self.worker_thread = VideoMixWorker(config)
            
            # 连接信号
            if progress_callback:
                self.worker_thread.progress_updated.connect(progress_callback)
            
            if status_callback:
                self.worker_thread.status_updated.connect(status_callback)
            
            if error_callback:
                self.worker_thread.error_occurred.connect(error_callback)
            
            if completion_callback:
                self.worker_thread.generation_completed.connect(completion_callback)
            
            # 启动线程
            self.worker_thread.start()
            return True
            
        except Exception as e:
            if error_callback:
                error_callback(f"启动生成任务失败: {str(e)}")
            return False
    
    def cancel_generation(self):
        """取消生成"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.cancel()
            self.worker_thread.wait(5000)  # 等待最多5秒
            if self.worker_thread.isRunning():
                self.worker_thread.terminate()
    
    def is_generating(self) -> bool:
        """检查是否正在生成"""
        return self.worker_thread and self.worker_thread.isRunning()
    
    def _get_generation_config(self) -> Dict:
        """获取生成配置"""
        try:
            # 从配置管理器获取配置
            full_audio_config = config_manager.get_full_audio_config()
            scenes_config = config_manager.get_scenes_config()
            video_config = config_manager.get_video_config()
            fixed_subtitle_config = config_manager.get_fixed_subtitles_config()
            output_config = config_manager.get_output_config()
            
            return {
                'use_full_audio': full_audio_config.get('use_full_audio', True),
                'full_audio_dir': full_audio_config.get('full_audio_dir', ''),
                'scenes': scenes_config,
                'video_config': video_config,
                'fixed_subtitles': fixed_subtitle_config,
                'output': output_config
            }
            
        except Exception as e:
            raise Exception(f"获取配置失败: {str(e)}")
    
    def get_available_video_files(self, directory: str) -> List[str]:
        """获取可用的视频文件"""
        try:
            from tools.video_usage_tracker import get_video_usage_tracker
            
            tracker = get_video_usage_tracker()
            return tracker.get_available_files(directory)
            
        except Exception as e:
            print(f"获取可用视频文件失败: {e}")
            return []
    
    def record_video_usage(self, file_path: str) -> bool:
        """记录视频文件使用"""
        try:
            from tools.video_usage_tracker import get_video_usage_tracker
            
            tracker = get_video_usage_tracker()
            return tracker.record_usage(file_path)
            
        except Exception as e:
            print(f"记录视频使用失败: {e}")
            return False


# 全局服务实例
_video_mix_service = None


def get_video_mix_service() -> VideoMixService:
    """获取视频混剪服务实例"""
    global _video_mix_service
    if _video_mix_service is None:
        _video_mix_service = VideoMixService()
    return _video_mix_service