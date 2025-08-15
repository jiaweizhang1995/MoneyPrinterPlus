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
#

import itertools
import math
import os
import random
import re
import subprocess
from typing import List
import streamlit as st

from PIL import Image

from services.video.texiao_service import gen_filter
from services.video.fancy_text_service import FancyTextService
from tools.file_utils import generate_temp_filename
from tools.tr_utils import tr
from tools.utils import random_with_system_time, run_ffmpeg_command, extent_audio
from tools.video_naming_utils import generate_daily_video_filename

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 视频出目录
video_output_dir = os.path.join(script_dir, "../../final")
video_output_dir = os.path.abspath(video_output_dir)

# work目录
work_output_dir = os.path.join(script_dir, "../../work")
work_output_dir = os.path.abspath(work_output_dir)

DEFAULT_DURATION = 5


def get_audio_duration(audio_file):
    """
    获取音频文件的时长（秒）
    :param audio_file: 音频文件路径
    :return: 音频时长（秒），如果失败则返回None
    """
    # 使用ffmpeg命令获取音频信息
    cmd = ['ffmpeg', '-i', audio_file]
    print(" ".join(cmd))
    result = subprocess.run(cmd, capture_output=True)

    # 解析输出，找到时长信息
    duration_search = re.search(
        r'Duration: (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)\.(?P<milliseconds>\d+)',
        result.stderr.decode('utf-8'))
    if duration_search:
        hours = int(duration_search.group('hours'))
        minutes = int(duration_search.group('minutes'))
        seconds = int(duration_search.group('seconds'))
        total_seconds = hours * 3600 + minutes * 60 + seconds
        print("音频时长:", total_seconds)
        return total_seconds
    else:
        print(f"无法从输出中获取音频时长: {result.stderr.decode('utf-8')}")
        return None


def get_video_fps(video_path):
    # ffprobe 命令，用于获取视频的帧率
    ffprobe_cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=r_frame_rate',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    print(" ".join(ffprobe_cmd))

    try:
        # 运行 ffprobe 命令并捕获输出
        result = subprocess.run(ffprobe_cmd, capture_output=True)
        stdout = result.stdout.decode('gbk', errors='ignore')
        stderr = result.stderr.decode('gbk', errors='ignore')

        # 检查命令是否成功执行
        if result.returncode != 0:
            print(f"Error running ffprobe: {result.stderr}")
            return None

        # 解析输出以获取帧率
        output = result.stdout.strip()
        if '/' in output:
            numerator, denominator = map(int, output.split('/'))
            fps = float(numerator) / float(denominator)
        else:
            fps = float(output)
        print("视频fps:", fps)
        return fps
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_video_info(video_file):
    command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of',
               'default=noprint_wrappers=1:nokey=1', video_file]
    print(" ".join(command))
    result = subprocess.run(command, capture_output=True)

    # 解析输出以获取宽度和高度
    output = result.stdout.decode('utf-8')
    # print("output is:",output)
    width_height = output.split('\n')
    width = int(width_height[0])
    height = int(width_height[1])

    print(f'Width: {width}, Height: {height}')
    return width, height


def get_image_info(image_file):
    # 打开图片
    img = Image.open(image_file)
    # 获取图片的宽度和高度
    width, height = img.size
    print(f'Width: {width}, Height: {height}')
    return width, height


def get_video_duration(video_file):
    # 构建FFmpeg命令来获取视频时长
    command = ['ffprobe', '-i', video_file, '-show_entries', 'format=duration']
    # 执行命令并捕获输出
    print(" ".join(command))
    result = subprocess.run(command, capture_output=True)
    output = result.stdout.decode('utf-8')

    # 使用正则表达式从输出中提取时长
    duration_match = re.search(r'duration=(\d+\.\d+)', output)
    if duration_match:
        duration = float(duration_match.group(1))
        print("视频时长:", duration)
        return duration
    else:
        print(f"无法从输出中提取视频时长: {output}")
        return None


