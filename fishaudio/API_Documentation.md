# API Documentation

## 概述
本文档描述了语音AI平台的REST API接口，包括用户钱包管理和语音模型管理功能。

## 基础信息

### 基础URL
```
https://api.example.com
```

### 认证方式
所有API请求都需要Bearer Token认证：
```
Authorization: Bearer <your_token>
```

### 响应格式
- 成功响应格式: `application/json`
- 时间格式: ISO 8601 (例: `2023-12-01T10:00:00Z`)

---

## 钱包管理 API

### 1. 获取API积分余额

**接口描述**: 获取用户当前API积分余额

**请求信息**:
- **HTTP方法**: `GET`
- **路径**: `/wallet/{user_id}/api-credit`
- **参数**:
  - **路径参数**:
    - `user_id` (string, required): 用户ID，可使用 `self` 表示当前用户
  - **查询参数**:
    - `check_free_credit` (boolean, optional, default: false): 是否检查免费积分

**请求示例**:
```http
GET /wallet/self/api-credit?check_free_credit=true
Authorization: Bearer your_token_here
```

**响应格式**:
- **状态码**: `200 OK`
- **响应体**:
```json
{
  "_id": "string",
  "user_id": "string",
  "credit": "string",
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z",
  "has_phone_sha256": true,
  "has_free_credit": true
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| _id | string | 记录唯一标识符 |
| user_id | string | 用户ID |
| credit | string | 积分余额 |
| created_at | string | 创建时间 |
| updated_at | string | 更新时间 |
| has_phone_sha256 | boolean | 是否已验证手机号 |
| has_free_credit | boolean/null | 是否有免费积分 |

---

### 2. 获取用户Premium信息

**接口描述**: 获取用户Premium套餐信息

**请求信息**:
- **HTTP方法**: `GET`
- **路径**: `/wallet/{user_id}/package`
- **参数**:
  - **路径参数**:
    - `user_id` (string, required): 用户ID，可使用 `self` 表示当前用户

**请求示例**:
```http
GET /wallet/self/package
Authorization: Bearer your_token_here
```

**响应格式**:
- **状态码**: `200 OK`
- **响应体**:
```json
{
  "user_id": "string",
  "type": "string",
  "total": 100,
  "balance": 50,
  "created_at": "string",
  "updated_at": "string",
  "finished_at": "string"
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | string | 用户ID |
| type | string | 套餐类型 |
| total | integer | 总量 |
| balance | integer | 余额 |
| created_at | string | 创建时间 |
| updated_at | string | 更新时间 |
| finished_at | string | 结束时间 |

---

## 模型管理 API

### 1. 获取模型列表

**接口描述**: 获取所有可用模型的列表，支持筛选和分页

**请求信息**:
- **HTTP方法**: `GET`
- **路径**: `/model`
- **参数**:
  - **查询参数**:
    - `page_size` (integer, optional, default: 10): 每页数量
    - `page_number` (integer, optional, default: 1): 页码
    - `title` (string, optional): 按标题筛选
    - `tag` (string[], optional): 按标签筛选
    - `self` (boolean, optional, default: false): 是否只返回用户自己创建的模型
    - `author_id` (string, optional): 按作者ID筛选（self为true时忽略）
    - `language` (string[], optional): 按语言筛选
    - `title_language` (string[], optional): 按标题语言筛选
    - `sort_by` (string, optional, default: "score"): 排序方式，可选值: `score`, `task_count`, `created_at`

**请求示例**:
```http
GET /model?page_size=20&page_number=1&sort_by=created_at&self=false
Authorization: Bearer your_token_here
```

**响应格式**:
- **状态码**: `200 OK`
- **响应体**:
```json
{
  "total": 100
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| total | integer | 模型总数 |

---

### 2. 创建语音模型

**接口描述**: 创建新的语音合成模型

**请求信息**:
- **HTTP方法**: `POST`
- **路径**: `/model`
- **Content-Type**: `multipart/form-data` 或 `application/msgpack`
- **参数**:
  - **必需字段**:
    - `type` (enum): 模型类型，当前支持 `tts`（文本转语音）
    - `title` (string): 模型标题或名称
    - `train_mode` (enum): 训练模式，当前支持 `fast`（快速模式，创建后立即可用）
    - `voices` (file[]): 用于训练模型的语音文件
  - **可选字段**:
    - `visibility` (enum, default: "public"): 可见性，可选值: `public`（公开）, `unlist`（不公开但可通过链接访问）, `private`（私有）
    - `description` (string): 模型描述
    - `cover_image` (file): 模型封面图片（公开模型必需）
    - `texts` (string[]): 对应语音的文本（未指定时将自动进行ASR识别）
    - `tags` (string[]): 模型标签
    - `enhance_audio_quality` (boolean, default: false): 是否增强音频质量

**请求示例**:
```http
POST /model
Authorization: Bearer your_token_here
Content-Type: multipart/form-data

type=tts&
title=MyVoiceModel&
train_mode=fast&
visibility=public&
description=My custom voice model&
enhance_audio_quality=true&
voices=@voice1.wav&
voices=@voice2.wav&
cover_image=@cover.jpg
```

**响应格式**:
- **状态码**: `201 Created`
- **响应体**:
```json
{
  "_id": "string",
  "type": "tts",
  "title": "string",
  "description": "string",
  "cover_image": "string",
  "state": "created",
  "tags": ["tag1", "tag2"],
  "created_at": "2023-12-01T10:00:00Z",
  "updated_at": "2023-12-01T10:00:00Z",
  "visibility": "public",
  "like_count": 0,
  "mark_count": 0,
  "shared_count": 0,
  "task_count": 0,
  "author": {},
  "train_mode": "fast",
  "samples": [],
  "languages": ["zh-CN"],
  "lock_visibility": false,
  "unliked": false,
  "liked": false,
  "marked": false
}
```

**响应字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| _id | string | 模型唯一标识符 |
| type | enum | 模型类型：`svc`, `tts` |
| title | string | 模型标题 |
| description | string | 模型描述 |
| cover_image | string | 封面图片URL |
| state | enum | 模型状态：`created`, `training`, `trained`, `failed` |
| tags | string[] | 标签列表 |
| created_at | string | 创建时间 |
| updated_at | string | 更新时间 |
| visibility | enum | 可见性：`public`, `unlist`, `private` |
| like_count | integer | 点赞数 |
| mark_count | integer | 收藏数 |
| shared_count | integer | 分享数 |
| task_count | integer | 任务数 |
| author | object | 作者信息 |
| train_mode | enum | 训练模式：`fast`, `full` |
| samples | array | 样本数据 |
| languages | string[] | 支持的语言 |
| lock_visibility | boolean | 是否锁定可见性 |
| liked | boolean | 当前用户是否点赞 |
| marked | boolean | 当前用户是否收藏 |

---

### 3. 获取模型详情

**接口描述**: 获取指定模型的详细信息

**请求信息**:
- **HTTP方法**: `GET`
- **路径**: `/model/{id}`
- **参数**:
  - **路径参数**:
    - `id` (string, required): 模型ID

**请求示例**:
```http
GET /model/60f7b3b4c9e77c001f5e4e5a
Authorization: Bearer your_token_here
```

**响应格式**:
- **状态码**: `200 OK`
- **响应体**: 与创建模型响应格式相同

---

### 4. 删除模型

**接口描述**: 删除指定的模型

**请求信息**:
- **HTTP方法**: `DELETE`
- **路径**: `/model/{id}`
- **参数**:
  - **路径参数**:
    - `id` (string, required): 模型ID

**请求示例**:
```http
DELETE /model/60f7b3b4c9e77c001f5e4e5a
Authorization: Bearer your_token_here
```

**响应格式**:
- **状态码**: `200 OK`
- **响应体**: 操作成功确认

---

## 错误码说明

### HTTP状态码
- `200 OK`: 请求成功
- `201 Created`: 资源创建成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 认证失败
- `403 Forbidden`: 权限不足
- `404 Not Found`: 资源不存在
- `429 Too Many Requests`: 请求频率超限
- `500 Internal Server Error`: 服务器内部错误

### 通用错误响应格式
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述信息",
    "details": {}
  }
}
```

## 使用限制

1. **API调用频率限制**: 每分钟最多1000次请求
2. **文件上传限制**: 
   - 语音文件: 最大50MB，支持格式 wav, mp3, flac
   - 图片文件: 最大10MB，支持格式 jpg, png, gif
3. **模型数量限制**: 每个用户最多可创建100个模型

## SDK和工具

### Fish Audio SDK (Python)

官方Python SDK，提供完整的API调用封装。

#### 安装
```bash
pip install fish-audio-sdk
```

**系统要求**: Python >=3.10

#### 基本用法

##### 初始化
```python
from fish_audio_sdk import Session

# 创建会话，使用API密钥
session = Session("your_api_key")

# 可选：自定义端点
session = Session("your_api_key", base_url="https://your-proxy-domain")
```

##### 文本转语音 (同步)
```python
from fish_audio_sdk import Session, TTSRequest

session = Session("your_api_key")

# 基本TTS调用
with open("output.mp3", "wb") as f:
    for chunk in session.tts(TTSRequest(text="Hello, world!")):
        f.write(chunk)
```

##### 文本转语音 (异步)
```python
import asyncio
import aiofiles
from fish_audio_sdk import Session, TTSRequest

async def main():
    session = Session("your_api_key")
    async with aiofiles.open("output.mp3", "wb") as f:
        async for chunk in session.tts.awaitable(TTSRequest(text="Hello, world!")):
            await f.write(chunk)

asyncio.run(main())
```

##### 使用参考音频进行TTS
```python
from fish_audio_sdk import TTSRequest, ReferenceAudio

# 使用参考模型ID
request = TTSRequest(
    text="Hello, world!",
    reference_id="your_model_id"
)

# 使用直接的参考音频
request = TTSRequest(
    text="Hello, world!",
    references=[
        ReferenceAudio(
            audio=audio_file.read(),
            text="reference audio text"
        )
    ]
)
```

##### 模型管理

###### 获取模型列表
```python
# 同步调用
models = session.list_models()
print(models)

# 异步调用
async def main():
    models = await session.list_models.awaitable()
    print(models)
```

###### 创建模型
```python
from fish_audio_sdk import CreateModelRequest

# 创建新模型
model_request = CreateModelRequest(
    type="tts",
    title="My Voice Model",
    train_mode="fast",
    voices=["path/to/voice1.wav", "path/to/voice2.wav"],
    visibility="public",
    description="My custom voice model"
)

model = session.create_model(model_request)
print(f"Created model: {model._id}")
```

###### 获取模型详情
```python
# 获取特定模型
model = session.get_model("model_id")
print(model)
```

###### 删除模型
```python
# 删除模型
session.delete_model("model_id")
print("Model deleted successfully")
```

##### 高级TTS参数
```python
from fish_audio_sdk import TTSRequest, Prosody

request = TTSRequest(
    text="Hello, world!",
    temperature=0.7,        # 控制随机性 (0.0-1.0)
    top_p=0.9,             # 控制多样性 (0.0-1.0)
    chunk_length=200,       # 分块长度 (100-300)
    normalize=True,         # 是否标准化
    format="mp3",          # 输出格式: wav, pcm, mp3, opus
    sample_rate=44100,     # 采样率
    mp3_bitrate=128,       # MP3比特率: 64, 128, 192
    opus_bitrate=32,       # Opus比特率: -1000, 24, 32, 48, 64
    latency="normal",      # 延迟模式: normal, balanced
    prosody=Prosody(       # 韵律控制
        speed=1.0,
        pitch=0.0
    )
)
```

##### 错误处理
```python
from fish_audio_sdk import Session, TTSRequest
from fish_audio_sdk.exceptions import APIError

session = Session("your_api_key")

try:
    with open("output.mp3", "wb") as f:
        for chunk in session.tts(TTSRequest(text="Hello, world!")):
            f.write(chunk)
except APIError as e:
    print(f"API Error: {e.message}")
    print(f"Error Code: {e.code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

#### 完整示例
```python
import asyncio
from fish_audio_sdk import Session, TTSRequest, ReferenceAudio

async def main():
    # 初始化会话
    session = Session("your_api_key")
    
    try:
        # 获取模型列表
        models = await session.list_models.awaitable()
        print(f"Available models: {len(models.total)}")
        
        # 使用参考音频进行TTS
        tts_request = TTSRequest(
            text="这是一个使用Fish Audio SDK的示例。",
            temperature=0.8,
            format="mp3",
            chunk_length=200
        )
        
        # 保存音频文件
        async with aiofiles.open("example_output.mp3", "wb") as f:
            async for chunk in session.tts.awaitable(tts_request):
                await f.write(chunk)
        
        print("TTS completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

# 运行示例
if __name__ == "__main__":
    asyncio.run(main())
```





### 其他工具
- JavaScript SDK: `npm install voice-ai-sdk`
- cURL示例可参考各接口的请求示例

## 更新日志

- v1.0.0: 初始版本发布
- v1.1.0: 新增模型管理功能
- v1.2.0: 优化钱包API响应格式







