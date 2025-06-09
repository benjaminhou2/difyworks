# Dify 官方资源汇总

## 🚀 快速配置检查清单

> **在开始使用前，请确认以下关键参数:**

### ⚠️ 你需要自己获取和配置的参数
- [ ] **DIFY_API_KEY** 🔴 - 从Dify平台获取API密钥
- [ ] **DIFY_APP_TYPE** 🔴 - 根据你创建的应用类型设置
- [ ] **INPUTS** 🔴 - 根据应用定义设置输入变量

### ✅ 项目已经配置好的参数
- [x] **DIFY_API_BASE** - 默认使用官方云服务
- [x] **TIMEOUT** - 30秒超时时间
- [x] **MAX_RETRIES** - 3次重试
- [x] **RESPONSE_MODE** - 流式响应
- [x] **项目结构** - 完整的目录和文件结构
- [x] **开发规范** - Cursor规则和代码规范
- [x] **文档链接** - 所有官方文档资源

### 🔧 可选的个性化配置
- [ ] **USER_ID** - 自定义用户标识
- [ ] **DIFY_API_BASE** - 如果使用自部署服务
- [ ] **CONVERSATION_ID** - 系统自动生成，无需预配置

---

## 📚 官方文档

### 核心文档
- **产品简介**: https://docs.dify.ai/zh-hans/introduction
- **快速开始**: https://docs.dify.ai/zh-hans/getting-started
- **特性与规格**: https://docs.dify.ai/zh-hans/getting-started/readme/features-and-specifications

### 应用开发
- **构建应用**: https://docs.dify.ai/zh-hans/guides/application-orchestration
- **工作流**: https://docs.dify.ai/zh-hans/guides/workflow
- **知识库**: https://docs.dify.ai/zh-hans/guides/knowledge-base
- **工具集成**: https://docs.dify.ai/zh-hans/guides/tools

### API开发
- **API访问**: https://docs.dify.ai/zh-hans/guides/application-publishing/developing-with-apis
- **SDK使用**: https://docs.dify.ai/zh-hans/api/sdk
- **Webhook**: https://docs.dify.ai/zh-hans/guides/application-publishing/webhook

### 模型集成
- **模型供应商列表**: https://docs.dify.ai/zh-hans/getting-started/readme/model-providers
- **模型接入**: https://docs.dify.ai/zh-hans/guides/model-configuration
- **自定义模型**: https://docs.dify.ai/zh-hans/development/models-integration

## 🔧 部署与运维

### 部署指南
- **云服务**: https://docs.dify.ai/zh-hans/getting-started/cloud
- **社区版部署**: https://docs.dify.ai/zh-hans/getting-started/install-self-hosted
- **Docker部署**: https://docs.dify.ai/zh-hans/getting-started/install-self-hosted/docker-compose
- **环境变量**: https://docs.dify.ai/zh-hans/getting-started/install-self-hosted/environments

### 监控运维
- **应用监测**: https://docs.dify.ai/zh-hans/guides/monitoring
- **日志管理**: https://docs.dify.ai/zh-hans/guides/monitoring/log-analysis
- **性能优化**: https://docs.dify.ai/zh-hans/guides/monitoring/tracing

## 🛠 开发者资源

### 插件开发
- **插件简介**: https://docs.dify.ai/zh-hans/plugins/introduction
- **快速开始**: https://docs.dify.ai/zh-hans/plugins/quick-start
- **接口规范**: https://docs.dify.ai/zh-hans/plugins/schema-specification
- **最佳实践**: https://docs.dify.ai/zh-hans/plugins/best-practice

### 后端开发
- **后端架构**: https://docs.dify.ai/zh-hans/development/backend
- **DifySandbox**: https://docs.dify.ai/zh-hans/development/sandbox
- **迁移指南**: https://docs.dify.ai/zh-hans/development/migration

## 🎯 实战案例

### 应用案例
- **微信机器人**: https://docs.dify.ai/zh-hans/learn-more/use-cases/dify-on-wechat
- **企业智能客服**: https://docs.dify.ai/zh-hans/learn-more/use-cases/build-an-notion-ai-assistant
- **Slack机器人**: https://docs.dify.ai/zh-hans/learn-more/use-cases/create-an-ai-chatbot-with-business-data-in-minutes
- **QQ群机器人**: https://docs.dify.ai/zh-hans/learn-more/use-cases/how-to-quickly-access-dify-chatbot-in-qq-wechat-lark-dingtalk

