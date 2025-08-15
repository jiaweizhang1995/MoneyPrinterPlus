#  Copyright © [2024] 程序那些事
#
#  All rights reserved. This software and associated documentation files (the "Software") are provided for personal and educational use only. Commercial use of the Software is strictly prohibited unless explicit permission is obtained from the author.
#
#  Permission is hereby granted to any person to use, copy, and modify the Software for non-commercial purposes, provided that the following conditions are met:
#
#  1. The original copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
#  2. Modifications, if any, must retain the original copyright information and must not imply that the modified version is an official version of the Software.
#  3. Any distribution of the Software or its modifications must retain the original copyright notice and include this permission notice.
#
#  For commercial use, including but not limited to selling, distributing, or using the Software as part of any commercial product or service, you must obtain explicit authorization from the author.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Author: 程序那些事
#  email: flydean@163.com
#  Website: [www.flydean.com](http://www.flydean.com)
#  GitHub: [https://github.com/ddean2009/MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus)
#
#  All rights reserved.
#
#

import os

import streamlit as st

from config.config import transition_types, fade_list, audio_languages, audio_types, load_session_state_from_yaml, \
    save_session_state_to_yaml, app_title, GPT_soVITS_languages, CosyVoice_voice, my_config
from main import main_generate_ai_video_for_mix, main_try_test_audio, get_audio_voices, main_try_test_local_audio, main_try_test_fishaudio
from pages.common import common_ui
from tools.tr_utils import tr
from tools.utils import get_file_map_from_dir

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)

# 脚本所在的目录
script_dir = os.path.dirname(script_path)

default_bg_music_dir = os.path.join(script_dir, "../bgmusic")
default_bg_music_dir = os.path.abspath(default_bg_music_dir)

default_chattts_dir = os.path.join(script_dir, "../chattts")
default_chattts_dir = os.path.abspath(default_chattts_dir)

load_session_state_from_yaml('02_first_visit')

if 'scene_number' not in st.session_state or st.session_state.get('scene_number', 0) == 0:
    st.session_state['scene_number'] = 4
    save_session_state_to_yaml()


def try_test_audio():
    main_try_test_audio()


def try_test_local_audio():
    main_try_test_local_audio()


def try_test_fishaudio():
    main_try_test_fishaudio()


def delete_scene_for_mix(video_scene_container):
    if 'scene_number' not in st.session_state or st.session_state['scene_number'] < 1:
        return
    st.session_state['scene_number'] = st.session_state['scene_number'] - 1
    save_session_state_to_yaml()


def add_more_scene_for_mix(video_scene_container):
    if 'scene_number' in st.session_state:
        # 最多5个场景
        if st.session_state['scene_number'] < 4:
            st.session_state['scene_number'] = st.session_state['scene_number'] + 1
        else:
            st.toast(tr("Maximum number of scenes reached"), icon="⚠️")
    else:
        st.session_state['scene_number'] = 1
    save_session_state_to_yaml()


def more_scene_fragment(video_scene_container):
    with video_scene_container:
        if 'scene_number' in st.session_state:
            for k in range(st.session_state['scene_number']):
                st.subheader(tr("Mix Video Scene") + str(k + 2))
                st.text_input(label=tr("Video Scene Resource"),
                              placeholder=tr("Please input video scene resource folder path"),
                              key="video_scene_folder_" + str(k + 2))
                # 条件显示文案路径输入框
                if not st.session_state.get("use_full_audio", False):
                    st.text_input(label=tr("Video Scene Text"), placeholder=tr("Please input video scene text path"),
                                  key="video_scene_text_" + str(k + 2))
                else:
                    st.info("📝 已启用完整音频模式，无需输入文案路径")


def generate_video_for_mix(video_generator):
    save_session_state_to_yaml()
    videos_count = st.session_state.get('videos_count')
    if videos_count is not None:
        for i in range(int(videos_count)):
            print(i)
            main_generate_ai_video_for_mix(video_generator)


common_ui()

st.markdown(f"<h1 style='text-align: center; font-weight:bold; font-family:comic sans ms; padding-top: 0rem;'> \
            {app_title}</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;padding-top: 0rem;'>By 阿城</h2>", unsafe_allow_html=True)

