# 视频混剪功能详细文档

本文档详细介绍 MoneyPrinterPlus 中的视频混剪功能和逻辑。

## 功能概述

视频混剪区（02_mix_video.py）是 MoneyPrinterPlus 的核心功能之一，它允许用户通过以下方式创建高质量的混剪视频：

- 从本地素材文件夹中智能选择和组合视频片段
- 为每个场景配置不同的文本内容进行配音
- 自动匹配音频时长与视频长度
- 支持多种音频源（远程TTS、本地TTS、音频识别）
- 添加背景音乐、字幕和过渡效果
- 支持多种视频格式和布局

## 界面结构和组件

### 1. 场景配置区域 (Mix Video Scene)

**位置**: `mix_video_container` 容器
**功能**: 允许用户配置多个视频场景（最多5个）

#### 核心组件:
- **视频素材路径**: 每个场景的视频资源文件夹路径
  - 支持的文件格式: `.jpg`, `.jpeg`, `.png`, `.mp4`, `.mov`
  - 系统会从指定文件夹中随机选择素材
- **场景文本**: 对应场景的文本内容路径
  - 要求: UTF-8编码，每行对应一个场景
  - 用于生成该场景的配音

#### 场景管理功能:
```python
def add_more_scene_for_mix(video_scene_container):
    # 最多支持5个场景
    if st.session_state['scene_number'] < 4:
        st.session_state['scene_number'] = st.session_state['scene_number'] + 1
    else:
        st.toast(tr("Maximum number of scenes reached"), icon="⚠️")

def delete_scene_for_mix(video_scene_container):
    # 删除场景，最少保留1个
    if st.session_state['scene_number'] >= 1:
        st.session_state['scene_number'] = st.session_state['scene_number'] - 1
```

### 2. 配音配置区域 (Video Captioning)

**位置**: `captioning_container` 容器
**功能**: 配置音频生成和语音合成

#### 音频类型选择:
- **远程TTS** (`remote`): 使用云端语音合成服务
- **本地TTS** (`local`): 使用本地部署的语音合成模型

#### 远程TTS配置:
- **音频语言**: 支持多种语言选择
- **音频声音**: 根据选择的语言显示可用声音
- **音频速度**: normal, fast, faster, fastest, slow, slower, slowest
- **音频测试**: 实时测试当前配置的音频效果

#### 本地TTS配置选项:

##### ChatTTS配置:
```python
# 文本优化参数
refine_text: bool  # 是否启用文本优化
refine_text_prompt: str  # 优化提示词，如 "[oral_2][laugh_0][break_6]"

# 生成参数
text_seed: int  # 文本种子值 (1-4294967295)
audio_temperature: float  # 音频温度 (0.01-1.0)
audio_top_p: float  # Top-P 采样 (0.1-0.9)
audio_top_k: int  # Top-K 采样 (1-20)

# 声音配置
use_random_voice: bool  # 是否使用随机声音
audio_seed: int  # 音频种子（随机声音时使用）
default_chattts_dir: str  # 本地ChatTTS模型目录
audio_voice: str  # 选择的声音文件 (.pt/.txt)
```

##### GPT-SoVITS配置:
```python
# 参考音频配置
use_reference_audio: bool  # 是否使用参考音频
reference_audio: file  # 参考音频文件 (.wav/.mp3)
reference_audio_text: str  # 参考音频对应文本
reference_audio_language: str  # 参考音频语言

# 推理参数
audio_temperature: float  # 音频温度
audio_top_p: float  # Top-P 采样
audio_top_k: int  # Top-K 采样
inference_audio_language: str  # 推理语言
```

##### CosyVoice配置:
```python
# 参考音频配置
use_reference_audio: bool  # 是否使用参考音频
reference_audio_file_path: str  # 参考音频文件路径
reference_audio_text: str  # 参考音频文本
reference_audio_language: str  # 参考音频语言（预设声音时使用）

# 生成参数
text_seed: int  # 文本种子值
audio_speed: str  # 音频速度
```

### 3. 音频识别区域 (Audio Recognition)

**位置**: `recognition_container` 容器
**功能**: 配置音频识别类型（远程/本地）

### 4. 背景音乐配置 (Video Background Music)

**位置**: `bg_music_container` 容器
**功能**: 为生成的视频添加背景音乐

#### 配置选项:
- **背景音乐目录**: 指定背景音乐文件夹路径
- **启用背景音乐**: 开关控制
- **背景音乐选择**: 从指定目录中选择音乐文件 (`.mp3`, `.wav`)
- **背景音乐音量**: 0.0-1.0 范围调节

### 5. 视频配置区域 (Video Config)

**位置**: `video_container` 容器
**功能**: 设置视频输出参数

