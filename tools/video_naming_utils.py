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
import glob
from datetime import datetime

def generate_video_filename(output_dir: str, prefix: str = "") -> str:
    """
    生成带日期和序号的视频文件名
    格式: YYYY-MM-DD_NN.mp4 或 prefix_YYYY-MM-DD_NN.mp4
    
    Args:
        output_dir: 输出目录路径
        prefix: 文件名前缀（可选）
    
    Returns:
        完整的文件路径
    """
    # 获取当前日期
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 构建搜索模式
    if prefix:
        pattern = os.path.join(output_dir, f"{prefix}_{today}_*.mp4")
        base_name = f"{prefix}_{today}"
    else:
        pattern = os.path.join(output_dir, f"{today}_*.mp4")
        base_name = today
    
    # 查找已存在的文件
    existing_files = glob.glob(pattern)
    
    # 提取序号并找到最大值
    max_number = 0
    for file_path in existing_files:
        filename = os.path.basename(file_path)
        # 移除扩展名
        name_without_ext = os.path.splitext(filename)[0]
        
        try:
            # 提取序号部分
            if prefix:
                # 格式: prefix_YYYY-MM-DD_NN
                parts = name_without_ext.split('_')
                if len(parts) >= 3:
                    number_str = parts[-1]  # 最后一部分是序号
                    number = int(number_str)
                    max_number = max(max_number, number)
            else:
                # 格式: YYYY-MM-DD_NN
                if '_' in name_without_ext:
                    number_str = name_without_ext.split('_')[-1]
                    number = int(number_str)
                    max_number = max(max_number, number)
        except (ValueError, IndexError):
            # 如果解析失败，跳过这个文件
            continue
    
    # 生成新的序号
    new_number = max_number + 1
    
    # 构建完整文件名
    filename = f"{base_name}_{new_number:02d}.mp4"
    full_path = os.path.join(output_dir, filename)
    
    return full_path

def generate_daily_video_filename(output_dir: str) -> str:
    """
    生成日期格式的视频文件名，格式: YYYY-MM-DD_NN.mp4
    
    Args:
        output_dir: 输出目录路径
    
    Returns:
        完整的文件路径
    """
    return generate_video_filename(output_dir)

def generate_prefixed_video_filename(output_dir: str, prefix: str) -> str:
    """
    生成带前缀的日期格式视频文件名，格式: prefix_YYYY-MM-DD_NN.mp4
    
    Args:
        output_dir: 输出目录路径
        prefix: 文件名前缀
    
    Returns:
        完整的文件路径
    """
    return generate_video_filename(output_dir, prefix)

def get_next_video_number(output_dir: str, date_str: str = None, prefix: str = "") -> int:
    """
    获取指定日期的下一个视频序号
    
    Args:
        output_dir: 输出目录路径
        date_str: 日期字符串，格式YYYY-MM-DD，默认为今天
        prefix: 文件名前缀（可选）
    
    Returns:
        下一个序号
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 构建搜索模式
    if prefix:
        pattern = os.path.join(output_dir, f"{prefix}_{date_str}_*.mp4")
    else:
        pattern = os.path.join(output_dir, f"{date_str}_*.mp4")
    
    # 查找已存在的文件
    existing_files = glob.glob(pattern)
    
    # 提取序号并找到最大值
    max_number = 0
    for file_path in existing_files:
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        try:
            # 提取序号部分
            if prefix:
                # 格式: prefix_YYYY-MM-DD_NN
                parts = name_without_ext.split('_')
                if len(parts) >= 3:
                    number_str = parts[-1]
                    number = int(number_str)
                    max_number = max(max_number, number)
            else:
                # 格式: YYYY-MM-DD_NN
                if '_' in name_without_ext:
                    number_str = name_without_ext.split('_')[-1]
                    number = int(number_str)
                    max_number = max(max_number, number)
        except (ValueError, IndexError):
            continue
    
    return max_number + 1

def list_videos_by_date(output_dir: str, date_str: str = None, prefix: str = "") -> list:
    """
    列出指定日期的所有视频文件
    
    Args:
        output_dir: 输出目录路径
        date_str: 日期字符串，格式YYYY-MM-DD，默认为今天
        prefix: 文件名前缀（可选）
    
    Returns:
        视频文件路径列表
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 构建搜索模式
    if prefix:
        pattern = os.path.join(output_dir, f"{prefix}_{date_str}_*.mp4")
    else:
        pattern = os.path.join(output_dir, f"{date_str}_*.mp4")
    
    # 查找文件并排序
    files = glob.glob(pattern)
    files.sort()
    
    return files