# 场景设置
mix_video_container = st.container(border=True)
with mix_video_container:
    st.subheader(tr("Mix Video"))
    
    # 完整音频选项
    full_audio_container = st.container(border=True)
    with full_audio_container:
        st.subheader("🎵 完整音频配置")
        audio_columns = st.columns(2)
        with audio_columns[0]:
            use_full_audio = st.checkbox(label="是否使用完整音频", 
                                       key="use_full_audio", 
                                       value=False,
                                       help="启用后将跳过TTS语音合成，直接使用MP3音频文件")
        with audio_columns[1]:
            if use_full_audio:
                st.text_input(label="音频文件目录", 
                            placeholder="请输入包含MP3文件的目录路径",
                            key="full_audio_dir",
                            help="系统将从此目录随机选择MP3文件作为配音")
    
    video_scene_container = st.container(border=True)
    with video_scene_container:
        st.subheader(tr("Mix Video Scene") + str(1))
        st.text_input(label=tr("Video Scene Resource"), placeholder=tr("Please input video scene resource folder path"),
                      key="video_scene_folder_" + str(1))
        # 条件显示文案路径输入框
        if not st.session_state.get("use_full_audio", False):
            st.text_input(label=tr("Video Scene Text"), placeholder=tr("Please input video scene text path"),
                          help=tr("One Line Text For One Scene,UTF-8 encoding"),
                          key="video_scene_text_" + str(1))
        else:
            st.info("📝 已启用完整音频模式，无需输入文案路径")
    more_scene_fragment(video_scene_container)
    st_columns = st.columns(2)
    with st_columns[0]:
        st.button(label=tr("Add More Scene"), type="primary", on_click=add_more_scene_for_mix,
                  args=(video_scene_container,))
    with st_columns[1]:
        st.button(label=tr("Delete Extra Scene"), type="primary", on_click=delete_scene_for_mix,
                  args=(video_scene_container,))

# FishAudio 配音区域
captioning_container = st.container(border=True)
with captioning_container:
    # 配音
    st.subheader(tr("Video Captioning") + " - Fish Audio")
    
    # 检查是否启用完整音频模式
    if st.session_state.get("use_full_audio", False):
        st.warning("⚠️ 已启用完整音频模式，将跳过TTS语音合成流程")
        st.info("🎵 系统将直接使用MP3音频文件进行配音，无需配置语音合成参数")
    else:
        # FishAudio 配置
        st.info("🐟 使用 Fish Audio 高质量语音合成服务，基于ALLE模型")
        
        llm_columns = st.columns(3)
        with llm_columns[0]:
            # 音频温度参数
            st.slider(
                label="音频温度 (Temperature)", 
                min_value=0.1, 
                max_value=1.0, 
                value=0.7, 
                step=0.1,
                key="fishaudio_temperature",
                help="控制语音的随机性，较低值更稳定，较高值更多样化"
            )
        
        with llm_columns[1]:
            # 音频格式选择
            st.selectbox(
                label="音频格式",
                options=["mp3", "wav"],
                index=0,
                key="fishaudio_format",
                help="选择输出音频格式"
            )
        
        with llm_columns[2]:
            # 测试按钮
            st.button(
                label="🎵 测试 Fish Audio", 
                type="primary", 
                on_click=try_test_fishaudio,
                help="测试Fish Audio语音合成效果"
            )
        
        # 模型信息
        st.caption("🔧 当前使用模型: ALLE (高质量多语言TTS模型)")
        st.caption("📝 支持从文案文件随机选取文本进行语音合成")

recognition_container = st.container(border=True)
with recognition_container:
    # 配音
    st.subheader(tr("Audio recognition"))
    llm_columns = st.columns(4)
    with llm_columns[0]:
        st.selectbox(label=tr("Choose recognition type"), options=audio_types, format_func=lambda x: audio_types.get(x),
                     key="recognition_audio_type")

# 背景音乐
bg_music_container = st.container(border=True)
with bg_music_container:
    # 背景音乐
    st.subheader(tr("Video Background Music"))
    llm_columns = st.columns(2)
    with llm_columns[0]:
        st.text_input(label=tr("Background Music Dir"), placeholder=tr("Input Background Music Dir"),
                      value=default_bg_music_dir,
                      key="background_music_dir")

    with llm_columns[1]:
        nest_columns = st.columns(3)
        with nest_columns[0]:
            st.checkbox(label=tr("Enable background music"), key="enable_background_music", value=True)
        with nest_columns[1]:
            bg_music_list = get_file_map_from_dir(st.session_state["background_music_dir"], ".mp3,.wav")
            st.selectbox(label=tr("Background music"), key="background_music",
                         options=bg_music_list, format_func=lambda x: bg_music_list[x])
        with nest_columns[2]:
            st.slider(label=tr("Background music volume"), min_value=0.0, value=0.3, max_value=1.0, step=0.1,
                      key="background_music_volume")