#### 核心配置:
```python
# 视频布局和尺寸
video_layout: str  # "portrait"(竖屏), "landscape"(横屏), "square"(方形)
video_fps: int  # 帧率: 20, 25, 30
video_size: str  # 分辨率，根据布局动态调整:
    # 竖屏: 1080x1920, 720x1280, 480x960, 360x720, 240x480
    # 横屏: 1920x1080, 1280x720, 960x480, 720x360, 480x240
    # 方形: 1080x1080, 720x720, 480x480, 360x360, 240x240

# 视频片段设置
video_segment_min_length: int  # 最小片段长度 (5-10秒)
video_segment_max_length: int  # 最大片段长度 (5-30秒)

# 转场效果
enable_video_transition_effect: bool  # 启用转场效果
video_transition_effect_type: str  # 转场类型
video_transition_effect_value: str  # 转场效果值
video_transition_effect_duration: str  # 转场持续时间 ("1", "2")
```

### 6. 字幕配置区域 (Video Subtitles)

**位置**: `subtitle_container` 容器
**功能**: 配置视频字幕样式和位置

#### 字幕设置:
```python
# 基本设置
enable_subtitles: bool  # 启用字幕
subtitle_font: str  # 字体选择（多种中文字体）
subtitle_font_size: int  # 字体大小 (4-24)
captioning_lines: int  # 字幕行数 (1-2)

# 位置和样式
subtitle_position: int  # 字幕位置:
    # 5: 左上, 6: 上中, 7: 右上
    # 9: 左中, 10: 中心, 11: 右中  
    # 1: 左下, 2: 下中, 3: 右下
subtitle_color: str  # 字幕颜色 (颜色选择器)
subtitle_border_color: str  # 字幕边框颜色
subtitle_border_width: int  # 字幕边框宽度 (0-4)
```

### 7. 视频生成区域 (Generate Video)

**位置**: `video_generator` 容器
**功能**: 执行视频生成任务

#### 生成设置:
- **视频数量**: 1-100个视频批量生成
- **生成按钮**: 触发视频生成流程

## 核心处理逻辑

### 1. 视频生成主流程

**入口函数**: `main_generate_ai_video_for_mix(video_generator)`

**流程步骤**:
```python
def main_generate_ai_video_for_mix(video_generator):
    with video_generator:
        # 1. 生成配音文件
        st.write(tr("Generate Video Dubbing..."))
        main_generate_video_dubbing_for_mix()
        
        # 2. 视频素材标准化
        st.write(tr("Video normalize..."))
        video_dir_list = get_must_session_option("video_dir_list", "请选择视频目录路径")
        audio_file_list = get_must_session_option("audio_output_file_list", "请先生成配音文件列表")
        
        # 3. 视频混剪服务初始化
        video_mix_service = VideoMixService()
        
        # 4. 处理每个场景的视频和音频匹配
        for video_dir, audio_file in zip(video_dir_list, audio_file_list):
            matching_videos, total_length = video_mix_service.match_videos_from_dir(
                video_dir, audio_file, is_head=(i==0))
        
        # 5. 音频拼接
        final_audio_output_file = concat_audio_list(audio_output_file_list)
        
        # 6. 生成字幕
        st.write(tr("Generate Video subtitles..."))
        main_generate_subtitle()
        
        # 7. 视频服务初始化和标准化
        video_service = VideoService(final_video_file_list, final_audio_output_file)
        video_service.normalize_video()
        
        # 8. 生成最终视频
        st.write(tr("Generate Video..."))
        video_file = video_service.generate_video_with_audio()
        
        # 9. 添加字幕（如果启用）
        if enable_subtitles:
            st.write(tr("Add Subtitles..."))
            # 字幕处理逻辑
```

### 2. VideoMixService 核心算法

**类功能**: 负责视频素材的智能匹配和选择

#### 初始化参数:
```python
def __init__(self):
    self.fps = st.session_state["video_fps"]
    self.segment_min_length = st.session_state["video_segment_min_length"]
    self.segment_max_length = st.session_state["video_segment_max_length"]
    self.target_width, self.target_height = st.session_state["video_size"].split('x')
    
    # 背景音乐配置
    self.enable_background_music = st.session_state["enable_background_music"]
    self.background_music = st.session_state["background_music"]
    self.background_music_volume = st.session_state["background_music_volume"]
    
    # 转场效果配置
    self.enable_video_transition_effect = st.session_state["enable_video_transition_effect"]
    self.video_transition_effect_duration = st.session_state["video_transition_effect_duration"]
```

