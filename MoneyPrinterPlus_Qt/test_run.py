"""
测试运行脚本
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 检查PyQt6是否安装
try:
    from PyQt6.QtWidgets import QApplication
    print("PyQt6已安装")
except ImportError:
    print("PyQt6未安装，请运行: pip install PyQt6")
    sys.exit(1)

# 测试配置管理器
try:
    from core.config_manager import config_manager
    print("配置管理器加载成功")
    print(f"当前配置: {config_manager.get_config()}")
except Exception as e:
    print(f"配置管理器加载失败: {e}")
    sys.exit(1)

# 测试翻译器
try:
    from core.translator import tr, set_language
    print("翻译器加载成功")
    print(f"测试翻译: {tr('Language')}")
except Exception as e:
    print(f"翻译器加载失败: {e}")
    sys.exit(1)

# 尝试启动主应用
try:
    from main import main
    print("准备启动应用...")
    main()
except Exception as e:
    print(f"应用启动失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)