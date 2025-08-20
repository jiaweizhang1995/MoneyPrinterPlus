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


import json
import os
import threading
from datetime import datetime
from typing import Dict, List, Optional


class VideoUsageTracker:
    """
    视频使用次数追踪器
    用于记录和管理视频文件的使用次数，防止过度使用导致平台限流
    """
    
    def __init__(self, config_dir: str = None, max_usage: int = 3):
        """
        初始化视频使用追踪器
        
        Args:
            config_dir: 配置目录路径，默认为项目根目录下的config
            max_usage: 最大使用次数，默认为3次
        """
        if config_dir is None:
            # 获取项目根目录
            script_path = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(script_path))
            config_dir = os.path.join(project_root, "config")
        
        self.config_dir = config_dir
        self.max_usage = max_usage
        self.records_file = os.path.join(config_dir, "video_usage_records.json")
        self.lock = threading.Lock()
        
        # 确保配置目录存在
        os.makedirs(config_dir, exist_ok=True)
        
        # 加载现有记录
        self.usage_records = self._load_records()
    
    def _load_records(self) -> Dict[str, Dict]:
        """
        从文件加载使用记录
        
        Returns:
            使用记录字典，格式：{文件路径: {count: 使用次数, last_used: 最后使用时间}}
        """
        try:
            if os.path.exists(self.records_file):
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                    print(f"已加载视频使用记录：{len(records)} 个文件")
                    return records
        except Exception as e:
            print(f"加载视频使用记录失败：{e}")
        
        print("创建新的视频使用记录")
        return {}
    
    def _save_records(self):
        """
        保存使用记录到文件
        """
        try:
            with open(self.records_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_records, f, ensure_ascii=False, indent=2)
            print(f"已保存视频使用记录：{len(self.usage_records)} 个文件")
        except Exception as e:
            print(f"保存视频使用记录失败：{e}")
    
    def _normalize_path(self, file_path: str) -> str:
        """
        标准化文件路径，确保一致性
        
        Args:
            file_path: 原始文件路径
            
        Returns:
            标准化后的绝对路径
        """
        return os.path.abspath(file_path).replace('\\', '/')
    
    def get_usage_count(self, file_path: str) -> int:
        """
        获取指定文件的使用次数
        
        Args:
            file_path: 文件路径
            
        Returns:
            使用次数
        """
        normalized_path = self._normalize_path(file_path)
        return self.usage_records.get(normalized_path, {}).get('count', 0)
    
    def is_usage_exceeded(self, file_path: str) -> bool:
        """
        检查文件使用次数是否超过限制
        
        Args:
            file_path: 文件路径
            
        Returns:
            True表示超过限制，False表示未超过
        """
        return self.get_usage_count(file_path) >= self.max_usage
    
    def record_usage(self, file_path: str) -> bool:
        """
        记录文件使用
        
        Args:
            file_path: 文件路径
            
        Returns:
            True表示记录成功，False表示已超过使用限制
        """
        with self.lock:
            normalized_path = self._normalize_path(file_path)
            
            if self.is_usage_exceeded(file_path):
                print(f"视频文件使用次数已达上限：{file_path} (已使用{self.get_usage_count(file_path)}次)")
                return False
            
            # 更新使用记录
            if normalized_path not in self.usage_records:
                self.usage_records[normalized_path] = {'count': 0, 'last_used': None}
            
            self.usage_records[normalized_path]['count'] += 1
            self.usage_records[normalized_path]['last_used'] = datetime.now().isoformat()
            
            print(f"记录视频使用：{file_path} (第{self.usage_records[normalized_path]['count']}次)")
            
            # 保存到文件
            self._save_records()
            return True
    
    def filter_available_videos(self, video_files: List[str]) -> List[str]:
        """
        过滤出可用的视频文件（未超过使用限制的）
        
        Args:
            video_files: 候选视频文件列表
            
        Returns:
            可用的视频文件列表
        """
        available_files = []
        for video_file in video_files:
            if not self.is_usage_exceeded(video_file):
                available_files.append(video_file)
            else:
                print(f"跳过已达使用上限的视频：{video_file}")
        
        print(f"可用视频文件：{len(available_files)}/{len(video_files)}")
        return available_files
    
    def get_least_used_videos(self, video_files: List[str], count: int = None) -> List[str]:
        """
        获取使用次数最少的视频文件
        
        Args:
            video_files: 候选视频文件列表
            count: 返回的文件数量，None表示返回所有可用文件
            
        Returns:
            按使用次数排序的视频文件列表
        """
        # 先过滤出可用文件
        available_files = self.filter_available_videos(video_files)
        
        if not available_files:
            print("警告：没有可用的视频文件")
            return []
        
        # 按使用次数排序
        available_files.sort(key=lambda f: self.get_usage_count(f))
        
        if count is not None:
            available_files = available_files[:count]
        
        return available_files
    
    def reset_usage_records(self, file_paths: List[str] = None):
        """
        重置使用记录
        
        Args:
            file_paths: 要重置的文件路径列表，None表示重置所有记录
        """
        with self.lock:
            if file_paths is None:
                # 重置所有记录
                self.usage_records.clear()
                print("已重置所有视频使用记录")
            else:
                # 重置指定文件的记录
                reset_count = 0
                for file_path in file_paths:
                    normalized_path = self._normalize_path(file_path)
                    if normalized_path in self.usage_records:
                        del self.usage_records[normalized_path]
                        reset_count += 1
                print(f"已重置 {reset_count} 个视频文件的使用记录")
            
            # 保存到文件
            self._save_records()
    
    def get_usage_statistics(self) -> Dict:
        """
        获取使用统计信息
        
        Returns:
            统计信息字典
        """
        total_files = len(self.usage_records)
        exceeded_files = sum(1 for record in self.usage_records.values() 
                           if record['count'] >= self.max_usage)
        
        usage_distribution = {}
        for record in self.usage_records.values():
            count = record['count']
            usage_distribution[count] = usage_distribution.get(count, 0) + 1
        
        return {
            'total_files': total_files,
            'exceeded_files': exceeded_files,
            'available_files': total_files - exceeded_files,
            'max_usage': self.max_usage,
            'usage_distribution': usage_distribution
        }
    
    def get_detailed_records(self) -> List[Dict]:
        """
        获取详细的使用记录
        
        Returns:
            包含文件路径、使用次数、最后使用时间的记录列表
        """
        records = []
        for file_path, record in self.usage_records.items():
            records.append({
                'file_path': file_path,
                'count': record['count'],
                'last_used': record['last_used'],
                'exceeded': record['count'] >= self.max_usage
            })
        
        # 按使用次数倒序排列
        records.sort(key=lambda x: x['count'], reverse=True)
        return records


# 全局实例
_tracker_instance = None
_tracker_lock = threading.Lock()


def get_video_usage_tracker(config_dir: str = None, max_usage: int = None) -> VideoUsageTracker:
    """
    获取视频使用追踪器的全局实例
    
    Args:
        config_dir: 配置目录路径
        max_usage: 最大使用次数，None时从配置文件读取
        
    Returns:
        VideoUsageTracker实例
    """
    global _tracker_instance
    
    with _tracker_lock:
        if _tracker_instance is None:
            # 如果没有指定最大使用次数，尝试从配置文件读取
            if max_usage is None:
                try:
                    from config.config import video_usage_config
                    max_usage = video_usage_config.get('video_usage', {}).get('max_usage_count', 3)
                except ImportError:
                    print("无法导入视频使用配置，使用默认值3")
                    max_usage = 3
            
            _tracker_instance = VideoUsageTracker(config_dir, max_usage)
        return _tracker_instance


def reset_tracker_instance():
    """
    重置全局追踪器实例（主要用于测试）
    """
    global _tracker_instance
    with _tracker_lock:
        _tracker_instance = None