#### 视频匹配算法:
```python
def match_videos_from_dir(self, video_dir, audio_file, is_head=False):
    # 1. 获取音频时长
    audio_duration = get_audio_duration(audio_file)
    
    # 2. 扫描媒体文件
    media_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.mp4', '.mov'))]
    
    # 3. 随机排序确保内容多样性
    random.shuffle(media_files)
    
    # 4. 优先选择视频文件
    video_files = [f for f in media_files if f.lower().endswith(('.mp4', '.mov'))]
    if video_files:
        random_video = random.choice(video_files)
        media_files.remove(random_video)
        media_files.insert(0, random_video)  # 将视频文件放在首位
    
    # 5. 按音频时长匹配视频片段
    total_length = 0
    matching_videos = []
    for video_file in media_files:
        # 计算视频时长
        if video_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            video_duration = self.default_duration  # 图片默认时长
        else:
            video_duration = get_video_duration(video_file)
        
        # 时长标准化
        if video_duration < self.segment_min_length:
            video_duration = self.segment_min_length
        if video_duration > self.segment_max_length:
            video_duration = self.segment_max_length
        
        # 检查是否需要更多片段
        if total_length < audio_duration:
            # 转场效果时长计算
            if self.enable_video_transition_effect:
                if i == 0 and is_head:
                    total_length += video_duration
                else:
                    total_length += video_duration - float(self.video_transition_effect_duration)
            else:
                total_length += video_duration
            
            matching_videos.append(video_file)
        else:
            # 音频延长以匹配视频
            extend_length = audio_duration - total_length
            if extend_length > 0:
                extent_audio(audio_file, int(math.ceil(extend_length)))
            break
    
    # 6. 验证资源充足性
    if total_length < audio_duration:
        st.toast(tr("You Need More Resource"), icon="⚠️")
        st.stop()
    
    return matching_videos, total_length
```

### 3. VideoService 视频处理

**类功能**: 负责最终视频的合成和处理

#### 核心方法:
- `normalize_video()`: 视频标准化处理
- `generate_video_with_audio()`: 合成音视频
- 支持背景音乐混合
- 支持转场效果应用
- 支持字幕叠加

### 4. 会话状态管理

**关键会话状态变量**:
```python
# 场景配置
st.session_state['scene_number']  # 场景数量
st.session_state['video_scene_folder_N']  # 第N个场景的视频文件夹
st.session_state['video_scene_text_N']  # 第N个场景的文本内容

# 音频配置
st.session_state['audio_type']  # 音频类型
st.session_state['audio_language']  # 音频语言
st.session_state['audio_voice']  # 音频声音
st.session_state['audio_speed']  # 音频速度

# 视频配置
st.session_state['video_layout']  # 视频布局
st.session_state['video_fps']  # 视频帧率
st.session_state['video_size']  # 视频尺寸
st.session_state['video_segment_min_length']  # 最小片段长度
st.session_state['video_segment_max_length']  # 最大片段长度

# 字幕配置
st.session_state['enable_subtitles']  # 启用字幕
st.session_state['subtitle_font']  # 字幕字体
st.session_state['subtitle_color']  # 字幕颜色

# 生成控制
st.session_state['videos_count']  # 生成视频数量
```

## 技术特性

### 1. 智能素材选择
- 随机化算法确保内容多样性
- 优先选择视频文件而非图片
- 自动调整片段长度匹配音频时长
- 支持图片素材的默认时长设置

### 2. 多格式支持
- **视频格式**: MP4, MOV
- **图片格式**: JPG, JPEG, PNG
- **音频格式**: MP3, WAV
- **字幕格式**: 支持多种字体和样式

### 3. 自适应处理
- 根据选择的布局自动调整分辨率选项
- 智能音视频时长匹配
- 资源不足时的警告机制

### 4. 性能优化
- 会话状态持久化 (`save_session_state_to_yaml()`)
- 文件系统缓存
- 批量处理支持

### 5. 用户体验
- 实时状态显示
- 进度条和状态更新
- 错误处理和用户提示
- 音频测试功能

## 使用流程建议

### 1. 准备阶段
1. 准备视频素材文件夹（每个场景一个文件夹）
2. 准备文本内容文件（UTF-8编码，每行对应一个场景）
3. 准备背景音乐文件（可选）

### 2. 配置阶段
1. 设置场景数量和对应的素材路径
2. 选择音频类型和相关参数
3. 配置视频输出参数（分辨率、帧率等）
4. 设置字幕样式（如果需要）

### 3. 生成阶段
1. 设置生成视频数量
2. 点击生成按钮
3. 监控生成进度
4. 预览生成的视频

## 故障排除

### 常见问题:
1. **资源不足警告**: 增加素材文件或减少视频长度要求
2. **音频生成失败**: 检查TTS服务配置和网络连接
3. **视频合成失败**: 验证FFmpeg安装和PATH配置
4. **字幕显示异常**: 检查字体文件和编码格式

### 性能建议:
1. 使用SSD存储提高I/O性能
2. 合理设置视频分辨率以平衡质量和处理速度
3. 批量生成时适当降低并发数
4. 定期清理临时文件和缓存