### 教程系列
- **初级教程**: https://docs.dify.ai/zh-hans/workshop/basic
- **中级教程**: https://docs.dify.ai/zh-hans/workshop/intermediate
- **动手实验室**: https://docs.dify.ai/zh-hans/workshop

## 🌐 社区资源

### 官方渠道
- **GitHub**: https://github.com/langgenius/dify
- **官网**: https://dify.ai
- **博客**: https://docs.dify.ai/blog
- **Discord社区**: https://discord.gg/FngNHpbcY7

### 获取支持
- **问题反馈**: https://github.com/langgenius/dify/issues
- **功能请求**: https://github.com/langgenius/dify/discussions
- **技术支持**: https://docs.dify.ai/zh-hans/community/support

## 📖 常用API端点

### 基础端点
```
# Dify Cloud
API Base: https://api.dify.ai/v1

# 自部署
API Base: http://your-domain/v1
```

### 常用接口详解

#### 💬 聊天消息接口 `/chat-messages`
**用途**: 与聊天助手或智能助手进行对话  
**支持应用类型**: `chatbot`, `agent`  
**请求方法**: POST  

**必需参数**:
- `user` (string): 用户标识符
- `query` (string): 用户输入的问题或消息

**可选参数**:
- `inputs` (object): 应用定义的输入变量
- `response_mode` (string): 响应模式 (`blocking` 或 `streaming`)
- `conversation_id` (string): 会话ID，用于多轮对话
- `files` (array): 上传的文件列表

**获取参数方法**:
1. 在Dify应用页面点击"访问API"
2. 查看"聊天消息API"部分的参数说明
3. 复制示例代码中的参数结构

#### 📝 文本生成接口 `/completion-messages`
**用途**: 生成文本内容，如文章、摘要等  
**支持应用类型**: `completion`  
**请求方法**: POST  

**必需参数**:
- `user` (string): 用户标识符
- `inputs` (object): 输入变量，根据应用配置而定

**可选参数**:
- `response_mode` (string): 响应模式
- `files` (array): 相关文件

#### ⚙️ 工作流执行接口 `/workflows/run`
**用途**: 执行复杂的工作流程  
**支持应用类型**: `workflow`  
**请求方法**: POST  

**必需参数**:
- `user` (string): 用户标识符
- `inputs` (object): 工作流输入变量

**可选参数**:
- `response_mode` (string): 响应模式
- `files` (array): 输入文件

**获取inputs参数**:
1. 在工作流应用中点击"访问API"
2. 查看"输入变量"部分
3. 根据变量名称构建inputs对象

#### 📊 知识库搜索接口 `/datasets/{dataset_id}/documents`
**用途**: 搜索知识库中的文档  
**请求方法**: GET  

**路径参数**:
- `dataset_id` (string): 知识库ID

**查询参数**:
- `query` (string): 搜索关键词
- `limit` (integer): 返回结果数量限制

**获取dataset_id**:
1. 在Dify知识库页面
2. 点击目标知识库
3. 在URL中查看知识库ID

#### 📱 应用信息接口 `/apps/{app_id}`
**用途**: 获取应用基本信息  
**请求方法**: GET  

**路径参数**:
- `app_id` (string): 应用ID

**获取app_id**:
1. 在应用列表页面查看应用URL
2. 或在"访问API"页面的示例代码中查看

## 🔑 重要配置参数详解

> 💡 **配置状态说明**:
> - ✅ **已配置**: Cursor/项目已经默认设置好，可直接使用
> - ⚠️ **需要确认**: 需要你根据实际情况填写具体值
> - 🔧 **可选配置**: 根据需要进行个性化调整

### 🌐 API基础配置

#### DIFY_API_BASE (API服务器地址) 🔧
**配置状态**: 🔧 **可选配置** - 项目已设置默认值，如使用官方云服务可不修改  
**用途**: 指定Dify API的服务器地址  
**格式**: URL地址  
**默认值**: `https://api.dify.ai/v1` (Dify官方云服务)  
**获取方法**:
- **Dify Cloud**: `https://api.dify.ai/v1` ← **已在项目中配置**
- **自部署**: `http://your-domain/v1` 或 `https://your-domain/v1` ← **需要你修改**

**示例**:
```bash
# 使用官方云服务
DIFY_API_BASE="https://api.dify.ai/v1"

# 使用自部署服务
DIFY_API_BASE="http://localhost:5001/v1"
DIFY_API_BASE="https://dify.yourcompany.com/v1"
```

