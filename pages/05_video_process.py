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
import subprocess
import tempfile
import random
import time
from pathlib import Path
import streamlit as st

from config.config import app_title, save_session_state_to_yaml, load_session_state_from_yaml
from pages.common import common_ui
from tools.tr_utils import tr
from tools.utils import run_ffmpeg_command

load_session_state_from_yaml('05_first_visit')

common_ui()

st.markdown(f"<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            {app_title}</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>去重处理</h2>", unsafe_allow_html=True)


def generate_deduplication_params():
    """
    生成TikTok去重处理的随机参数
    """
    # 使用当前时间戳作为种子确保每次都不同
    random.seed(int(time.time() * 1000) % 10000)
    
    params = {
        # 放大倍数 (5%-15%随机放大)
        'zoom_factor': round(random.uniform(1.05, 1.15), 3),
        
        # 镜像翻转概率 (50%概率)
        'apply_flip': random.choice([True, False]),
        
        # 裁切偏移 (-5%到+5%随机偏移)
        'crop_offset_x': round(random.uniform(-0.05, 0.05), 3),
        'crop_offset_y': round(random.uniform(-0.05, 0.05), 3),
        
        # 像素噪声强度
        'noise_strength': random.randint(1, 3),
        
        # 时间戳随机偏移 (毫秒)
        'timestamp_offset': random.randint(1, 100)
    }
    
    return params


def apply_tiktok_deduplication_filter(zoom_factor, apply_flip, crop_offset_x, crop_offset_y, 
                                    noise_strength, timestamp_offset):
    """
    生成TikTok去重处理的FFmpeg滤镜链 - 简化版本
    """
    filters = []
    
    # 1. 镜像翻转 (如果启用) - 最简单的去重方式
    if apply_flip:
        filters.append("hflip")
    
    # 2. 轻微放大+裁切 (保持视频流畅)
    filters.append(f"scale=iw*{zoom_factor}:ih*{zoom_factor}")
    filters.append("crop=iw*0.95:ih*0.95:(iw-ow)/2:(ih-oh)/2")
    
    # 3. 轻微亮度调整改变MD5
    brightness_adj = 0.02 + (noise_strength * 0.01)  # 2%-5%亮度调整
    filters.append(f"eq=brightness={brightness_adj}")
    
    return ",".join(filters)


def trim_video_with_ffmpeg(input_file, output_file, start_time, end_time, enable_deduplication=True):
    """
    使用FFmpeg剪辑视频，支持TikTok去重处理
    """
    try:
        duration = end_time - start_time
        
        # 构建基础FFmpeg命令
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-ss', str(start_time),
            '-t', str(duration),
            '-c:v', 'libx264',
            '-an',  # 移除音频轨道
            '-preset', 'fast',
            '-crf', '23',
            '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart'
        ]
        
        # 如果启用去重处理，添加滤镜
        if enable_deduplication:
            # 生成随机去重参数
            dedup_params = generate_deduplication_params()
            
            # 显示去重处理信息
            flip_text = tr("Yes") if dedup_params['apply_flip'] else tr("No")
            st.info(f"""
            {tr("Applying TikTok deduplication")}:
            - {tr("Zoom factor")}: {dedup_params['zoom_factor']}x
            - {tr("Mirror flip")}: {flip_text}
            - {tr("Crop offset")}: X{dedup_params['crop_offset_x']:.2f}, Y{dedup_params['crop_offset_y']:.2f}
            """)
            
            # 生成去重滤镜链
            dedup_filter = apply_tiktok_deduplication_filter(
                dedup_params['zoom_factor'],
                dedup_params['apply_flip'],
                dedup_params['crop_offset_x'],
                dedup_params['crop_offset_y'],
                dedup_params['noise_strength'],
                dedup_params['timestamp_offset']
            )
            
            # 添加滤镜到命令
            cmd.extend(['-vf', dedup_filter])
        
        # 添加输出文件和覆盖选项
        cmd.extend([output_file, '-y'])
        
        try:
            # 执行FFmpeg命令
            run_ffmpeg_command(cmd)
            
            success_msg = tr("Video trimming completed successfully")
            if enable_deduplication:
                success_msg += " " + tr("with anti-detection processing")
            
            return True, success_msg
            
        except Exception as first_error:
            # 如果第一种方法失败，尝试不使用去重的简单方法
            st.warning(tr("Deduplication failed, trying without anti-detection..."))
            
            cmd_simple = [
                'ffmpeg',
                '-ss', str(start_time),
                '-i', input_file,
                '-t', str(duration),
                '-c:v', 'libx264',
                '-an',
                '-preset', 'fast',
                '-crf', '23',
                '-pix_fmt', 'yuv420p',
                output_file,
                '-y'
            ]
            
            run_ffmpeg_command(cmd_simple)
            return True, tr("Video trimming completed successfully") + " " + tr("(without anti-detection)")
        
    except Exception as e:
        return False, f"{tr('Processing error')}: {str(e)}"


