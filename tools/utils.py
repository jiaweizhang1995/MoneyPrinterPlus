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

import os
import random
import subprocess
import time
import streamlit as st
from typing import Optional

from tools.file_utils import generate_temp_filename


def generate_operator():
    operators = ['+', '-']
    return random.choice(operators)


def random_with_system_time():
    system_time = int(time.time() * 1000)
    random_seed = (system_time + random.randint(0, 10000))
    return random_seed


def get_images_with_prefix(img_dir, img_file_prefix):
    # 确保提供的是绝对路径
    img_dir = os.path.abspath(img_dir)

    # 持有所有匹配前缀的图片文件的列表
    images_with_prefix = []

    # 遍历img_dir中的文件
    for filename in os.listdir(img_dir):
        # print('filename:', filename)
        # print('img_file_prefix:',img_file_prefix)
        # print(filename.startswith(img_file_prefix))
        # 检查文件名是否以img_file_prefix开头 并且后缀是.jpg
        if filename.startswith(img_file_prefix) and (filename.endswith('.png') or filename.endswith('.jpg')):
            # 构建完整的文件路径
            file_path = os.path.join(img_dir, filename)
            # 确保这是一个文件而不是目录
            if os.path.isfile(file_path):
                images_with_prefix.append(file_path)

    return images_with_prefix


def get_file_from_dir(file_dir, extension):
    extension_list = [ext.strip() for ext in extension.split(',')]
    # 确保提供的是绝对路径
    file_dir = os.path.abspath(file_dir)

    # 所有文件的列表
    file_list = []

    # 遍历file_dir中的文件
    for filename in os.listdir(file_dir):
        # print('filename:', filename)
        file_extension = os.path.splitext(filename)[1]
        # 检查文件名是否以img_file_prefix开头 并且后缀是.txt
        if file_extension in extension_list:
            # 构建完整的文件路径
            file_path = os.path.join(file_dir, filename)
            # 确保这是一个文件而不是目录
            if os.path.isfile(file_path):
                file_list.append(file_path)

    return file_list


def get_file_map_from_dir(file_dir, extension):
    extension_list = [ext.strip() for ext in extension.split(',')]
    # 确保提供的是绝对路径
    # 所有文件的列表
    file_map = {}
    if file_dir is not None and os.path.exists(file_dir):
        file_dir = os.path.abspath(file_dir)

        # 遍历file_dir中的文件
        for filename in os.listdir(file_dir):
            # print('filename:', filename)
            file_extension = os.path.splitext(filename)[1]
            # 检查文件名是否以img_file_prefix开头 并且后缀是.txt
            if file_extension in extension_list:
                # 构建完整的文件路径
                file_path = os.path.join(file_dir, filename)
                # 确保这是一个文件而不是目录
                if os.path.isfile(file_path):
                    file_map[file_path] = os.path.split(file_path)[1]

    return file_map


def get_text_from_dir(text_dir):
    return get_file_from_dir(text_dir, ".txt")


def get_mp4_from_dir(video_dir):
    return get_file_from_dir(video_dir, ".mp4")


def get_session_option(option: str) -> Optional[str]:
    return st.session_state.get(option)


def get_must_session_option(option: str, msg: str) -> Optional[str]:
    result = st.session_state.get(option)
    if not result:
        st.toast(msg, icon="⚠️")
        st.stop()
    return result


def must_have_value(option: str, msg: str) -> Optional[str]:
    if not option:
        st.toast(msg, icon="⚠️")
        st.stop()
    return option


def run_ffmpeg_command(command):
    try:
        result = subprocess.run(command, capture_output=True, check=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg returned an error: {result.stderr}")
        else:
            print("Command executed successfully.")
    except Exception as e:
        print(f"An error occurred while execute ffmpeg command {e}")


def extent_audio(audio_file, pad_dur=2):
    temp_file = generate_temp_filename(audio_file)
    # 构造ffmpeg命令
    command = [
        'ffmpeg',
        '-i', audio_file,
        '-af', f'apad=pad_dur={pad_dur}',
        temp_file
    ]
    # 执行命令
    subprocess.run(command, capture_output=True, check=True)
    # 重命名最终的文件
    if os.path.exists(temp_file):
        os.remove(audio_file)
        os.renames(temp_file, audio_file)


def trim_audio_to_duration(audio_file, target_duration, output_file=None):
    """
    将音频文件裁剪到指定时长
    :param audio_file: 输入音频文件路径
    :param target_duration: 目标时长（秒）
    :param output_file: 输出文件路径，如果为None则覆盖原文件
    :return: 输出文件路径
    """
    if output_file is None:
        output_file = generate_temp_filename(audio_file)
        overwrite_original = True
    else:
        overwrite_original = False
    
    # 构造ffmpeg命令
    command = [
        'ffmpeg',
        '-i', audio_file,
        '-t', str(target_duration),  # 截取到指定时长
        '-c', 'copy',  # 复制编码，不重新编码
        '-y',  # 覆盖输出文件
        output_file
    ]
    
    try:
        # 执行命令
        subprocess.run(command, capture_output=True, check=True)
        
        if overwrite_original:
            # 重命名最终的文件
            if os.path.exists(output_file):
                os.remove(audio_file)
                os.renames(output_file, audio_file)
            return audio_file
        else:
            return output_file
    except subprocess.CalledProcessError as e:
        print(f"音频裁剪失败: {e}")
        return None


def convert_mp3_to_wav(mp3_file, wav_file=None):
    """
    将MP3文件转换为WAV格式
    :param mp3_file: 输入MP3文件路径
    :param wav_file: 输出WAV文件路径，如果为None则自动生成
    :return: 输出WAV文件路径
    """
    if wav_file is None:
        # 生成输出文件名
        base_name = os.path.splitext(mp3_file)[0]
        wav_file = base_name + ".wav"
    
    # 构造ffmpeg命令
    command = [
        'ffmpeg',
        '-i', mp3_file,
        '-acodec', 'pcm_s16le',  # WAV格式编码
        '-ar', '16000',  # 采样率16kHz
        '-ac', '1',  # 单声道
        '-y',  # 覆盖输出文件
        wav_file
    ]
    
    try:
        # 执行命令
        subprocess.run(command, capture_output=True, check=True)
        return wav_file
    except subprocess.CalledProcessError as e:
        print(f"MP3转WAV失败: {e}")
        return None


def get_audio_files_from_dir(audio_dir, extensions=".mp3,.wav"):
    """
    从目录中获取音频文件列表
    :param audio_dir: 音频文件目录
    :param extensions: 支持的文件扩展名，用逗号分隔
    :return: 音频文件路径列表
    """
    extension_list = [ext.strip() for ext in extensions.split(',')]
    audio_files = []
    
    if audio_dir and os.path.exists(audio_dir):
        audio_dir = os.path.abspath(audio_dir)
        
        for filename in os.listdir(audio_dir):
            if any(filename.lower().endswith(ext) for ext in extension_list):
                audio_files.append(os.path.join(audio_dir, filename))
    
    return audio_files


def select_random_audio_file(audio_dir, extensions=".mp3,.wav"):
    """
    从目录中随机选择一个音频文件
    :param audio_dir: 音频文件目录
    :param extensions: 支持的文件扩展名
    :return: 随机选择的音频文件路径，如果没有文件则返回None
    """
    audio_files = get_audio_files_from_dir(audio_dir, extensions)
    
    if audio_files:
        return random.choice(audio_files)
    else:
        return None
