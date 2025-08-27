"""
视频使用次数追踪器 - PyQt6版本
基于原项目的video_usage_tracker.py
"""
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
            # 获取PyQt6项目的配置目录
            script_path = os.path.abspath(__file__)
            qt_project_root = os.path.dirname(os.path.dirname(script_path))
            config_dir = os.path.join(qt_project_root, "config")
        
        self.config_dir = config_dir
        self.max_usage = max_usage
        self.lock = threading.Lock()
        
        # 确保配置目录存在
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        self.usage_file = os.path.join(self.config_dir, "video_usage.json")
        
        # 加载现有使用记录
        self.usage_data = self._load_usage_data()
    
    def _load_usage_data(self) -> Dict[str, Dict]:
        """加载使用数据"""
        if not os.path.exists(self.usage_file):
            return {}
        
        try:
            with open(self.usage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载视频使用记录失败: {e}")
            return {}
    
    def _save_usage_data(self):
        """保存使用数据"""
        try:
            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(self.usage_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存视频使用记录失败: {e}")
    
    def record_usage(self, file_path: str) -> bool:
        """
        记录视频文件使用
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            bool: 是否可以使用（未超过最大使用次数）
        """
        with self.lock:
            # 规范化文件路径
            file_path = os.path.abspath(file_path)
            
            # 获取当前记录
            if file_path not in self.usage_data:
                self.usage_data[file_path] = {
                    'count': 0,
                    'first_used': None,
                    'last_used': None
                }
            
            record = self.usage_data[file_path]
            current_time = datetime.now().isoformat()
            
            # 检查是否超过最大使用次数
            if record['count'] >= self.max_usage:
                return False
            
            # 更新使用记录
            record['count'] += 1
            record['last_used'] = current_time
            if record['first_used'] is None:
                record['first_used'] = current_time
            
            # 保存数据
            self._save_usage_data()
            
            return True
    
    def is_available(self, file_path: str) -> bool:
        """
        检查视频文件是否可用
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            bool: 是否可用
        """
        file_path = os.path.abspath(file_path)
        
        if file_path not in self.usage_data:
            return True
        
        return self.usage_data[file_path]['count'] < self.max_usage
    
    def get_usage_count(self, file_path: str) -> int:
        """
        获取文件使用次数
        
        Args:
            file_path: 视频文件路径
            
        Returns:
            int: 使用次数
        """
        file_path = os.path.abspath(file_path)
        
        if file_path not in self.usage_data:
            return 0
        
        return self.usage_data[file_path]['count']
    
    def get_usage_statistics(self) -> Dict:
        """
        获取使用统计信息
        
        Returns:
            dict: 统计信息
        """
        with self.lock:
            total_files = len(self.usage_data)
            available_files = sum(1 for record in self.usage_data.values() 
                                if record['count'] < self.max_usage)
            exceeded_files = total_files - available_files
            
            # 使用次数分布
            usage_distribution = {}
            for record in self.usage_data.values():
                count = record['count']
                usage_distribution[count] = usage_distribution.get(count, 0) + 1
            
            return {
                'total_files': total_files,
                'available_files': available_files,
                'exceeded_files': exceeded_files,
                'max_usage': self.max_usage,
                'usage_distribution': usage_distribution
            }
    
    def get_detailed_records(self) -> List[Dict]:
        """
        获取详细记录
        
        Returns:
            list: 详细记录列表
        """
        records = []
        
        for file_path, record in self.usage_data.items():
            records.append({
                'file_path': file_path,
                'count': record['count'],
                'exceeded': record['count'] >= self.max_usage,
                'first_used': record.get('first_used'),
                'last_used': record.get('last_used')
            })
        
        # 按最后使用时间排序
        records.sort(key=lambda x: x['last_used'] or '', reverse=True)
        
        return records
    
    def reset_usage_records(self):
        """重置所有使用记录"""
        with self.lock:
            self.usage_data = {}
            self._save_usage_data()
    
    def reset_file_usage(self, file_path: str):
        """
        重置单个文件的使用记录
        
        Args:
            file_path: 视频文件路径
        """
        with self.lock:
            file_path = os.path.abspath(file_path)
            if file_path in self.usage_data:
                del self.usage_data[file_path]
                self._save_usage_data()
    
    def get_available_files(self, directory: str, extensions: List[str] = None) -> List[str]:
        """
        获取目录中可用的视频文件
        
        Args:
            directory: 目录路径
            extensions: 允许的文件扩展名列表，默认为常见视频格式
            
        Returns:
            list: 可用文件路径列表
        """
        if extensions is None:
            extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']
        
        available_files = []
        
        if not os.path.isdir(directory):
            return available_files
        
        try:
            for filename in os.listdir(directory):
                if any(filename.lower().endswith(ext) for ext in extensions):
                    file_path = os.path.join(directory, filename)
                    if self.is_available(file_path):
                        available_files.append(file_path)
        except Exception as e:
            print(f"扫描目录失败 {directory}: {e}")
        
        return available_files
    
    def export_records(self) -> Dict:
        """
        导出记录数据
        
        Returns:
            dict: 导出的数据
        """
        return {
            'export_time': datetime.now().isoformat(),
            'max_usage': self.max_usage,
            'statistics': self.get_usage_statistics(),
            'records': self.get_detailed_records()
        }


# 全局实例
_global_tracker = None
_tracker_lock = threading.Lock()


def get_video_usage_tracker() -> VideoUsageTracker:
    """
    获取全局视频使用追踪器实例
    
    Returns:
        VideoUsageTracker: 追踪器实例
    """
    global _global_tracker
    
    with _tracker_lock:
        if _global_tracker is None:
            _global_tracker = VideoUsageTracker()
        return _global_tracker