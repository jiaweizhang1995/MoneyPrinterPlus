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
import subprocess

import streamlit as st

from tools.file_utils import random_line_from_text_file
from tools.utils import get_must_session_option, random_with_system_time, extent_audio, run_ffmpeg_command, select_random_audio_file, convert_mp3_to_wav, trim_audio_to_duration

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# print("当前脚本的绝对路径是:", script_path)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)
# 音频输出目录
audio_output_dir = os.path.join(script_dir, "../../work")
audio_output_dir = os.path.abspath(audio_output_dir)


def get_session_video_scene_text():
    video_dir_list = []
    video_text_list = []
    if 'scene_number' not in st.session_state:
        st.session_state['scene_number'] = 0
    for i in range(int(st.session_state.get('scene_number'))+1):
        print("select video scene " + str(i + 1))
        if "video_scene_folder_" + str(i + 1) in st.session_state and st.session_state["video_scene_folder_" + str(i + 1)] is not None:
            video_dir_list.append(st.session_state["video_scene_folder_" + str(i + 1)])
            video_text_list.append(st.session_state["video_scene_text_" + str(i + 1)])
    return video_dir_list, video_text_list


def get_video_scene_text_list(video_text_list):
    video_scene_text_list = []
    for video_text in video_text_list:
        if video_text is not None and video_text != "":
            video_line = random_line_from_text_file(video_text)
            video_scene_text_list.append(video_line)
        else:
            video_scene_text_list.append("")
    return video_scene_text_list


def get_video_text_from_list(video_scene_text_list):
    return " ".join(video_scene_text_list)


def get_audio_and_video_list(audio_service, audio_rate):
    audio_output_file_list = []
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    audio_voice = get_must_session_option("audio_voice", "请先设置配音语音")
    i = 0
    for video_scene_text in video_scene_text_list:
        if video_scene_text is not None and video_scene_text != "":
            temp_file_name = str(random_with_system_time()) + str(i)
            i = i + 1
            audio_output_file = os.path.join(audio_output_dir, str(temp_file_name) + ".wav")
            audio_service.save_with_ssml(video_scene_text,
                                         audio_output_file,
                                         audio_voice,
                                         audio_rate)
            extent_audio(audio_output_file, 1)
            audio_output_file_list.append(audio_output_file)
        else:
            st.toast("配音文字不能为空", icon="⚠️")
            st.stop()

    return audio_output_file_list, video_dir_list


def get_audio_and_video_list_local(audio_service):
    audio_output_file_list = []
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    i = 0
    for video_scene_text in video_scene_text_list:
        temp_file_name = str(random_with_system_time()) + str(i)
        i = i + 1
        audio_output_file = os.path.join(audio_output_dir, str(temp_file_name) + ".wav")
        audio_service.chat_with_content(video_scene_text, audio_output_file)
        extent_audio(audio_output_file, 1)
        audio_output_file_list.append(audio_output_file)
    return audio_output_file_list, video_dir_list


def get_video_text():
    video_dir_list, video_text_list = get_session_video_scene_text()
    video_scene_text_list = get_video_scene_text_list(video_text_list)
    return get_video_text_from_list(video_scene_text_list)


def concat_audio_list(audio_output_file_list):
    temp_output_file_name = os.path.join(audio_output_dir, str(random_with_system_time()) + ".wav")
    concat_audio_file = os.path.join(audio_output_dir, "concat_audio_file.txt")
    with open(concat_audio_file, 'w', encoding='utf-8') as f:
        for audio_file in audio_output_file_list:
            f.write("file '{}'\n".format(os.path.abspath(audio_file)))
    # 调用ffmpeg来合并音频
    # 注意：这里假设ffmpeg在你的PATH中，否则你需要提供ffmpeg的完整路径
    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', concat_audio_file,
        '-c', 'copy',  # 如果可能，直接复制流而不是重新编码
        temp_output_file_name
    ]
    run_ffmpeg_command(command)
    # 完成后，删除临时文件（如果你不再需要它）
    os.remove(concat_audio_file)
    print(f"Audio files have been merged into {temp_output_file_name}")
    return temp_output_file_name


def get_session_video_scene_dirs():
    """
    获取会话中配置的视频场景目录列表
    :return: 视频目录列表
    """
    video_dir_list = []
    if 'scene_number' not in st.session_state:
        st.session_state['scene_number'] = 0
    for i in range(int(st.session_state.get('scene_number'))+1):
        print("select video scene " + str(i + 1))
        if "video_scene_folder_" + str(i + 1) in st.session_state and st.session_state["video_scene_folder_" + str(i + 1)] is not None:
            video_dir_list.append(st.session_state["video_scene_folder_" + str(i + 1)])
    return video_dir_list


def get_audio_and_video_list_from_mp3():
    """
    完整音频模式：从MP3目录随机选择音频文件并处理为与视频匹配的音频列表
    新的处理逻辑：不分割音频，直接使用完整音频匹配所有视频场景
    :return: 音频文件列表, 视频目录列表
    """
    from services.video.video_service import get_audio_duration
    
    # 获取完整音频目录
    full_audio_dir = get_must_session_option("full_audio_dir", "请先设置音频文件目录")
    
    # 获取视频场景目录列表
    video_dir_list = get_session_video_scene_dirs()
    
    if not video_dir_list:
        st.toast("请先配置视频场景资源目录", icon="⚠️")
        st.stop()
    
    # 随机选择一个MP3文件
    selected_mp3 = select_random_audio_file(full_audio_dir, ".mp3,.wav")
    if not selected_mp3:
        st.toast("在指定目录中未找到音频文件", icon="⚠️")
        st.stop()
    
    print(f"选择的音频文件: {selected_mp3}")
    
    # 转换为WAV格式（如果是MP3）
    if selected_mp3.lower().endswith('.mp3'):
        # 生成临时WAV文件路径
        temp_file_name = str(random_with_system_time())
        converted_wav = os.path.join(audio_output_dir, f"{temp_file_name}_converted.wav")
        converted_wav = convert_mp3_to_wav(selected_mp3, converted_wav)
        if not converted_wav:
            st.toast("音频格式转换失败", icon="⚠️")
            st.stop()
        working_audio = converted_wav
    else:
        working_audio = selected_mp3
    
    # 获取音频总时长
    total_audio_duration = get_audio_duration(working_audio)
    if not total_audio_duration:
        st.toast("无法获取音频时长", icon="⚠️")
        st.stop()
    
    print(f"音频总时长: {total_audio_duration}秒")
    print("完整音频模式：不分割音频，直接使用完整音频")
    
    # 保存完整音频信息到session_state
    st.session_state["full_audio_original_file"] = working_audio
    st.session_state["full_audio_mode"] = True  # 标记为完整音频模式
    st.session_state["full_audio_duration"] = total_audio_duration
    
    # 返回完整音频文件（作为单个元素的列表）和视频目录列表
    # 这样可以保持与原有接口的兼容性
    return [working_audio], video_dir_list


def cleanup_full_audio_temp_files():
    """
    清理完整音频模式下生成的临时文件
    """
    # 清理原始转换的音频文件（如果是从MP3转换而来）
    full_audio_original = st.session_state.get("full_audio_original_file")
    if full_audio_original and os.path.exists(full_audio_original):
        # 检查是否是临时转换文件（包含converted字样）
        if "_converted.wav" in full_audio_original:
            os.remove(full_audio_original)
            print(f"清理临时音频文件: {full_audio_original}")
    
    # 清理session_state中的临时变量
    for key in ["full_audio_original_file", "full_audio_mode", "full_audio_duration"]:
        if key in st.session_state:
            del st.session_state[key]
