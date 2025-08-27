"""
测试配置管理器
"""
import sys
import os

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_config_manager():
    """测试配置管理器"""
    print("=== 测试配置管理器 ===")
    
    try:
        from core.config_manager import config_manager, LANGUAGES, AUDIO_PROVIDERS, LLM_PROVIDERS
        print("+ 配置管理器导入成功")
        
        # 测试获取配置
        config = config_manager.get_config()
        print(f"✓ 获取配置成功: {len(config)} 个配置节")
        
        # 测试语言设置
        current_lang = config_manager.get_ui_language()
        print(f"✓ 当前语言: {current_lang}")
        
        # 测试设置语言
        config_manager.set_ui_language('en')
        new_lang = config_manager.get_ui_language()
        print(f"✓ 设置语言成功: {new_lang}")
        
        # 恢复原语言
        config_manager.set_ui_language(current_lang)
        
        # 测试音频提供商
        audio_provider = config_manager.get_audio_provider()
        print(f"✓ 当前音频提供商: {audio_provider}")
        
        # 测试LLM提供商
        llm_provider = config_manager.get_llm_provider()
        print(f"✓ 当前LLM提供商: {llm_provider}")
        
        # 测试配置更新
        config_manager.update_nested_config('audio', 'Azure', 'speech_key', 'test_key')
        azure_config = config_manager.get_audio_config('Azure')
        print(f"✓ 配置更新成功: Azure配置包含 {len(azure_config)} 项")
        
        print("✓ 配置管理器测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ 配置管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_translator():
    """测试翻译器"""
    print("\n=== 测试翻译器 ===")
    
    try:
        from core.translator import tr, set_language, translator
        print("✓ 翻译器导入成功")
        
        # 测试中文翻译
        set_language('zh-CN')
        chinese_text = tr('Language')
        print(f"✓ 中文翻译: Language -> {chinese_text}")
        
        # 测试英文翻译
        set_language('en')
        english_text = tr('Language')
        print(f"✓ 英文翻译: Language -> {english_text}")
        
        # 测试不存在的key
        unknown_text = tr('NonExistentKey')
        print(f"✓ 未知键处理: NonExistentKey -> {unknown_text}")
        
        print("✓ 翻译器测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ 翻译器测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_persistence():
    """测试配置持久化"""
    print("\n=== 测试配置持久化 ===")
    
    try:
        from core.config_manager import config_manager
        
        # 保存原始值
        original_provider = config_manager.get_audio_provider()
        
        # 修改配置
        test_provider = 'Ali' if original_provider != 'Ali' else 'Azure'
        config_manager.set_audio_provider(test_provider)
        
        # 保存配置
        config_manager.save_config()
        print("✓ 配置保存成功")
        
        # 创建新的配置管理器实例来测试加载
        from core.config_manager import ConfigManager
        new_manager = ConfigManager()
        loaded_provider = new_manager.get_audio_provider()
        
        if loaded_provider == test_provider:
            print("✓ 配置加载成功")
        else:
            print(f"✗ 配置加载失败: 期望 {test_provider}, 实际 {loaded_provider}")
            return False
        
        # 恢复原始配置
        config_manager.set_audio_provider(original_provider)
        config_manager.save_config()
        
        print("✓ 配置持久化测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ 配置持久化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("开始测试 MoneyPrinterPlus Qt 核心功能...")
    
    results = []
    results.append(test_config_manager())
    results.append(test_translator())
    results.append(test_config_persistence())
    
    print(f"\n=== 测试总结 ===")
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ 全部测试通过! ({passed}/{total})")
        print("\n核心功能正常，可以尝试安装PyQt6并运行GUI界面")
        return True
    else:
        print(f"✗ 部分测试失败: {passed}/{total}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)