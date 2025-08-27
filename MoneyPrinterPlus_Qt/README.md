# MoneyPrinterPlus PyQt6版本

这是MoneyPrinterPlus的PyQt6桌面版本，提供现代化的图形界面来配置AI视频生成工具。

## 项目特性

- 🎨 **现代化UI**: 基于PyQt6的美观界面设计
- 🌍 **多语言支持**: 支持中文、英文界面切换
- ⚙️ **配置管理**: 简化的配置界面，支持多种服务提供商
- 💾 **自动保存**: 配置自动保存到YAML文件
- 🔧 **即插即用**: 无需复杂设置，开箱即用

## 第一阶段功能

当前版本实现了基础配置功能：

### ✅ 已完成功能

1. **界面语言配置**
   - 支持中文/英文界面切换
   - 配置自动保存和加载

2. **音频服务配置**
   - Azure语音服务配置
   - 阿里云语音服务配置  
   - 腾讯云语音服务配置
   - 提供商切换和参数配置

3. **LLM大模型配置**
   - 支持8个主流LLM提供商：
     - OpenAI
     - Moonshot (月之暗面)
     - Azure OpenAI
     - 百度千帆 (Qianfan)
     - 百川 (Baichuan)
     - 通义千问 (Tongyi)
     - DeepSeek
     - Ollama
   - 自动适配各提供商的配置参数

4. **配置持久化**
   - YAML格式配置文件
   - 自动保存修改
   - 与原项目配置兼容

## 安装和运行

### 环境要求

- Python 3.8+
- PyQt6

### 安装步骤

1. **进入PyQt6项目目录**
   ```bash
   cd MoneyPrinterPlus/MoneyPrinterPlus_Qt
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements_qt.txt
   ```
   
   或者手动安装：
   ```bash
   pip install PyQt6 PyYAML requests
   ```

3. **测试核心功能**
   ```bash
   # 使用父目录的虚拟环境
   ..\venv\Scripts\python.exe simple_test.py    # Windows
   ../venv/bin/python simple_test.py            # Linux/Mac
   ```
   
   如果看到所有 `[OK]` 标记，说明核心功能正常。

4. **运行应用**
   ```bash
   # 使用父目录的虚拟环境
   ..\venv\Scripts\python.exe main.py          # Windows
   ../venv/bin/python main.py                  # Linux/Mac
   
   # 或者从父目录使用启动脚本
   cd ..
   start_qt.bat        # Windows
   bash start_qt.sh    # Linux/Mac
   ```

### 打包为exe文件

安装PyInstaller：
```bash
pip install pyinstaller
```

打包为单个exe文件：
```bash
pyinstaller --onefile --windowed --name="MoneyPrinterPlus" main.py
```

生成的exe文件在 `dist/` 目录中。

## 项目结构

```
MoneyPrinterPlus_Qt/
├── main.py                 # 主入口文件
├── simple_test.py          # 核心功能测试
├── requirements_qt.txt     # 依赖列表
├── ui/                     # PyQt6界面模块
│   ├── main_window.py      # 主窗口
│   └── components/         # UI组件
│       ├── language_widget.py     # 语言选择组件
│       ├── audio_config_widget.py # 音频配置组件
│       └── llm_config_widget.py   # LLM配置组件
├── core/                   # 核心业务逻辑
│   ├── config_manager.py   # 配置管理器
│   └── translator.py       # 翻译管理器
├── resources/              # 资源文件
│   ├── locales/           # 翻译文件
│   └── styles/            # 样式文件
└── config/                # 配置文件目录（自动生成）
    ├── config.yml         # 主配置文件
    └── config.example.yml # 配置模板
```

## 使用说明

### 1. 语言设置
在界面顶部选择您偏好的界面语言（中文/English）。

### 2. 音频服务配置
选择音频服务提供商（Azure/阿里云/腾讯云），然后填入相应的API密钥和配置信息。

### 3. LLM模型配置
选择您要使用的LLM服务提供商，填入API密钥和模型名称等信息。

### 4. 配置自动保存
所有配置修改会自动保存到 `config/config.yml` 文件中。

## 开发说明

### 扩展功能
这是重构的第一阶段，后续可以继续添加：
- 视频生成界面
- 批量处理功能
- 发布管理功能
- 更多服务提供商

### 代码结构
- 采用MVC模式，界面和逻辑分离
- 配置管理采用单例模式
- 国际化支持，易于添加新语言
- 组件化设计，便于扩展

## 故障排除

### 1. PyQt6安装失败
如果PyQt6安装失败，可以尝试：
```bash
pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 配置文件问题
如果配置文件损坏，删除 `config/config.yml` 文件，程序会自动重新生成。

### 3. 界面显示异常
确保系统支持高DPI显示，程序已启用高DPI缩放支持。

### 4. 应用启动测试
可以使用测试脚本验证应用是否正常：
```bash
# 核心功能测试
python simple_test.py

# 启动测试（自动关闭）
python test_startup.py
```

## 更新日志

### v1.0.1 (最新)
- ✅ 修复递归错误和配置保存问题
- ✅ 添加延迟保存机制，避免频繁写入
- ✅ 优化语言切换逻辑，防止循环调用
- ✅ 改进配置管理，支持变更检测

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

遵循原项目的版权协议。