def get_video_length_list(video_list):
    video_length_list = []
    for video_file in video_list:
        length = get_video_duration(video_file)
        video_length_list.append(length)
    return video_length_list


def add_music(video_file, audio_file):
    output_file = generate_temp_filename(video_file)
    # 构造ffmpeg命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_file,  # 输入视频文件
        '-i', audio_file,  # 输入音频文件
        '-c:v', 'copy',  # 复制视频流编码
        '-c:a', 'aac',  # 使用AAC编码音频流
        '-strict', 'experimental',  # 有时可能需要这个选项来启用AAC编码
        '-map', '0:v:0',  # 选择第一个输入文件的视频流
        '-map', '1:a:0',  # 选择第二个输入文件的音频流
        '-shortest',
        '-y',
        output_file  # 输出文件路径
    ]
    print(" ".join(ffmpeg_cmd))
    try:
        result = subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
        print("视频音频合成成功")
        # 重命名最终的文件
        if os.path.exists(output_file):
            os.remove(video_file)
            os.renames(output_file, video_file)
        else:
            print(f"错误：输出文件不存在 {output_file}")
            raise FileNotFoundError(f"FFmpeg未能生成输出文件: {output_file}")
    except subprocess.CalledProcessError as e:
        stdout = e.stdout.decode('gbk', errors='ignore') if e.stdout else ""
        stderr = e.stderr.decode('gbk', errors='ignore') if e.stderr else ""
        print(f"FFmpeg视频音频合成失败:")
        print(f"命令: {' '.join(ffmpeg_cmd)}")
        print(f"返回码: {e.returncode}")
        print(f"标准输出: {stdout}")
        print(f"错误输出: {stderr}")
        raise Exception(f"视频音频合成失败: {stderr}")
    except Exception as e:
        print(f"视频音频合成过程中发生错误: {e}")
        raise


def add_background_music(video_file, audio_file, bgm_volume=0.5):
    output_file = generate_temp_filename(video_file)
    # 构建FFmpeg命令
    command = [
        'ffmpeg',
        '-i', video_file,  # 输入视频文件
        '-i', audio_file,  # 输入音频文件（背景音乐）
        '-filter_complex',
        f"[1:a]aloop=loop=0:size=100M[bgm];[bgm]volume={bgm_volume}[bgm_vol];[0:a][bgm_vol]amix=duration=first:dropout_transition=3:inputs=2[a]",
        # 在[1:a]之后添加了aloop过滤器来循环背景音乐。loop=0表示无限循环，size=200M和duration=300是可选参数，用于设置循环音频的大小或时长（这里设置得很大以确保足够长，可以根据实际需要调整），start=0表示从音频的开始处循环。
        '-map', '0:v',  # 选择视频流
        '-map', '[a]',  # 选择混合后的音频流
        '-c:v', 'copy',  # 复制视频流
        '-shortest',  # 输出时长与最短的输入流相同
        output_file  # 输出文件
    ]
    # 调用FFmpeg命令
    print(" ".join(command))
    try:
        result = subprocess.run(command, capture_output=True, check=True)
        print("背景音乐添加成功")
        # 重命名最终的文件
        if os.path.exists(output_file):
            os.remove(video_file)
            os.renames(output_file, video_file)
        else:
            print(f"错误：背景音乐输出文件不存在 {output_file}")
            raise FileNotFoundError(f"FFmpeg未能生成背景音乐输出文件: {output_file}")
    except subprocess.CalledProcessError as e:
        stdout = e.stdout.decode('gbk', errors='ignore') if e.stdout else ""
        stderr = e.stderr.decode('gbk', errors='ignore') if e.stderr else ""
        print(f"FFmpeg背景音乐添加失败:")
        print(f"命令: {' '.join(command)}")
        print(f"返回码: {e.returncode}")
        print(f"标准输出: {stdout}")
        print(f"错误输出: {stderr}")
        raise Exception(f"背景音乐添加失败: {stderr}")
    except Exception as e:
        print(f"背景音乐添加过程中发生错误: {e}")
        raise