# 视频配置
video_container = st.container(border=True)
with video_container:
    st.subheader(tr("Video Config"))
    llm_columns = st.columns(3)
    with llm_columns[0]:
        layout_options = {"portrait": "竖屏", "landscape": "横屏", "square": "方形"}
        st.selectbox(label=tr("video layout"), key="video_layout", options=layout_options,
                     format_func=lambda x: layout_options[x])
    with llm_columns[1]:
        st.selectbox(label=tr("video fps"), key="video_fps", options=[20, 25, 30])
    with llm_columns[2]:
        if st.session_state.get("video_layout") == "portrait":
            video_size_options = {"1080x1920": "1080p", "720x1280": "720p", "480x960": "480p", "360x720": "360p",
                                  "240x480": "240p"}
        elif st.session_state.get("video_layout") == "landscape":
            video_size_options = {"1920x1080": "1080p", "1280x720": "720p", "960x480": "480p", "720x360": "360p",
                                  "480x240": "240p"}
        else:
            video_size_options = {"1080x1080": "1080p", "720x720": "720p", "480x480": "480p", "360x360": "360p",
                                  "240x240": "240p"}
        st.selectbox(label=tr("video size"), key="video_size", options=video_size_options,
                     format_func=lambda x: video_size_options[x])
    llm_columns = st.columns(2)
    with llm_columns[0]:
        st.slider(label=tr("video segment min length"), min_value=5, value=5, max_value=10, step=1,
                  key="video_segment_min_length")
    with llm_columns[1]:
        st.slider(label=tr("video segment max length"), min_value=5, value=10, max_value=30, step=1,
                  key="video_segment_max_length")
    llm_columns = st.columns(4)
    with llm_columns[0]:
        st.checkbox(label=tr("Enable video Transition effect"), key="enable_video_transition_effect", value=True)
    with llm_columns[1]:
        st.selectbox(label=tr("video Transition effect"), key="video_transition_effect_type", options=transition_types)
    with llm_columns[2]:
        st.selectbox(label=tr("video Transition effect types"), key="video_transition_effect_value", options=fade_list)
    with llm_columns[3]:
        st.selectbox(label=tr("video Transition effect duration"), key="video_transition_effect_duration",
                     options=["1", "2"])

