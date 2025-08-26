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
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>视频处理</h2>", unsafe_allow_html=True)


def trim_video_with_ffmpeg(input_file, output_file, start_time, end_time):
    """
    使用FFmpeg剪辑视频
    """
    try:
        duration = end_time - start_time
        
        # 方法1：使用重新编码确保兼容性，移除音频
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-ss', str(start_time),
            '-t', str(duration),  # 使用持续时间
            '-c:v', 'libx264',    # 视频编码器
            '-an',                # 移除音频轨道
            '-preset', 'fast',     # 编码速度预设
            '-crf', '23',         # 质量控制
            '-pix_fmt', 'yuv420p', # 像素格式，确保兼容性
            '-movflags', '+faststart',  # 优化MP4播放
            output_file,
            '-y'  # 覆盖输出文件
        ]
        
        try:
            # 使用项目现有的FFmpeg执行函数
            run_ffmpeg_command(cmd)
            return True, tr("Video trimming completed successfully")
        except Exception as first_error:
            # 如果第一种方法失败，尝试复制流方法
            st.warning(tr("First method failed, trying alternative approach..."))
            
            cmd_copy = [
                'ffmpeg',
                '-ss', str(start_time),  # 在输入前指定开始时间，更快
                '-i', input_file,
                '-t', str(duration),
                '-c:v', 'copy',  # 复制视频流
                '-an',           # 移除音频
                '-avoid_negative_ts', 'make_zero',
                output_file + '.temp',
                '-y'
            ]
            
            run_ffmpeg_command(cmd_copy)
            
            # 如果复制成功，重新编码确保兼容性
            cmd_reencode = [
                'ffmpeg',
                '-i', output_file + '.temp',
                '-c:v', 'libx264',
                '-an',           # 移除音频
                '-pix_fmt', 'yuv420p',
                output_file,
                '-y'
            ]
            
            run_ffmpeg_command(cmd_reencode)
            
            # 删除临时文件
            try:
                os.unlink(output_file + '.temp')
            except:
                pass
                
            return True, tr("Video trimming completed successfully")
        
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
                with st.spinner(tr("Trimming video, please wait...")):
                    success, message = trim_video_with_ffmpeg(temp_input_path, output_path, start_time, end_time)
                
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