class VideoMixService:
    def __init__(self):
        self.fps = st.session_state["video_fps"]
        self.segment_min_length = st.session_state["video_segment_min_length"]
        self.segment_max_length = st.session_state["video_segment_max_length"]
        self.target_width, self.target_height = st.session_state["video_size"].split('x')
        self.target_width = int(self.target_width)
        self.target_height = int(self.target_height)

        self.enable_background_music = st.session_state["enable_background_music"]
        self.background_music = st.session_state["background_music"]
        self.background_music_volume = st.session_state["background_music_volume"]

        self.enable_video_transition_effect = st.session_state["enable_video_transition_effect"]
        self.video_transition_effect_duration = st.session_state["video_transition_effect_duration"]
        self.video_transition_effect_type = st.session_state["video_transition_effect_type"]
        self.video_transition_effect_value = st.session_state["video_transition_effect_value"]
        self.default_duration = DEFAULT_DURATION
        if DEFAULT_DURATION < self.segment_min_length:
            self.default_duration = self.segment_min_length

    def match_videos_from_dir(self, video_dir, audio_file, is_head=False):
        matching_videos = []
        # 获取音频时长
        audio_duration = get_audio_duration(audio_file)
        print("音频时长:" + str(audio_duration))

        # 获取媒体文件夹中的所有图片和视频文件
        media_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if
                       f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]

        # 随机排序媒体文件
        random.shuffle(media_files)

        # 确保有视频文件在列表中
        video_files = [os.path.join(video_dir, f) for f in media_files if f.lower().endswith(('.mp4', '.mov'))]
        if video_files:
            # 从视频文件中随机选择一个
            random_video = random.choice(video_files)
            # 将随机选择的视频文件从列表中移除
            media_files.remove(random_video)
            # 将随机选择的视频文件添加到列表的开头
            media_files.insert(0, random_video)

        total_length = 0
        i = 0
        for video_file in media_files:
            if video_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                video_duration = self.default_duration
            else:
                video_duration = get_video_duration(video_file)
            # 短的视频拉长到最小值
            if video_duration < self.segment_min_length:
                video_duration = self.segment_min_length
            if video_duration > self.segment_max_length:
                video_duration = self.segment_max_length

            print("total length:", total_length, "audio length:", audio_duration)
            if total_length < audio_duration:
                if self.enable_video_transition_effect:
                    if i == 0 and is_head:
                        total_length = total_length + video_duration
                    else:
                        total_length = total_length + video_duration - float(
                            self.video_transition_effect_duration)
                else:
                    total_length = total_length + video_duration
                matching_videos.append(video_file)
                i = i + 1
            else:
                extend_length = audio_duration - total_length
                extend_length = int(math.ceil(extend_length))
                if extend_length > 0:
                    extent_audio(audio_file, extend_length)
                break
        print("total length:", total_length, "audio length:", audio_duration)
        if total_length < audio_duration:
            st.toast(tr("You Need More Resource"), icon="⚠️")
            st.stop()
        return matching_videos, total_length

    def match_videos_from_dir_full_audio(self, video_dir, complete_audio_file, is_head=False):
        """
        完整音频模式下的视频匹配方法
        为每个视频目录分配音频时长的一部分
        """
        matching_videos = []
        
        # 获取完整音频时长和场景信息
        total_audio_duration = st.session_state.get("full_audio_duration", 0)
        scene_count = len(st.session_state.get("video_dir_list", []))
        
        if scene_count == 0 or total_audio_duration == 0:
            print("警告：无法获取完整音频信息")
            return matching_videos, 0
        
        # 计算当前场景应该占用的音频时长（均匀分配）
        segment_duration = total_audio_duration / scene_count
        
        print(f"完整音频模式匹配视频：目标时长 {segment_duration:.2f}秒")
        
        # 获取媒体文件夹中的所有图片和视频文件
        media_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if
                       f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]

        # 随机排序媒体文件
        random.shuffle(media_files)

        # 确保有视频文件在列表中
        video_files = [f for f in media_files if f.lower().endswith(('.mp4', '.mov'))]
        if video_files:
            # 从视频文件中随机选择一个
            random_video = random.choice(video_files)
            # 将随机选择的视频文件从列表中移除
            media_files.remove(random_video)
            # 将随机选择的视频文件添加到列表的开头
            media_files.insert(0, random_video)

        total_length = 0
        i = 0
        for video_file in media_files:
            if video_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                video_duration = self.default_duration
            else:
                video_duration = get_video_duration(video_file)
            
            # 短的视频拉长到最小值
            if video_duration < self.segment_min_length:
                video_duration = self.segment_min_length
            if video_duration > self.segment_max_length:
                video_duration = self.segment_max_length

            print(f"视频文件: {video_file}, 时长: {video_duration}秒")
            
            if total_length < segment_duration:
                if self.enable_video_transition_effect:
                    if i == 0 and is_head:
                        total_length = total_length + video_duration
                    else:
                        total_length = total_length + video_duration - float(
                            self.video_transition_effect_duration)
                else:
                    total_length = total_length + video_duration
                matching_videos.append(video_file)
                i = i + 1
                
                print(f"累计时长: {total_length:.2f}秒, 目标: {segment_duration:.2f}秒")
            else:
                break
        
        print(f"场景视频匹配完成：实际时长 {total_length:.2f}秒, 目标时长 {segment_duration:.2f}秒")
        
        if total_length < segment_duration * 0.8:  # 如果实际时长小于目标时长的80%，给出警告
            print(f"警告：视频素材可能不足，实际时长 {total_length:.2f}秒 < 目标时长 {segment_duration:.2f}秒")
            # 在完整音频模式下，如果视频素材不足，我们不能延长音频
            # 但可以通过重复最后一个视频来填充时间
            if matching_videos:
                last_video = matching_videos[-1]
                while total_length < segment_duration:
                    if last_video.lower().endswith(('.jpg', '.jpeg', '.png')):
                        additional_duration = min(self.default_duration, segment_duration - total_length)
                    else:
                        video_duration = get_video_duration(last_video)
                        additional_duration = min(video_duration, segment_duration - total_length)
                    
                    matching_videos.append(last_video)
                    total_length += additional_duration
                    print(f"重复视频片段以填充时长，当前累计: {total_length:.2f}秒")
                    
                    if len(matching_videos) > 20:  # 避免无限循环
                        print("警告：为避免无限循环，停止添加视频片段")
                        break
        
        return matching_videos, total_length


