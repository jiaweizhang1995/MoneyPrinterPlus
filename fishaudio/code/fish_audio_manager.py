#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fish Audio 交互式管理工具
提供文案生成、TTS转换、模型管理等功能
"""

import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# 设置控制台编码
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

try:
    from fish_audio_sdk import Session, TTSRequest
except ImportError:
    print("❌ Fish Audio SDK 未安装")
    print("请运行: pip install fish-audio-sdk")
    exit(1)


class FishAudioManager:
    def __init__(self):
        # 配置信息
        self.api_key = "808b20b16b3941e4b693f9c01ba8d0de"
        self.default_model_id = "59e9dc1cb20c452584788a2690c80970"  # ALLE model
        
        # 目录配置
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "output"
        self.text_prompts_dir = self.base_dir / "text_prompts"
        self.models_file = self.base_dir / "models.json"
        
        # 创建必要目录
        self._create_directories()
        
        # 初始化Fish Audio会话
        try:
            self.session = Session(self.api_key)
            print("✅ Fish Audio SDK 初始化成功")
        except Exception as e:
            print(f"❌ Fish Audio SDK 初始化失败: {e}")
            self.session = None

    def _create_directories(self):
        """创建必要的目录"""
        try:
            self.output_dir.mkdir(exist_ok=True)
            self.text_prompts_dir.mkdir(exist_ok=True)
            print(f"✅ 目录初始化完成: {self.output_dir}, {self.text_prompts_dir}")
        except Exception as e:
            print(f"❌ 目录创建失败: {e}")

    def _load_models_config(self) -> Dict:
        """加载模型配置文件"""
        if not self.models_file.exists():
            default_config = {"aliases": {}}
            with open(self.models_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
            return default_config
        
        try:
            with open(self.models_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 读取模型配置失败: {e}")
            return {"aliases": {}}

    def _save_models_config(self, config: Dict):
        """保存模型配置文件"""
        try:
            with open(self.models_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存模型配置失败: {e}")

    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _read_aliyun_template(self) -> str:
        """读取阿里云模板文件中的prompt"""
        aliyun_file = self.base_dir / "aliyun.md"
        try:
            with open(aliyun_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取prompt部分（从prompt=开始）
                if "prompt=" in content:
                    prompt_start = content.find("prompt=") + len("prompt=")
                    prompt_content = content[prompt_start:].strip()
                    return prompt_content
                else:
                    # 如果没有找到prompt=，返回默认模板
                    return self._get_default_prompt_template()
        except Exception as e:
            print(f"❌ 读取aliyun.md失败: {e}")
            return self._get_default_prompt_template()

    def _get_default_prompt_template(self) -> str:
        """默认的prompt模板"""
        return """You are a TikTok seller creating an AI-generated voiceover script for a 30–50 second ad for the DONBUKLL Collagen Sleeping Mask. The final script must be in fluent, natural-sounding English and designed to be spoken aloud within that time range (approximately 80–120 words). Begin with a relatable skincare pain point, then introduce the product as a soothing, effective solution. Highlight key ingredients (hyaluronic acid complex, hydrolyzed collagen, allantoin, linden extract) and their benefits (hydration, elasticity, calming redness, glass skin finish). Emphasize comfort ("no burning, no tightness"), luxury feel ("silk-like," "cooling all night"), and value (three masks under $30).
Here is an example : Have you ever put on a 'miracle mask and woken up to red bumps and that stinging fire alarm? Yeah, I have—my face protests like a crying baby.
"So tonight I'm trying the DONBUKLL Collagen Sleeping Mask. I slather it on—it feels like silk wrapped around my skin. It's packed with soothing botanicals like allantoin and linden to calm redness, while a hyaluronic acid complex and hydrolyzed collagen act like a sponge to lock in moisture and boost elasticity, giving my face a porcelain-doll, glass-like finish. No burning, no tightness—it feels like a cooling, hydrating mask all night long.
So, if your last mask felt like napalm, switch to a truly thoughtful one. Three masks under $30 is better than a day of burning. Shop with a tap and sleep peacefully."""

    def generate_content_from_template(self) -> str:
        """基于模板生成文案内容"""
        template = self._read_aliyun_template()
        
        # 从模板中提取示例脚本
        if "Here is an example :" in template:
            example_start = template.find("Here is an example :") + len("Here is an example :")
            example_content = template[example_start:].strip()
            return example_content
        
        # 如果没找到示例，返回默认的示例脚本
        return """Have you ever put on a 'miracle mask and woken up to red bumps and that stinging fire alarm? Yeah, I have—my face protests like a crying baby.
