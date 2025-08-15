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
- **final/**: Final video output directory with date-based naming (YYYY-MM-DD_NN.mp4)
- **bgmusic/**: Background music files
- **fonts/**: Font files for subtitles
- **locales/**: Translation files for i18n
- **chattts/**, **fasterwhisper/**, **sensevoice/**: Local AI model directories

## Testing and Development

### Video File Naming System
Videos are automatically named using date-based format:
- Regular videos: `2025-08-16_01.mp4`, `2025-08-16_02.mp4`
- Merge videos: `merge_2025-08-16_01.mp4`
- System auto-increments sequence numbers to prevent conflicts

### Testing Commands
```bash
# Test video naming functionality
python -c "from tools.video_naming_utils import *; print(generate_daily_video_filename('final'))"

# Test fancy text service
python -c "from services.video.fancy_text_service import FancyTextService; service=FancyTextService(); print('Service loaded:', service.config is not None)"

# Validate configuration
python -c "from config.config import my_config; print('Config loaded:', my_config is not None)"
```

## Advanced Features

### Fancy Text Overlays
- **Location**: `services/video/fancy_text_service.py`
- **Configuration**: `config/fancy_text_overlays.yml`
- **Functionality**: Automatic text overlays with brand names and product benefits
- **Styling**: Supports main title + subtitle with different fonts, colors, backgrounds
- **Integration**: Automatically applied during video generation via FFmpeg drawtext filters

### Complete Audio Mode
- Allows using pre-recorded MP3 files instead of TTS synthesis
- Located in `services/hunjian/hunjian_service.py`
- Automatically disables subtitle generation when enabled
- Supports random selection from audio directory

### Multi-Platform Publishing
- **Selenium-based automation**: Requires browser debug mode
- **Chrome**: Start with `--remote-debugging-port=9222`
- **Firefox**: Start with `-marionette -start-debugger-server 2828`
- **Platforms**: 抖音/Douyin, 快手/Kuaishou, 小红书/Xiaohongshu, 视频号/WeChat Channels, B站/Bilibili

## Code Architecture Details

### Service Layer Pattern
Each service domain is self-contained with:
- **Provider abstraction**: Support for multiple service providers (Azure, Ali, Tencent, etc.)
- **Configuration management**: YAML-based with runtime overrides
- **Error handling**: Comprehensive error handling with fallbacks
- **Session state integration**: Streamlit session state for UI consistency

### Video Processing Pipeline
1. **Content Generation**: LLM generates script from keywords
2. **Audio Processing**: TTS or complete audio mode with duration matching
3. **Video Matching**: Intelligent video selection to match audio duration
4. **Effects Application**: Transitions, text overlays, background music
5. **Subtitle Generation**: Optional automated subtitle creation (disabled in complete audio mode)
6. **Final Assembly**: FFmpeg-based video compilation with date-based naming

### Configuration System
- **Template**: `config.example.yml` provides all available options
- **Runtime**: Values merged from config files and Streamlit session state
- **Validation**: Service-specific validation with fallback defaults
- **Persistence**: Session state automatically saved to `config/session.yml`

### UI Architecture
- **Streamlit pages**: Modular page structure in `pages/` directory
- **Session management**: Persistent session state across page navigation
- **Multi-language support**: i18n via `locales/` with `tools/tr_utils.py`
- **Conditional rendering**: UI elements adapt based on feature flags and mode selection

## Key Implementation Patterns

### Error Handling Strategy
- Services implement graceful degradation
- FFmpeg operations include file validation
- Temporary file cleanup on failure
- User-friendly error messages in UI

### Resource Management
- Automatic temporary file cleanup
- Video file integrity verification
- Memory-efficient processing for large files
- Background process monitoring

### Extensibility Points
- Service provider interface allows easy addition of new TTS/LLM providers
- Video effect system supports custom FFmpeg filters
- Text overlay system configurable via YAML
- Publishing automation extensible to new platforms