# 字幕
subtitle_container = st.container(border=True)
with subtitle_container:
    st.subheader(tr("Video Subtitles"))
    llm_columns = st.columns(4)
    with llm_columns[0]:
        # 当启用完整音频模式时禁用字幕选项
        use_full_audio = st.session_state.get("use_full_audio", False)
        if use_full_audio:
            st.checkbox(label=tr("Enable subtitles"), key="enable_subtitles", value=False, disabled=True, 
                       help="完整音频模式下不支持字幕生成")
        else:
            st.checkbox(label=tr("Enable subtitles"), key="enable_subtitles", value=True)
    with llm_columns[1]:
        st.selectbox(label=tr("subtitle font"), key="subtitle_font",
                     options=["Songti SC Bold",
                              "Songti SC Black",
                              "Songti SC Light",
                              "STSong",
                              "Songti SC Regular",
                              "PingFang SC Regular",
                              "PingFang SC Medium",
                              "PingFang SC Semibold",
                              "PingFang SC Light",
                              "PingFang SC Thin",
                              "PingFang SC Ultralight"], )
    with llm_columns[2]:
        st.selectbox(label=tr("subtitle font size"), key="subtitle_font_size", index=1,
                     options=[4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    with llm_columns[3]:
        st.selectbox(label=tr("subtitle lines"), key="captioning_lines", index=1,
                     options=[1, 2])

    llm_columns = st.columns(4)
    with llm_columns[0]:
        subtitle_position_options = {5: "top left",
                                     6: "top center",
                                     7: "top right",
                                     9: "center left",
                                     10: "center",
                                     11: "center right",
                                     1: "bottom left",
                                     2: "bottom center",
                                     3: "bottom right"}
        st.selectbox(label=tr("subtitle position"), key="subtitle_position", index=7,
                     options=subtitle_position_options, format_func=lambda x: subtitle_position_options[x])
    with llm_columns[1]:
        st.color_picker(label=tr("subtitle color"), key="subtitle_color", value="#FFFFFF")
    with llm_columns[2]:
        st.color_picker(label=tr("subtitle border color"), key="subtitle_border_color", value="#000000")
    with llm_columns[3]:
        st.slider(label=tr("subtitle border width"), min_value=0, value=0, max_value=4, step=1,
                  key="subtitle_border_width")

# 花式文本叠加
fancy_text_container = st.container(border=True)
with fancy_text_container:
    st.subheader("✨ 花式文本叠加")
    
    # 导入花式文本服务用于预览
    try:
        from services.video.fancy_text_service import FancyTextService
        fancy_service = FancyTextService()
        config_loaded = True
    except Exception as e:
        st.error(f"加载花式文本服务失败: {e}")
        config_loaded = False
    
    if config_loaded:
        # 第一行：基础控制
        fancy_columns_1 = st.columns(4)
        with fancy_columns_1[0]:
            st.checkbox(label="启用花式文本", key="enable_fancy_text", value=False, 
                       help="在视频中添加产品名称和卖点的花式文本叠加")
        
        with fancy_columns_1[1]:
            st.slider(label="显示频率（秒）", min_value=10, value=25, max_value=60, step=5,
                     key="fancy_text_frequency", help="每隔多少秒显示一次文本")
        
        with fancy_columns_1[2]:
            st.slider(label="显示时长（秒）", min_value=2, value=4, max_value=8, step=1,
                     key="fancy_text_duration", help="每次显示文本的持续时间")
        
        with fancy_columns_1[3]:
            position_options = {"top_center": "顶部居中", "top_left": "顶部左侧", 
                              "center": "屏幕中央", "bottom_center": "底部居中"}
            st.selectbox(label="显示位置", key="fancy_text_position", 
                        options=position_options, format_func=lambda x: position_options[x],
                        help="选择文本在视频中的显示位置")
        
        # 第二行：样式控制
        if st.session_state.get("enable_fancy_text", False):
            fancy_columns_2 = st.columns(3)
            with fancy_columns_2[0]:
                content_options = {"phrases": "产品短语", "advantages": "产品优势", "mixed": "混合显示"}
                st.selectbox(label="内容类型", key="fancy_text_content_type",
                           options=content_options, format_func=lambda x: content_options[x],
                           help="选择显示的文本内容类型")
            
            with fancy_columns_2[1]:
                st.checkbox(label="随机位置", key="fancy_text_random_position", value=True,
                           help="启用后文本位置会在预设位置中随机选择")
            
            with fancy_columns_2[2]:
                st.checkbox(label="启用动画效果", key="fancy_text_animation", value=True,
                           help="文本显示时使用淡入淡出等动画效果")
            
            # 第三行：字体和颜色设置
            fancy_columns_3 = st.columns(4)
            with fancy_columns_3[0]:
                st.color_picker(label="主标题颜色", key="fancy_text_main_color", value="#FFFFFF",
                               help="主标题文本的颜色")
            
            with fancy_columns_3[1]:
                st.color_picker(label="副标题颜色", key="fancy_text_sub_color", value="#000000",
                               help="副标题文本的颜色")
            
            with fancy_columns_3[2]:
                st.color_picker(label="背景颜色", key="fancy_text_bg_color", value="#FFA500",
                               help="副标题背景框的颜色")
            
            with fancy_columns_3[3]:
                st.checkbox(label="启用文本阴影", key="fancy_text_shadow", value=True,
                           help="为文本添加阴影效果增强可读性")
            
            # 预览区域
            with st.expander("📱 文本效果预览", expanded=False):
                preview_col1, preview_col2 = st.columns(2)
                
                with preview_col1:
                    st.markdown("**主标题样式预览:**")
                    main_preview = fancy_service.preview_text_style('main_title')
                    sample_main, sample_sub = main_preview.get('sample_text', ('Donbukll', 'wrapping mask'))
                    
                    main_color = st.session_state.get('fancy_text_main_color', '#FFFFFF')
                    st.markdown(f'<p style="font-size: 28px; color: {main_color}; font-style: italic; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{sample_main}</p>', 
                               unsafe_allow_html=True)
                
                with preview_col2:
                    st.markdown("**副标题样式预览:**")
                    sub_color = st.session_state.get('fancy_text_sub_color', '#000000')
                    bg_color = st.session_state.get('fancy_text_bg_color', '#FFA500')
                    st.markdown(f'<p style="font-size: 20px; color: {sub_color}; background-color: {bg_color}; padding: 8px 12px; border-radius: 6px; display: inline-block;">{sample_sub}</p>', 
                               unsafe_allow_html=True)
                
                st.info("💡 提示：文本内容会根据配置文件中的产品信息和优势自动随机选择显示")
    else:
        st.warning("⚠️ 花式文本服务未正确加载，请检查配置文件")

# 生成视频
video_generator = st.container(border=True)
with video_generator:
    st.slider(label=tr("how many videos do you want"), min_value=1, value=1, max_value=100, step=1,
              key="videos_count")
    st.button(label=tr("Generate Video Button"), type="primary", on_click=generate_video_for_mix,
              args=(video_generator,))
result_video_file = st.session_state.get("result_video_file")
if result_video_file:
    st.video(result_video_file)