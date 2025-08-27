# -*- coding: utf-8 -*-
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("开始测试核心功能...")

# 测试配置管理器
try:
    from core.config_manager import config_manager
    print("[OK] 配置管理器导入成功")
    
    config = config_manager.get_config()
    print(f"[OK] 获取配置成功: {len(config)} 个配置节")
    
    # 测试语言设置
    current_lang = config_manager.get_ui_language()
    print(f"[OK] 当前语言: {current_lang}")
    
    # 测试音频提供商
    audio_provider = config_manager.get_audio_provider()
    print(f"[OK] 当前音频提供商: {audio_provider}")
    
    # 测试LLM提供商
    llm_provider = config_manager.get_llm_provider()
    print(f"[OK] 当前LLM提供商: {llm_provider}")
    
except Exception as e:
    print(f"[ERROR] 配置管理器测试失败: {e}")

# 测试翻译器
try:
    from core.translator import tr, set_language
    print("[OK] 翻译器导入成功")
    
    set_language('zh-CN')
    chinese_text = tr('Language')
    print(f"[OK] 中文翻译: Language -> {chinese_text}")
    
    set_language('en')
    english_text = tr('Language')
    print(f"[OK] 英文翻译: Language -> {english_text}")
    
except Exception as e:
    print(f"[ERROR] 翻译器测试失败: {e}")

# 测试配置保存
try:
    from core.config_manager import config_manager
    
    # 保存原始值
    original_provider = config_manager.get_audio_provider()
    
    # 修改配置
    test_provider = 'Ali' if original_provider != 'Ali' else 'Azure'
    config_manager.set_audio_provider(test_provider)
    config_manager.save_config()
    print("[OK] 配置保存成功")
    
    # 验证保存
    if config_manager.get_audio_provider() == test_provider:
        print("[OK] 配置修改验证成功")
    
    # 恢复原始配置
    config_manager.set_audio_provider(original_provider)
    config_manager.save_config()
    print("[OK] 配置恢复成功")
    
except Exception as e:
    print(f"[ERROR] 配置保存测试失败: {e}")

print("\n核心功能测试完成！")
print("如果所有测试都显示 [OK]，说明核心功能正常")
print("接下来可以安装 PyQt6 并运行GUI界面")
print("\n安装命令: pip install PyQt6")
print("运行命令: python main.py")