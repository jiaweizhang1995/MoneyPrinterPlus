# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MoneyPrinterPlus is a Python-based AI video generation and publishing tool that allows users to:
- Generate AI-powered short videos with text-to-speech and automatic subtitle generation
- Batch mix and merge videos using local resources
- Automatically publish videos to multiple platforms (抖音/Douyin, 快手/Kuaishou, 小红书/Xiaohongshu, 视频号/WeChat Channels, B站/Bilibili)

The application is built using Streamlit for the web interface and integrates with various AI services for content generation, voice synthesis, and video processing.

## Development Commands

### Setup and Installation
```bash
# Windows - Automatic setup (recommended for beginners)
setup.bat

# Mac/Linux - Automatic setup
bash setup.sh

# Manual installation
pip install -r requirements.txt
```

### Running the Application
```bash
# Windows - Automatic start
start.bat

# Mac/Linux - Automatic start  
bash start.sh

# Manual start
streamlit run gui.py
```

### Dependencies
- Python 3.10 or 3.11 required
- FFmpeg 6.1.1+ required (must be in PATH)
- Windows requires Visual C++ Redistributable

## Architecture Overview

### Core Structure
- **gui.py**: Main Streamlit application entry point and core video generation logic
- **main.py**: Command-line interface entry point
- **pages/**: Streamlit page modules for different features
- **services/**: Core business logic organized by domain
- **config/**: Configuration management
- **tools/**: Utility functions and helpers

### Key Service Domains
- **services/audio/**: Text-to-speech and speech recognition (Azure, Ali, Tencent, ChatTTS, GPT-SoVITS, CosyVoice)
- **services/llm/**: Large language model integrations (OpenAI, Azure, Kimi, Qianfan, Baichuan, Tongyi, DeepSeek, Ollama)
- **services/video/**: Video processing, merging, and generation
- **services/resource/**: External resource providers (Pexels, Pixabay, Stable Diffusion)
- **services/publisher/**: Platform-specific video publishing automation
- **services/captioning/**: Subtitle generation and processing

### Configuration System
- Uses YAML configuration files in `config/`
- `config.example.yml` provides template configuration
- Configuration is loaded and managed through `config/config.py`
- Supports various providers for each service type

### Video Generation Pipeline
1. **Content Generation**: LLM generates video script from topic/keywords
2. **Audio Processing**: Text-to-speech conversion with voice selection
3. **Resource Acquisition**: Fetch relevant video clips from external sources
4. **Video Assembly**: Combine audio, video clips, transitions, and effects
5. **Subtitle Generation**: Optional automated subtitle creation
6. **Final Output**: Produce finished video file

### Publishing Automation
Uses Selenium WebDriver to automate video uploads to social media platforms. Requires browser setup with debug mode enabled (Chrome port 9222 or Firefox port 2828).

## Key Features
- Multi-language support with internationalization
- 100+ voice options across different TTS providers
- 30+ video transition effects
- Local and cloud-based AI model support
- Batch video generation and mixing
- Automated social media publishing
- Multiple video resolutions and aspect ratios

## File Organization
- **work/**: Audio and video output directory
- **final/**: Final video output directory  
- **bgmusic/**: Background music files
- **fonts/**: Font files for subtitles
- **locales/**: Translation files for i18n
- **chattts/**, **fasterwhisper/**, **sensevoice/**: Local AI model directories