So tonight I'm trying the DONBUKLL Collagen Sleeping Mask. I slather it on—it feels like silk wrapped around my skin. It's packed with soothing botanicals like allantoin and linden to calm redness, while a hyaluronic acid complex and hydrolyzed collagen act like a sponge to lock in moisture and boost elasticity, giving my face a porcelain-doll, glass-like finish. No burning, no tightness—it feels like a cooling, hydrating mask all night long.
So, if your last mask felt like napalm, switch to a truly thoughtful one. Three masks under $30 is better than a day of burning. Shop with a tap and sleep peacefully."""

    def option_1_auto_mode(self):
        """选项1：全自动模式"""
        print("\n🤖 执行全自动模式...")
        
        try:
            # 生成文案
            prompt_content = self.generate_content_from_template()
            print("✅ 文案生成完成")
            
            # 生成时间戳
            timestamp = self._get_timestamp()
            
            # 保存文案到txt文件
            txt_filename = f"aliyun_prompt_auto_{timestamp}.txt"
            txt_path = self.output_dir / txt_filename
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(prompt_content)
            print(f"✅ 文案已保存: {txt_filename}")
            
            # 调用Fish Audio API生成音频
            if self.session is None:
                print("❌ Fish Audio会话未初始化，无法生成音频")
                return
            
            print("🎵 开始生成音频...")
            tts_request = TTSRequest(
                text=prompt_content,
                reference_id=self.default_model_id,
                temperature=0.7,
                format="mp3"
            )
            
            # 保存音频文件
            mp3_filename = f"aliyun_prompt_auto_{timestamp}.mp3"
            mp3_path = self.output_dir / mp3_filename
            
            print("🎧 正在生成音频流...")
            with open(mp3_path, "wb") as f:
                chunk_count = 0
                for chunk in self.session.tts(tts_request):
                    f.write(chunk)
                    chunk_count += 1
                    if chunk_count % 10 == 0:  # 每10个chunk显示一次进度
                        print(f"📦 已处理 {chunk_count} 个音频块...")
            print("🎵 音频流生成完成")
            
            # 检查文件是否成功创建
            print("🔍 正在验证文件...")
            if mp3_path.exists():
                file_size = mp3_path.stat().st_size
                print(f"✅ 音频生成成功: {mp3_filename}")
                print(f"📁 文件大小: {file_size} bytes")
                print(f"🎉 MP3文件导出完成! 可以播放 {mp3_filename}")
            else:
                print("❌ 音频文件创建失败")
                
        except Exception as e:
            print(f"❌ 全自动模式执行失败: {e}")

    def option_2_generate_content(self):
        """选项2：仅生成文案"""
        print("\n📝 生成文案模式...")
        
        try:
            # 生成文案内容
            prompt_content = self.generate_content_from_template()
            
            # 生成时间戳和文件名
            timestamp = self._get_timestamp()
            filename = f"prompt_{timestamp}.txt"
            file_path = self.text_prompts_dir / filename
            
            # 保存文案
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(prompt_content)
            
            print(f"✅ 文案已生成并保存: {filename}")
            print(f"📄 文件路径: {file_path}")
            print(f"📊 内容长度: {len(prompt_content.split())} 词")
            
        except Exception as e:
            print(f"❌ 文案生成失败: {e}")

    def option_3_text_to_speech(self):
        """选项3：文本转语音（TTS）"""
        print("\n🎤 文本转语音模式...")
        
        # 检查text_prompts目录
        txt_files = list(self.text_prompts_dir.glob("*.txt"))
        if not txt_files:
            print("❌ text_prompts目录下没有找到.txt文件")
            return
        
        print(f"📁 找到 {len(txt_files)} 个文本文件")
        
        # 询问用户是否要使用自定义model_id
        print("\n请选择模型ID:")
        print(f"1. 使用默认模型 ({self.default_model_id})")
        print("2. 输入自定义模型ID")
        print("3. 使用已保存的模型别名")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        model_id = self.default_model_id
        if choice == "2":
            custom_model = input("请输入模型ID: ").strip()
            if custom_model:
                model_id = custom_model
        elif choice == "3":
            config = self._load_models_config()
            aliases = config.get("aliases", {})
            if aliases:
                print("\n已保存的模型别名:")
                for alias, mid in aliases.items():
                    print(f"  - {alias}: {mid}")
                alias_choice = input("请输入别名: ").strip()
                if alias_choice in aliases:
                    model_id = aliases[alias_choice]
                    print(f"✅ 使用模型: {alias_choice} ({model_id})")
                else:
                    print("❌ 别名不存在，使用默认模型")
            else:
                print("❌ 没有保存的模型别名，使用默认模型")
        
        print(f"\n🎯 使用模型ID: {model_id}")
        
        # 处理每个文本文件
        if self.session is None:
            print("❌ Fish Audio会话未初始化，无法生成音频")
            return
        
        success_count = 0
        for txt_file in txt_files:
            try:
                print(f"\n🔄 处理文件: {txt_file.name}")
                
                # 读取文本内容
                with open(txt_file, 'r', encoding='utf-8') as f:
                    text_content = f.read().strip()
                
                if not text_content:
                    print("⚠️  文件内容为空，跳过")
                    continue
                
                # 创建TTS请求
                tts_request = TTSRequest(
                    text=text_content,
                    reference_id=model_id,
                    temperature=0.7,
                    format="mp3"
                )
                
                # 生成音频文件名（与原文件名一致，但扩展名为.mp3）
                mp3_filename = txt_file.stem + ".mp3"
                mp3_path = self.output_dir / mp3_filename
                
                # 生成并保存音频
                print(f"🎧 正在生成音频: {mp3_filename}")
                with open(mp3_path, "wb") as f:
                    chunk_count = 0
                    for chunk in self.session.tts(tts_request):
                        f.write(chunk)
                        chunk_count += 1
                        if chunk_count % 10 == 0:  # 每10个chunk显示一次进度
                            print(f"📦 已处理 {chunk_count} 个音频块...")
                print(f"🎵 {mp3_filename} 音频生成完成")
                
                # 验证文件创建
                print("🔍 正在验证文件...")
                if mp3_path.exists():
                    file_size = mp3_path.stat().st_size
                    print(f"✅ 成功: {mp3_filename} ({file_size} bytes)")
                    print(f"🎉 {mp3_filename} 导出完成!")
                    success_count += 1
                else:
                    print(f"❌ 失败: {mp3_filename}")
                    
            except Exception as e:
                print(f"❌ 处理 {txt_file.name} 失败: {e}")
        
        print(f"\n📊 批量处理完成: {success_count}/{len(txt_files)} 个文件成功")
        if success_count == len(txt_files):
            print("🎉 所有音频文件都已成功生成并导出完成!")
        elif success_count > 0:
            print(f"⚠️  部分文件处理成功，请检查失败的文件")
        else:
            print("❌ 没有文件处理成功")

    def option_4_model_management(self):
        """选项4：模型ID管理"""
        while True:
            print("\n🛠️  模型ID管理")
            print("a) 新增 model_id")
            print("b) 删除 model_id") 
            print("c) 查看所有已保存 model_id")
            print("d) 返回主菜单")
            
            choice = input("请选择操作 (a-d): ").strip().lower()
            
            if choice == 'a':
                self._add_model_alias()
            elif choice == 'b':
                self._delete_model_alias()
            elif choice == 'c':
                self._view_model_aliases()
            elif choice == 'd':
                break
            else:
                print("❌ 无效选择，请重新输入")

    def _add_model_alias(self):
        """添加模型别名"""
        print("\n➕ 新增模型ID")
        
        alias = input("请输入别名（如'客服女声'）: ").strip()
        if not alias:
            print("❌ 别名不能为空")
            return
        
        model_id = input("请输入对应的model_id: ").strip()
        if not model_id:
            print("❌ model_id不能为空")
            return
        
        config = self._load_models_config()
        config["aliases"][alias] = model_id
        self._save_models_config(config)
        
        print(f"✅ 成功添加: {alias} -> {model_id}")

    def _delete_model_alias(self):
        """删除模型别名"""
        print("\n🗑️  删除模型ID")
        
        config = self._load_models_config()
        aliases = config.get("aliases", {})
        
        if not aliases:
            print("❌ 没有保存的模型别名")
            return
        
        print("当前已保存的别名:")
        for i, (alias, model_id) in enumerate(aliases.items(), 1):
            print(f"  {i}. {alias}: {model_id}")
        
        alias_to_delete = input("请输入要删除的别名: ").strip()
        if alias_to_delete in aliases:
            del config["aliases"][alias_to_delete]
            self._save_models_config(config)
            print(f"✅ 已删除别名: {alias_to_delete}")
        else:
            print("❌ 别名不存在")

    def _view_model_aliases(self):
        """查看所有模型别名"""
        print("\n👀 查看所有已保存的模型ID")
        
        config = self._load_models_config()
        aliases = config.get("aliases", {})
        
        if not aliases:
            print("❌ 没有保存的模型别名")
            return
        
        print("📋 已保存的模型别名:")
        for alias, model_id in aliases.items():
            print(f"  • {alias}: {model_id}")

    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*50)
        print("🎵 Fish Audio 交互式管理工具")
        print("="*50)
        print("1. 全自动模式")
        print("   └─ 生成文案 + 调用API生成音频")
        print("2. 仅生成文案")
        print("   └─ 基于aliyun.md模板生成prompt文案")
        print("3. 文本转语音（TTS）")
        print("   └─ 将text_prompts目录下的txt文件转为音频")
        print("4. 模型ID管理")
        print("   └─ 管理model_id别名映射")
        print("0. 退出程序")
        print("="*50)

    def run(self):
        """运行主程序"""
        print("🎵 Fish Audio 管理工具启动中...")
        print(f"📁 工作目录: {self.base_dir}")
        print(f"🔑 API密钥: {self.api_key[:8]}...{self.api_key[-8:]}")
        
        while True:
            self.show_menu()
            choice = input("请选择操作 (0-4): ").strip()
            
            if choice == "1":
                self.option_1_auto_mode()
            elif choice == "2":
                self.option_2_generate_content()
            elif choice == "3":
                self.option_3_text_to_speech()
            elif choice == "4":
                self.option_4_model_management()
            elif choice == "0":
                print("👋 程序退出，感谢使用！")
                break
            else:
                print("❌ 无效选择，请输入0-4之间的数字")
            
            input("\n按回车键继续...")


def main():
    """主函数"""
    try:
        manager = FishAudioManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n👋 程序被用户中断，感谢使用！")
    except Exception as e:
        print(f"\n❌ 程序运行错误: {e}")


if __name__ == "__main__":
    main()