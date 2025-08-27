"""
翻译管理器 - 适配自原项目的 tr_utils.py
"""
import json
import os

class Translator:
    def __init__(self):
        self.current_language = 'zh-CN'
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """加载当前语言的翻译文件"""
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(script_dir, "resources", "locales", f'{self.current_language}.json')
        default_file_path = os.path.join(script_dir, "resources", "locales", 'zh-CN.json')
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.translations = json.load(file)
            else:
                # 加载默认中文翻译
                with open(default_file_path, 'r', encoding='utf-8') as file:
                    self.translations = json.load(file)
        except Exception as e:
            print(f"加载翻译文件失败: {e}")
            self.translations = {}
    
    def set_language(self, language):
        """设置当前语言"""
        if language != self.current_language:
            self.current_language = language
            self.load_translations()
    
    def tr(self, key):
        """获取翻译文本"""
        return self.translations.get(key, key)

# 全局翻译器实例
translator = Translator()

def tr(key):
    """便捷的翻译函数"""
    return translator.tr(key)

def set_language(language):
    """设置语言"""
    translator.set_language(language)