# 创建主要的UI组件
st.subheader(tr("Select Video File"))

# 文件选择
uploaded_file = st.file_uploader(
    tr("Select Video File"), 
    type=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'],
    help=tr("Supported formats: mp4, avi, mov, mkv, flv, wmv")
)

if uploaded_file is not None:
    # 显示文件信息
    st.info(f"{tr('Selected file')}: {uploaded_file.name}")
    
    # 时间设置
    st.subheader(tr("Set Trimming Time Range"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_time = st.number_input(
            tr("Start Time (seconds)"), 
            min_value=0.0, 
            value=0.0, 
            step=0.1,
            format="%.1f",
            key="start_time"
        )
    
    with col2:
        end_time = st.number_input(
            tr("End Time (seconds)"), 
            min_value=0.1, 
            value=10.0, 
            step=0.1,
            format="%.1f",
            key="end_time"
        )
    
    # 输出设置
    st.subheader(tr("Output Settings"))
    
    # 默认输出目录
    default_output_dir = os.path.join(os.getcwd(), "final")
    
    output_dir = st.text_input(
        tr("Output Directory Path"), 
        value=default_output_dir,
        help=tr("Generated videos will be saved to this directory"),
        key="output_dir"
    )
    
    # 输出文件名
    base_name = os.path.splitext(uploaded_file.name)[0]
    default_output_name = f"trimmed_{base_name}.mp4"
    
    output_filename = st.text_input(
        tr("Output Filename"),
        value=default_output_name,
        help=tr("Name of the output file (including extension)"),
        key="output_filename"
    )
    
    # TikTok去重处理选项
    st.subheader(tr("Anti-Detection Settings"))
    
    enable_deduplication = st.checkbox(
        tr("Enable TikTok Deduplication"),
        value=True,
        help=tr("Apply anti-detection processing to avoid content detection"),
        key="enable_deduplication"
    )
    
    if enable_deduplication:
        st.info(tr("Video will be processed with mirror flip, zoom crop, and noise to avoid detection"))
    
    # 验证时间设置
    if start_time >= end_time:
        st.error(tr("Start time must be less than end time"))
    else:
        # 处理按钮
        if st.button(tr("Start Video Trimming"), type="primary"):
            # 保存会话状态
            save_session_state_to_yaml()
            
            # 确保输出目录存在
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # 创建临时输入文件
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                temp_file.write(uploaded_file.getbuffer())
                temp_input_path = temp_file.name
            
            # 生成输出文件路径
            output_path = os.path.join(output_dir, output_filename)
            
            try:
                # 显示处理进度
                progress_text = tr("Trimming video, please wait...")
                if enable_deduplication:
                    progress_text += " " + tr("(with anti-detection processing)")
                
                with st.spinner(progress_text):
                    success, message = trim_video_with_ffmpeg(temp_input_path, output_path, start_time, end_time, enable_deduplication)
                
                # 显示结果
                if success:
                    st.success(f"✅ {message}")
                    st.info(f"{tr('Output file saved to')}: {output_path}")
                    
                    # 显示文件信息
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        file_size_mb = file_size / (1024 * 1024)
                        st.success(f"{tr('File size')}: {file_size_mb:.2f} MB")
                        
                        # 提供下载链接
                        with open(output_path, "rb") as file:
                            st.download_button(
                                label=tr("Download Processed Video"),
                                data=file,
                                file_name=output_filename,
                                mime="video/mp4"
                            )
                else:
                    st.error(f"❌ {message}")
            
            finally:
                # 清理临时文件
                try:
                    os.unlink(temp_input_path)
                except:
                    pass

# 使用说明
with st.expander(tr("Usage Instructions")):
    st.markdown(f"""
    ### {tr("Video Processing Feature Description")}
    
    1. **{tr("Select Video File")}**: {tr("Click the Select Video File button to upload the video to be processed")}
    
    2. **{tr("Set Time Range")}**: 
       - {tr("Start Time")}: {tr("Starting time point for trimming (seconds)")}
       - {tr("End Time")}: {tr("Ending time point for trimming (seconds)")}
       
    3. **{tr("Output Settings")}**:
       - {tr("Output Directory")}: {tr("Location where generated videos will be saved")}
       - {tr("Output Filename")}: {tr("Name of the generated file")}
    
    4. **{tr("Start Processing")}**: {tr("Click the Start Video Trimming button to begin processing")}
    
    ### {tr("Notes")}
    - {tr("Ensure FFmpeg is properly installed and added to system PATH")}
    - {tr("Supported video formats: mp4, avi, mov, mkv, flv, wmv")}
    - {tr("Processing time depends on video size and duration")}
    - {tr("Generated videos will be saved to the specified output directory")}
    """)