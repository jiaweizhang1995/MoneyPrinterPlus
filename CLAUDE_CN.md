# CLAUDE_CN.md

本文件为 Claude Code (claude.ai/code) 在处理此代码库时提供指导。

## 项目概述

MoneyPrinterPlus 是一个基于 Python 的 AI 视频生成和发布工具，允许用户：
- 生成具有文本转语音和自动字幕生成的 AI 驱动的短视频
- 使用本地资源批量混合和合并视频
- 自动将视频发布到多个平台（抖音/Douyin、快手/Kuaishou、小红书/Xiaohongshu、视频号/WeChat Channels、B站/Bilibili）

该应用程序使用 Streamlit 构建 Web 界面，并与各种 AI 服务集成，用于内容生成、语音合成和视频处理。

## 开发命令

### 设置和安装
```bash
# Windows - 自动设置（推荐新手使用）
setup.bat

# Mac/Linux - 自动设置
bash setup.sh

# 手动安装
pip install -r requirements.txt
```

### 运行应用程序
```bash
# Windows - 自动启动
start.bat

# Mac/Linux - 自动启动
bash start.sh

# 手动启动
streamlit run gui.py
```

### 依赖项
- 需要 Python 3.10 或 3.11
- 需要 FFmpeg 6.1.1+（必须在 PATH 中）
- Windows 需要 Visual C++ Redistributable

## 架构概览

### 核心结构
- **gui.py**: 主 Streamlit 应用程序入口点和核心视频生成逻辑
- **main.py**: 命令行界面入口点
- **pages/**: 不同功能的 Streamlit 页面模块
- **services/**: 按领域组织的核心业务逻辑
- **config/**: 配置管理
- **tools/**: 实用函数和辅助工具

### 关键服务领域
- **services/audio/**: 文本转语音和语音识别（Azure、阿里、腾讯、ChatTTS、GPT-SoVITS、CosyVoice）
- **services/llm/**: 大语言模型集成（OpenAI、Azure、Kimi、千帆、百川、通义、DeepSeek、Ollama）
- **services/video/**: 视频处理、合并和生成
- **services/resource/**: 外部资源提供商（Pexels、Pixabay、Stable Diffusion）
- **services/publisher/**: 平台特定的视频发布自动化
- **services/captioning/**: 字幕生成和处理

### 配置系统
- 使用 `config/` 中的 YAML 配置文件
- `config.example.yml` 提供模板配置
- 通过 `config/config.py` 加载和管理配置
- 支持每种服务类型的各种提供商

### 视频生成流程
1. **内容生成**: LLM 从主题/关键词生成视频脚本
2. **音频处理**: 文本转语音转换，支持语音选择
3. **资源获取**: 从外部源获取相关视频片段
4. **视频组装**: 组合音频、视频片段、转场和特效
5. **字幕生成**: 可选的自动字幕创建
6. **最终输出**: 生成完成的视频文件
test 

### 发布自动化
使用 Selenium WebDriver 自动化视频上传到社交媒体平台。需要启用调试模式的浏览器设置（Chrome 端口 9222 或 Firefox 端口 2828）。

## 关键功能
- 支持多语言国际化
- 100+ 跨不同 TTS 提供商的语音选项
- 30+ 视频转场特效
- 本地和云端 AI 模型支持
- 批量视频生成和混合
- 自动化社交媒体发布
- 多种视频分辨率和宽高比

## 文件组织
- **work/**: 音频和视频输出目录
- **final/**: 最终视频输出目录
- **bgmusic/**: 背景音乐文件
- **fonts/**: 字幕字体文件
- **locales/**: i18n 翻译文件
- **chattts/**, **fasterwhisper/**, **sensevoice/**: 本地 AI 模型目录