class VideoService:
    def __init__(self, video_list, audio_file):
        self.video_list = video_list
        self.audio_file = audio_file
        self.fps = st.session_state["video_fps"]
        self.seg_min_duration = st.session_state["video_segment_min_length"]
        self.seg_max_duration = st.session_state["video_segment_max_length"]
        self.target_width, self.target_height = st.session_state["video_size"].split('x')
        self.target_width = int(self.target_width)
        self.target_height = int(self.target_height)

        self.enable_background_music = st.session_state["enable_background_music"]
        self.background_music = st.session_state["background_music"]
        self.background_music_volume = st.session_state["background_music_volume"]

        self.enable_video_transition_effect = st.session_state["enable_video_transition_effect"]
        self.video_transition_effect_duration = st.session_state["video_transition_effect_duration"]
        self.video_transition_effect_type = st.session_state["video_transition_effect_type"]
        self.video_transition_effect_value = st.session_state["video_transition_effect_value"]
        self.default_duration = DEFAULT_DURATION
        if DEFAULT_DURATION < self.seg_min_duration:
            self.default_duration = self.seg_min_duration

    def normalize_video(self):
        return_video_list = []
        for media_file in self.video_list:
            # 如果当前文件是图片，添加转换为视频的命令
            if media_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                output_name = generate_temp_filename(media_file, ".mp4", work_output_dir)
                # 判断图片的纵横比和
                img_width, img_height = get_image_info(media_file)
                if img_width / img_height > self.target_width / self.target_height:
                    # 转换图片为视频片段 图片的视频帧率必须要跟视频的帧率一样，否则可能在最后的合并过程中导致 合并过后的视频过长
                    # ffmpeg_cmd = f"ffmpeg -loop 1 -i '{media_file}' -c:v h264 -t {self.default_duration} -r {self.fps} -vf 'scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2' -y {output_name}"
                    ffmpeg_cmd = [
                        'ffmpeg',
                        '-loop', '1',
                        '-i', media_file,
                        '-c:v', 'h264',
                        '-t', str(self.default_duration),
                        '-r', str(self.fps),
                        '-vf',
                        f'scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                        '-y', output_name]
                else:
                    # ffmpeg_cmd = f"ffmpeg -loop 1 -i '{media_file}' -c:v h264 -t {self.default_duration} -r {self.fps} -vf 'scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2' -y {output_name}"
                    ffmpeg_cmd = [
                        'ffmpeg',
                        '-loop', '1',
                        '-i', media_file,
                        '-c:v', 'h264',
                        '-t', str(self.default_duration),
                        '-r', str(self.fps),
                        '-vf',
                        f'scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                        '-y', output_name]
                print(" ".join(ffmpeg_cmd))
                subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
                return_video_list.append(output_name)

            else:
                # 当前文件是视频文件
                video_duration = get_video_duration(media_file)
                video_width, video_height = get_video_info(media_file)
                output_name = generate_temp_filename(media_file, new_directory=work_output_dir)
                if self.seg_min_duration > video_duration:
                    # 需要扩展视频
                    stretch_factor = float(self.seg_min_duration) / float(video_duration)  # 拉长比例
                    # 构建FFmpeg命令
                    if video_width / video_height > self.target_width / self.target_height:
                        command = [
                            'ffmpeg',
                            '-i', media_file,  # 输入文件
                            '-r', str(self.fps),  # 设置帧率
                            '-an',  # 去除音频
                            '-vf',
                            f"setpts={stretch_factor}*PTS,scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                            # 调整时间戳滤镜
                            # '-vf', f'scale=-1:{self.target_height}:force_original_aspect_ratio=1',  # 设置视频滤镜来调整分辨率
                            # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                            # '-af', f'atempo={1 / stretch_factor}',  # 调整音频速度以匹配视频
                            '-y',
                            output_name  # 输出文件
                        ]
                    else:
                        command = [
                            'ffmpeg',
                            '-i', media_file,  # 输入文件
                            '-r', str(self.fps),  # 设置帧率
                            '-an',  # 去除音频
                            '-vf',
                            f"setpts={stretch_factor}*PTS,scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                            # 调整时间戳滤镜
                            # '-vf', f'scale={self.target_width}:-1:force_original_aspect_ratio=1',  # 设置视频滤镜来调整分辨率
                            # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                            # '-af', f'atempo={1 / stretch_factor}',  # 调整音频速度以匹配视频
                            '-y',
                            output_name  # 输出文件
                        ]
                    # 执行FFmpeg命令
                    print(" ".join(command))
                    run_ffmpeg_command(command)
                elif self.seg_max_duration < video_duration:
                    # 需要裁减视频
                    if video_width / video_height > self.target_width / self.target_height:
                        cmd = [
                            'ffmpeg',
                            '-i', media_file,
                            '-r', str(self.fps),  # 设置帧率
                            '-an',  # 去除音频
                            # '-ss', '00:00:00',
                            '-t', str(self.seg_max_duration),
                            # '-c', 'copy',
                            # '-vcodec', 'copy',
                            # '-acodec', 'copy',
                            '-vf',
                            f"scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                            # 设置视频滤镜来调整分辨率
                            # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                            '-y',
                            output_name
                        ]
                    else:
                        cmd = [
                            'ffmpeg',
                            '-i', media_file,
                            '-r', str(self.fps),  # 设置帧率
                            '-an',  # 去除音频
                            # '-ss', '00:00:00',
                            '-t', str(self.seg_max_duration),
                            # '-c', 'copy',
                            # '-vcodec', 'copy',
                            # '-acodec', 'copy',
                            '-vf',
                            f"scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                            # 设置视频滤镜来调整分辨率
                            # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                            '-y',
                            output_name
                        ]
                    print(" ".join(cmd))
                    run_ffmpeg_command(cmd)
                else:
                    # 不需要拉伸也不需要裁剪，只需要调整分辨率和fps
                    if video_width / video_height > self.target_width / self.target_height:
                        command = [
                            'ffmpeg',
                            '-i', media_file,  # 输入文件
                            '-r', str(self.fps),  # 设置帧率
                            '-an',  # 去除音频
                            '-vf',
                            f"scale=-1:{self.target_height}:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                            # 设置视频滤镜来调整分辨率
                            # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                            '-y',
                            output_name  # 输出文件
                        ]
                    else:
                        command = [
                            'ffmpeg',
                            '-i', media_file,  # 输入文件
                            '-r', str(self.fps),  # 设置帧率
                            '-an',  # 去除音频
                            '-vf',
                            f"scale={self.target_width}:-1:force_original_aspect_ratio=1,crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2",
                            # 设置视频滤镜来调整分辨率
                            # '-vf', f'crop={self.target_width}:{self.target_height}:(ow-iw)/2:(oh-ih)/2',
                            '-y',
                            output_name  # 输出文件
                        ]
                    # 执行FFmpeg命令
                    print(" ".join(command))
                    run_ffmpeg_command(command)
                # 重命名最终的文件
                # if os.path.exists(output_name):
                #     os.remove(media_file)
                #     os.renames(output_name, media_file)
                return_video_list.append(output_name)
        self.video_list = return_video_list
        return return_video_list

    def generate_video_with_audio(self):
        # 生成视频和音频的代码
        merge_video = generate_daily_video_filename(video_output_dir)
        temp_video_filelist_path = os.path.join(video_output_dir, 'generate_video_with_audio_file_list.txt')

        # 创建包含所有视频文件的文本文件
        with open(temp_video_filelist_path, 'w') as f:
            for video_file in self.video_list:
                f.write(f"file '{video_file}'\n")

        # 拼接视频
        ffmpeg_concat_cmd = ['ffmpeg',
                             '-f', 'concat',
                             '-safe', '0',
                             '-i', temp_video_filelist_path,
                             '-c', 'copy',
                             '-fflags',
                             '+genpts',
                             '-y',
                             merge_video]

        # 是否需要转场特效
        if self.enable_video_transition_effect and len(self.video_list) > 1:
            video_length_list = get_video_length_list(self.video_list)
            print("启动转场特效")
            zhuanchang_txt = gen_filter(video_length_list, None, None,
                                        self.video_transition_effect_type,
                                        self.video_transition_effect_value,
                                        self.video_transition_effect_duration,
                                        False)

            # File inputs from the list
            files_input = [['-i', f] for f in self.video_list]
            ffmpeg_concat_cmd = ['ffmpeg', *itertools.chain(*files_input),
                                 '-filter_complex', zhuanchang_txt,
                                 '-map', '[video]',
                                 # '-map', '[audio]',
                                 '-y',
                                 merge_video]

        subprocess.run(ffmpeg_concat_cmd)
        # 删除临时文件
        os.remove(temp_video_filelist_path)

        # 验证视频文件的完整性
        if not self.verify_video_file(merge_video):
            raise Exception(f"生成的视频文件损坏或不完整: {merge_video}")
        
        # 添加花式文本叠加
        self.apply_fancy_text_overlays(merge_video)
        
        # 拼接音频
        add_music(merge_video, self.audio_file)

        # 添加背景音乐
        if self.enable_background_music:
            add_background_music(merge_video, self.background_music, self.background_music_volume)
        return merge_video
    
    def apply_fancy_text_overlays(self, video_file):
        """
        为视频添加花式文本叠加效果
        """
        try:
            # 检查是否启用花式文本功能
            if not st.session_state.get('enable_fancy_text', False):
                print("花式文本功能未启用，跳过文本叠加")
                return
            
            print("开始添加花式文本叠加...")
            
            # 初始化花式文本服务
            fancy_service = FancyTextService()
            if not fancy_service.is_enabled():
                print("花式文本服务未启用，跳过文本叠加")
                return
            
            # 获取视频信息
            video_duration = get_video_duration(video_file)
            video_width, video_height = get_video_info(video_file)
            
            if not video_duration or not video_width or not video_height:
                print("无法获取视频信息，跳过文本叠加")
                return
            
            print(f"视频信息: 时长={video_duration}秒, 分辨率={video_width}x{video_height}")
            
            # 生成花式文本滤镜
            fancy_filter = fancy_service.generate_complete_filter_complex(
                video_duration, video_width, video_height
            )
            
            if not fancy_filter:
                print("未生成花式文本滤镜，跳过文本叠加")
                return
            
            print(f"生成的花式文本滤镜: {fancy_filter}")
            
            # 生成输出文件路径
            output_file = generate_temp_filename(video_file)
            
            # 构建FFmpeg命令
            ffmpeg_cmd = [
                'ffmpeg',
                '-i', video_file,
                '-vf', fancy_filter,
                '-c:a', 'copy',  # 保持音频不变
                '-y',
                output_file
            ]
            
            print(f"执行FFmpeg命令: {' '.join(ffmpeg_cmd)}")
            
            # 执行FFmpeg命令
            try:
                result = subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
                print("花式文本叠加成功")
                
                # 验证输出文件
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    # 替换原文件
                    os.remove(video_file)
                    os.rename(output_file, video_file)
                    print(f"花式文本叠加完成: {video_file}")
                else:
                    print(f"错误：花式文本叠加输出文件无效 {output_file}")
                    if os.path.exists(output_file):
                        os.remove(output_file)
                        
            except subprocess.CalledProcessError as e:
                stdout = e.stdout.decode('gbk', errors='ignore') if e.stdout else ""
                stderr = e.stderr.decode('gbk', errors='ignore') if e.stderr else ""
                print(f"FFmpeg花式文本叠加失败:")
                print(f"命令: {' '.join(ffmpeg_cmd)}")
                print(f"返回码: {e.returncode}")
                print(f"标准输出: {stdout}")
                print(f"错误输出: {stderr}")
                
                # 清理临时文件
                if os.path.exists(output_file):
                    os.remove(output_file)
                    
                print("花式文本叠加失败，继续处理视频...")
                
        except Exception as e:
            print(f"添加花式文本叠加时发生错误: {e}")
            print("继续处理视频...")

    def verify_video_file(self, video_file):
        """
        验证视频文件的完整性
        """
        if not os.path.exists(video_file):
            print(f"视频文件不存在: {video_file}")
            return False
        
        file_size = os.path.getsize(video_file)
        if file_size == 0:
            print(f"视频文件大小为0: {video_file}")
            return False
        
        # 使用ffprobe检查视频文件
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_file]
            result = subprocess.run(cmd, capture_output=True, check=True)
            
            if result.returncode == 0:
                print(f"视频文件验证成功: {video_file} ({file_size} bytes)")
                return True
            else:
                print(f"ffprobe验证失败: {video_file}")
                return False
        except subprocess.CalledProcessError as e:
            print(f"ffprobe验证视频文件时出错: {e}")
            print(f"stderr: {e.stderr.decode('gbk', errors='ignore') if e.stderr else ''}")
            return False
        except Exception as e:
            print(f"验证视频文件时发生未知错误: {e}")
            return False