#### DIFY_API_KEY (API密钥) ⚠️
**配置状态**: ⚠️ **需要确认** - **这是你必须自己获取并填写的重要参数**  
**用途**: 验证身份，访问特定Dify应用的凭证  
**格式**: `app-` 开头的字符串  
**重要性**: 🔴 **必需参数** - 没有此参数无法调用API  
**获取步骤**:
1. 登录 [Dify官网](https://dify.ai) 或你的自部署实例
2. 进入 "工作室" 页面
3. 选择或创建一个应用
4. 点击左侧菜单的 "访问 API"
5. 点击 "API密钥" 按钮
6. 点击 "创建密钥"
7. 复制生成的密钥

**示例**:
```bash
DIFY_API_KEY="app-1234567890abcdef"
```

**⚠️ 安全提醒**:
- 密钥具有应用级别的权限
- 不要将密钥提交到版本控制
- 定期轮换密钥以提高安全性

#### DIFY_APP_TYPE (应用类型) ⚠️
**配置状态**: ⚠️ **需要确认** - **必须根据你创建的Dify应用类型来设置**  
**用途**: 指定调用的Dify应用类型，影响API调用方式  
**默认值**: `chatbot` (项目中已设置，但你需要根据实际应用修改)  
**重要性**: 🔴 **必需参数** - 类型错误会导致API调用失败  
**可选值**:

| 值 | 应用类型 | API端点 | 用途 |
|---|---------|---------|------|
| `chatbot` | 聊天助手 | `/chat-messages` | 基础对话功能 |
| `agent` | 智能助手 | `/chat-messages` | 工具调用和推理 |
| `workflow` | 工作流 | `/workflows/run` | 复杂业务流程 |
| `completion` | 文本生成 | `/completion-messages` | 文本补全生成 |

**获取方法**:
1. 在Dify应用列表中查看应用图标
2. 或在应用编辑页面顶部查看应用类型

### 🔧 高级配置参数

#### TIMEOUT (超时时间) ✅
**配置状态**: ✅ **已配置** - 项目已设置合理默认值，通常无需修改  
**用途**: API请求的超时时间（秒）  
**默认值**: 30秒 ← **已在项目中配置**  
**建议值**: 
- 简单对话: 10-30秒 ← **当前设置适用**
- 复杂工作流: 60-300秒 ← **如需要可调整**
- 大文件处理: 300-600秒 ← **如需要可调整**

```bash
TIMEOUT=30
```

#### MAX_RETRIES (最大重试次数) ✅
**配置状态**: ✅ **已配置** - 项目已设置合理默认值，通常无需修改  
**用途**: 当API请求失败时的重试次数  
**默认值**: 3次 ← **已在项目中配置**  
**建议值**: 1-5次 ← **当前设置在合理范围内**

```bash
MAX_RETRIES=3
```

#### RESPONSE_MODE (响应模式) ✅
**配置状态**: ✅ **已配置** - 项目默认设置为流式响应，可根据需要调整  
**用途**: 控制API响应的方式  
**默认值**: `streaming` ← **已在项目中配置**  
**可选值**:
- `blocking`: 阻塞式，等待完整响应 ← **适合简单同步调用**
- `streaming`: 流式，实时返回响应 ← **当前设置，适合实时交互**

```bash
RESPONSE_MODE="streaming"
```

### 🎯 应用特定配置

#### USER_ID (用户标识) 🔧
**配置状态**: 🔧 **可选配置** - 项目已设置默认值，可根据业务需要自定义  
**用途**: 标识API调用的用户，用于会话管理和日志追踪  
**格式**: 字符串，建议使用唯一标识符  
**默认值**: `user-12345` ← **已在项目中配置**  
**示例**:
```bash
USER_ID="user-12345"
USER_ID="session-${timestamp}"
```

#### CONVERSATION_ID (会话ID) 🔧
**配置状态**: 🔧 **可选配置** - 系统自动生成，无需预先配置  
**用途**: 维持多轮对话的上下文  
**获取方法**: 首次调用聊天API时自动生成 ← **系统自动处理**  
**使用场景**: 需要连续对话时传入此ID ← **由应用逻辑决定**

#### INPUTS (输入变量) ⚠️
**配置状态**: ⚠️ **需要确认** - **必须根据你的Dify应用定义来设置**  
**用途**: 传递给Dify应用的变量  
**格式**: JSON对象  
**重要性**: 🔴 **关键参数** - 应用定义了什么变量就必须传什么  
**获取方法**: 在Dify应用的"发布 -> 访问API"页面查看所需输入变量 ← **你需要查看并记录**

### 📝 完整配置示例

#### 环境变量文件 (.env)
```bash
# ===================
# Dify API 基础配置
# ===================
DIFY_API_BASE="https://api.dify.ai/v1"
DIFY_API_KEY="app-your-api-key-here"
DIFY_APP_TYPE="chatbot"

# ===================
# 连接配置
# ===================
TIMEOUT=30
MAX_RETRIES=3
RESPONSE_MODE="streaming"

# ===================
# 用户配置
# ===================
USER_ID="user-12345"
DEFAULT_LANGUAGE="zh-hans"

# ===================
# 日志配置
# ===================
LOG_LEVEL="INFO"
LOG_FILE="logs/dify.log"

# ===================
# 项目配置
# ===================
PROJECT_NAME="DifyWorks"
ENVIRONMENT="development"
```

#### YAML配置文件
```yaml
dify:
  # API基础设置
  api_base: "https://api.dify.ai/v1"
  api_key: "app-xxxxxxxxxxxxx"
  app_type: "chatbot"
  
  # 连接设置
  timeout: 30
  max_retries: 3
  response_mode: "streaming"
  
  # 用户设置
  user_id: "user-12345"
  language: "zh-hans"
  
  # 应用特定设置
  inputs:
    query: ""
    context: ""
  
  # 高级设置
  conversation:
    auto_generate_title: true
    max_tokens: 4000
    temperature: 0.7
```

#### Python配置类
```python
import os
from typing import Dict, Any, Optional

class DifyConfig:
    def __init__(self):
        # 基础配置
        self.api_base = os.getenv('DIFY_API_BASE', 'https://api.dify.ai/v1')
        self.api_key = os.getenv('DIFY_API_KEY')
        self.app_type = os.getenv('DIFY_APP_TYPE', 'chatbot')
        
        # 连接配置
        self.timeout = int(os.getenv('TIMEOUT', '30'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.response_mode = os.getenv('RESPONSE_MODE', 'streaming')
        
        # 用户配置
        self.user_id = os.getenv('USER_ID', 'default-user')
        
        # 验证必需参数
        if not self.api_key:
            raise ValueError("DIFY_API_KEY is required")
    
    def get_headers(self) -> Dict[str, str]:
        """获取API请求头"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
    
    def get_base_payload(self) -> Dict[str, Any]:
        """获取基础请求载荷"""
        return {
            'user': self.user_id,
            'response_mode': self.response_mode,
        }
```

### 🔍 参数验证检查清单

使用前请确认：

- [ ] **API密钥**: 是否以 `app-` 开头
- [ ] **API地址**: 是否以 `/v1` 结尾
- [ ] **应用类型**: 是否与实际应用匹配
- [ ] **网络连接**: 是否能访问API地址
- [ ] **权限设置**: API密钥是否有足够权限
- [ ] **配额限制**: 是否超出API调用限制

### 🚨 常见配置错误

1. **密钥错误**: 确保复制完整的API密钥
2. **地址错误**: 自部署时确认端口和协议
3. **类型不匹配**: 应用类型与实际应用不符
4. **网络问题**: 防火墙或代理设置
5. **编码问题**: 确保配置文件使用UTF-8编码

### 📋 参数获取详细步骤指南

#### 🔑 获取API密钥的完整流程

1. **访问Dify平台**
   ```
   云服务: https://dify.ai
   自部署: http://your-domain
   ```

2. **创建或选择应用**
   - 点击右上角 "工作室"
   - 选择已有应用或点击 "创建空白应用"
   - 填写应用信息并保存

3. **获取API凭证**
   - 在应用页面，点击左侧菜单 "发布" → "访问API"
   - 在API访问页面，点击右上角 "API密钥"
   - 点击 "创建密钥" 按钮
   - 为密钥起个名称（如：生产环境、测试环境）
   - 复制生成的密钥（格式：`app-xxxxxxxxxx`）

4. **查看API端点**
   - 在同一页面可以看到API服务器地址
   - 云服务固定为：`https://api.dify.ai/v1`
   - 自部署需要确认你的域名和端口

#### 🎯 确定应用类型的方法

**方法一：应用列表查看**
- 在工作室页面查看应用图标：
  - 💬 对话图标 = `chatbot` (聊天助手)
  - 🤖 机器人图标 = `agent` (智能助手) 
  - ⚙️ 齿轮图标 = `workflow` (工作流)
  - 📝 文档图标 = `completion` (文本生成)

**方法二：应用编辑页面**
- 进入应用编辑页面
- 顶部面包屑导航显示应用类型
- 如：工作室 > 聊天助手 > 应用名称

#### 📊 获取输入变量 (inputs) 参数

**对于聊天助手/智能助手**:
```json
{
  "inputs": {},  // 大多数情况为空对象
  "query": "用户输入的问题",
  "user": "user-123"
}
```

**对于工作流应用**:
1. 在工作流编辑页面查看 "开始" 节点
2. 记录所有输入变量名称
3. 构建inputs对象：
```json
{
  "inputs": {
    "query": "用户问题",
    "language": "zh-hans",
    "context": "额外上下文"
  },
  "user": "user-123"
}
```

**对于文本生成应用**:
1. 在提示词编排页面查看变量
2. 所有 `{{变量名}}` 都需要在inputs中提供：
```json
{
  "inputs": {
    "topic": "文章主题",
    "style": "写作风格",
    "length": "文章长度"
  },
  "user": "user-123"
}
```

#### 🔍 调试和验证参数

**使用curl测试**:
```bash
# 测试聊天接口
curl -X POST "https://api.dify.ai/v1/chat-messages" \
  -H "Authorization: Bearer app-your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {},
    "query": "Hello",
    "response_mode": "blocking",
    "user": "test-user"
  }'

# 测试工作流接口
curl -X POST "https://api.dify.ai/v1/workflows/run" \
  -H "Authorization: Bearer app-your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": {"query": "测试输入"},
    "response_mode": "blocking",
    "user": "test-user"
  }'
```

**Python测试脚本**:
```python
import requests
import json

def test_dify_api():
    api_base = "https://api.dify.ai/v1"
    api_key = "app-your-key-here"
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    # 测试数据
    data = {
        "inputs": {},
        "query": "测试消息",
        "response_mode": "blocking",
        "user": "test-user"
    }
    
    try:
        response = requests.post(
            f"{api_base}/chat-messages",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ API调用成功")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ API调用失败: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")

# 运行测试
if __name__ == "__main__":
    test_dify_api()
```

#### 🎯 常用参数组合示例

**基础聊天**:
```json
{
  "inputs": {},
  "query": "你好，请介绍一下你自己",
  "response_mode": "streaming",
  "user": "user-123"
}
```

**带上下文的聊天**:
```json
{
  "inputs": {
    "context": "用户是一个Python开发者"
  },
  "query": "如何优化代码性能？",
  "response_mode": "streaming",
  "conversation_id": "conv-456",
  "user": "user-123"
}
```

**工作流执行**:
```json
{
  "inputs": {
    "document": "需要分析的文档内容",
    "analysis_type": "sentiment",
    "output_format": "json"
  },
  "response_mode": "blocking",
  "user": "user-123"
}
```

**文档上传**:
```json
{
  "inputs": {},
  "query": "请分析这个文档",
  "files": [
    {
      "type": "document",
      "transfer_method": "remote_url",
      "url": "https://example.com/document.pdf"
    }
  ],
  "response_mode": "streaming",
  "user": "user-123"
}
```

---

## 🎯 配置优先级和行动建议

### 第一优先级 (必须完成) 🔴
1. **获取API密钥** - 登录Dify平台，创建应用，获取API密钥
2. **确定应用类型** - 记录你创建的应用类型（chatbot/agent/workflow/completion）
3. **查看输入变量** - 在应用的API访问页面查看需要的输入参数

### 第二优先级 (建议配置) 🟡
1. **自定义用户ID** - 设置有意义的用户标识符
2. **调整超时时间** - 根据应用复杂度调整超时设置
3. **选择响应模式** - 根据使用场景选择blocking或streaming

### 第三优先级 (可选优化) 🟢
1. **自部署配置** - 如果使用自己的Dify服务器
2. **日志配置** - 配置详细的日志记录
3. **环境变量** - 设置不同环境的配置

### 📝 配置完成检查
完成配置后，使用以下方式验证：
```bash
# 检查环境变量
echo $DIFY_API_KEY
echo $DIFY_APP_TYPE

# 运行测试脚本
python test_dify_api.py

# 查看项目配置
cat .env
```

---

## 📌 更新日志

- **2024-06-09**: 创建资源汇总文档，添加配置状态标注
- **2024-06-09**: 补充详细的参数说明和获取方法
- **2024-06-09**: 添加配置优先级和检查清单
- 定期更新最新的API文档链接和功能介绍

> 💡 **提示**: 本文档会定期更新，建议收藏备用。当你需要查找Dify相关信息时，可以直接在这个文档中查找对应的官方链接。
> 
> 🎯 **重要**: 红色标记的参数是你必须自己配置的，绿色标记的参数项目已经配置好可直接使用！ 