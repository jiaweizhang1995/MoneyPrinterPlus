# Fish Audio 交互式管理工具

## 功能概述

这是一个基于Fish Audio SDK的Python交互式管理工具，提供文案生成、TTS转换和模型管理功能。

## 安装要求

```bash
pip install fish-audio-sdk
```

Python版本要求：>= 3.10

## 使用方法

### 启动脚本

```bash
cd fish_audio/code
python fish_audio_manager.py
```

### 功能说明

#### 1. 全自动模式
- 自动基于`aliyun.md`中的文案模板生成TikTok广告脚本
- 调用Fish Audio API生成MP3音频文件
- 文件保存格式：
  - 音频：`output/aliyun_prompt_auto_YYYYMMDD_HHMMSS.mp3`
  - 文案：`output/aliyun_prompt_auto_YYYYMMDD_HHMMSS.txt`

#### 2. 仅生成文案
- 生成符合30-50秒语音要求的营销文案（80-120词）
- 包含情感标签：(excited), (satisfied), (grateful)等
- 文件保存至：`text_prompts/prompt_YYYYMMDD_HHMMSS.txt`

#### 3. 文本转语音（TTS）
- 批量处理`text_prompts/`目录下的所有`.txt`文件
- 支持自定义模型ID选择
- 支持使用保存的模型别名
- 输出文件：`output/[原文件名].mp3`

#### 4. 模型ID管理
- **新增别名**：为长模型ID创建易记的别名（如"客服女声"）
- **删除别名**：移除不需要的模型别名
- **查看别名**：显示所有已保存的模型映射
- 配置文件：`models.json`

## 配置信息

- **API密钥**：`808b20b16b3941e4b693f9c01ba8d0de`
- **默认模型ID**：`92216edbdcc34e089ec646200cc6d0be`
- **基础URL**：使用Fish Audio官方API

## 目录结构

```
fish_audio/
├── code/
│   ├── fish_audio_manager.py    # 主脚本
│   ├── test_script.py          # 测试脚本
│   └── README.md               # 使用说明
├── output/                     # 生成的音频和文案文件
├── text_prompts/              # 待转换的文本文件
├── models.json                # 模型别名配置
├── API_Documentation.md       # API文档
├── aliyun.md                  # 文案模板
└── fish_audio_test.py         # 原始测试文件
```

## 示例使用流程

### 快速开始（全自动模式）
1. 运行脚本：`python fish_audio_manager.py`
2. 选择选项1（全自动模式）
3. 系统自动生成文案并转换为音频
4. 在`output/`目录查看结果

### 自定义文案转语音
1. 将自定义文案保存为`.txt`文件到`text_prompts/`目录
2. 运行脚本，选择选项3
3. 选择模型ID（默认/自定义/别名）
4. 等待批量处理完成

### 模型管理
1. 选择选项4进入模型管理
2. 添加常用模型别名：
   - 别名：`客服女声`
   - 模型ID：`your_model_id_here`
3. 在TTS功能中直接使用别名

## 文案模板特点

生成的文案遵循以下规范：
- **时长**：30-50秒语音（约80-120词）
- **结构**：痛点描述 → 产品介绍 → 功效说明 → 购买号召
- **情感标签**：句首使用情感标记提升语音表现力
- **产品信息**：针对DONBUKLL胶原蛋白睡眠面膜
- **关键成分**：透明质酸、水解胶原蛋白、尿囊素、椴树提取物

## 错误处理

脚本包含完整的异常处理机制：
- 网络连接失败自动重试提示
- 文件读写权限检查
- API调用错误详细报告
- 用户输入验证和格式检查

## 注意事项

1. 确保网络连接稳定，API调用需要网络访问
2. 首次运行会自动创建必要的目录结构
3. 生成的音频文件为MP3格式，适合各种播放设备
4. 文案内容为英文，针对海外TikTok营销场景
5. 模型别名配置会持久保存在`models.json`中

## 故障排除

- **SDK导入错误**：确认已安装`fish-audio-sdk`
- **编码问题**：脚本已适配Windows系统UTF-8编码
- **API调用失败**：检查网络连接和API密钥有效性
- **文件权限错误**：确认对工作目录有读写权限