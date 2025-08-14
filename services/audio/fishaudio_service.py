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
import json
import tempfile
import streamlit as st
from pathlib import Path
from pydub import AudioSegment

from services.audio.audio_service import AudioService
from tools.file_utils import convert_mp3_to_wav
from tools.utils import random_with_system_time

try:
    from fish_audio_sdk import Session, TTSRequest
except ImportError:
    print("❌ Fish Audio SDK 未安装")
    print("请运行: pip install fish-audio-sdk")
    Session = None
    TTSRequest = None

# 获取当前脚本的绝对路径
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# 音频输出目录
audio_output_dir = os.path.join(script_dir, "../../work")
audio_output_dir = os.path.abspath(audio_output_dir)


class FishAudioService(AudioService):
    def __init__(self):
        super().__init__()
        # 从FishAudio实现中获取API密钥和默认模型
        self.api_key = "808b20b16b3941e4b693f9c01ba8d0de"
        self.default_model_id = self._load_default_model_id()
        
        # 初始化Fish Audio会话
        if Session is not None:
            try:
                self.session = Session(self.api_key)
                print("✅ Fish Audio SDK 初始化成功")
            except Exception as e:
                print(f"❌ Fish Audio SDK 初始化失败: {e}")
                st.error(f"Fish Audio SDK 初始化失败: {e}")
                self.session = None
        else:
            self.session = None
            st.error("Fish Audio SDK 未安装，请运行: pip install fish-audio-sdk")

    def _load_default_model_id(self):
        """从models.json文件中加载默认的ALLE模型ID"""
        try:
            # 从fishaudio目录加载models.json
            fishaudio_dir = os.path.join(script_dir, "../../fishaudio")
            models_file = os.path.join(fishaudio_dir, "models.json")
            models_file = os.path.abspath(models_file)
            
            if os.path.exists(models_file):
                with open(models_file, 'r', encoding='utf-8') as f:
                    models_config = json.load(f)
                    # 获取ALLE模型ID
                    alle_model_id = models_config.get("aliases", {}).get("ALLE", "")
                    if alle_model_id:
                        print(f"✅ 加载ALLE模型ID: {alle_model_id}")
                        return alle_model_id
            
            # 如果无法加载，使用硬编码的默认值
            default_id = "59e9dc1cb20c452584788a2690c80970"
            print(f"⚠️ 使用默认ALLE模型ID: {default_id}")
            return default_id
            
        except Exception as e:
            print(f"❌ 加载模型配置失败: {e}")
            # 返回硬编码的默认值
            return "59e9dc1cb20c452584788a2690c80970"

    def save_with_ssml(self, text, file_name, voice, rate="0.00"):
        """实现AudioService接口 - 为远程TTS模式保存音频文件"""
        if self.session is None:
            raise Exception("Fish Audio SDK 未正确初始化")
        
        try:
            # 创建TTS请求
            tts_request = TTSRequest(
                text=text,
                reference_id=self.default_model_id,
                temperature=float(st.session_state.get("fishaudio_temperature", 0.7)),
                format="mp3"
            )
            
            # 创建临时MP3文件
            temp_mp3 = file_name + ".tmp.mp3"
            
            # 生成并保存音频
            print(f"🎵 开始生成音频: {os.path.basename(file_name)}")
            with open(temp_mp3, "wb") as f:
                chunk_count = 0
                for chunk in self.session.tts(tts_request):
                    f.write(chunk)
                    chunk_count += 1
                    if chunk_count % 10 == 0:  # 每10个chunk显示一次进度
                        print(f"📦 已处理 {chunk_count} 个音频块...")
            
            # 转换MP3到WAV格式（保持与现有流程兼容）
            if os.path.exists(temp_mp3):
                convert_mp3_to_wav(temp_mp3, file_name)
                os.remove(temp_mp3)  # 清理临时文件
                print(f"✅ 音频生成完成: {os.path.basename(file_name)}")
            else:
                raise Exception("临时音频文件生成失败")
                
        except Exception as e:
            print(f"❌ Fish Audio TTS 失败: {e}")
            st.error(f"Fish Audio TTS 失败: {e}")
            raise

    def read_with_ssml(self, text, voice, rate="0.00"):
        """实现AudioService接口 - 返回音频数据（用于预览等）"""
        if self.session is None:
            raise Exception("Fish Audio SDK 未正确初始化")
        
        try:
            # 创建TTS请求
            tts_request = TTSRequest(
                text=text,
                reference_id=self.default_model_id,
                temperature=float(st.session_state.get("fishaudio_temperature", 0.7)),
                format="mp3"
            )
            
            # 生成音频数据
            audio_data = b""
            for chunk in self.session.tts(tts_request):
                audio_data += chunk
            
            return audio_data
            
        except Exception as e:
            print(f"❌ Fish Audio TTS 预览失败: {e}")
            st.error(f"Fish Audio TTS 预览失败: {e}")
            raise

    def chat_with_content(self, content, audio_output_file):
        """为本地TTS模式实现接口 - 处理文本内容生成音频"""
        if self.session is None:
            raise Exception("Fish Audio SDK 未正确初始化")
        
        try:
            # 创建TTS请求
            tts_request = TTSRequest(
                text=content,
                reference_id=self.default_model_id,
                temperature=float(st.session_state.get("fishaudio_temperature", 0.7)),
                format="mp3"
            )
            
            # 创建临时MP3文件
            temp_mp3 = audio_output_file + ".tmp.mp3"
            
            # 生成并保存音频
            print(f"🎵 开始生成音频: {os.path.basename(audio_output_file)}")
            with open(temp_mp3, "wb") as f:
                chunk_count = 0
                for chunk in self.session.tts(tts_request):
                    f.write(chunk)
                    chunk_count += 1
                    if chunk_count % 10 == 0:  # 每10个chunk显示一次进度
                        print(f"📦 已处理 {chunk_count} 个音频块...")
            
            # 转换MP3到WAV格式（保持与现有流程兼容）
            if os.path.exists(temp_mp3):
                convert_mp3_to_wav(temp_mp3, audio_output_file)
                os.remove(temp_mp3)  # 清理临时文件
                print(f"✅ 音频生成完成: {os.path.basename(audio_output_file)}")
            else:
                raise Exception("临时音频文件生成失败")
                
        except Exception as e:
            print(f"❌ Fish Audio TTS 失败: {e}")
            st.error(f"Fish Audio TTS 失败: {e}")
            raise

    def test_audio_generation(self, test_text="这是一个Fish Audio语音合成测试。"):
        """测试音频生成功能"""
        if self.session is None:
            st.error("Fish Audio SDK 未正确初始化")
            return False
        
        try:
            # 生成测试音频文件
            test_filename = os.path.join(audio_output_dir, f"fishaudio_test_{random_with_system_time()}.wav")
            self.chat_with_content(test_text, test_filename)
            
            if os.path.exists(test_filename):
                st.success("✅ Fish Audio 测试成功!")
                st.audio(test_filename, format="audio/wav")
                return True
            else:
                st.error("❌ 测试音频文件生成失败")
                return False
                
        except Exception as e:
            st.error(f"❌ Fish Audio 测试失败: {e}")
            return False