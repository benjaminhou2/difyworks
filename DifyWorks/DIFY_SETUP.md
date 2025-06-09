# Dify 快速设置指南

## 🚀 快速开始

这个文件帮助你快速配置和使用Dify相关功能。

### 1. Dify官方文档（已配置为Cursor知识库）

- **中文文档**: https://docs.dify.ai/zh-hans/introduction
- **API文档**: https://docs.dify.ai/zh-hans/guides/application-publishing/developing-with-apis
- **完整资源**: 查看 `docs/dify_resources.md`

### 2. 环境配置

#### 创建 .env 文件
```bash
# Dify API配置
DIFY_API_BASE=https://api.dify.ai/v1
DIFY_API_KEY=app-your-api-key-here
DIFY_APP_TYPE=chatbot

# 项目配置
PROJECT_NAME=DifyWorks
LOG_LEVEL=INFO
```

#### 安装依赖
```bash
# 基础依赖
pip install -r requirements.txt

# 开发依赖
pip install -r requirements-dev.txt
```

### 3. Dify应用类型

| 类型 | 配置值 | 用途 |
|------|--------|------|
| 聊天助手 | `chatbot` | 基础对话功能 |
| 智能助手 | `agent` | 工具调用和推理 |
| 工作流 | `workflow` | 复杂业务流程 |

### 4. 常用API调用示例

#### 聊天API
```python
import requests

url = "https://api.dify.ai/v1/chat-messages"
headers = {
    'Authorization': 'Bearer YOUR-API-KEY',
    'Content-Type': 'application/json',
}
data = {
    "inputs": {},
    "query": "你好，请介绍一下Dify",
    "response_mode": "blocking",
    "user": "user-123"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

#### 工作流API
```python
url = "https://api.dify.ai/v1/workflows/run"
data = {
    "inputs": {"query": "处理这个请求"},
    "response_mode": "blocking",
    "user": "user-123"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### 5. 项目中的配置使用

#### 配置类示例
```python
from src.utils.config import Config

# 加载配置
config = Config()

# 获取Dify配置
api_base = config.get('dify.api_base')
api_key = config.get('dify.api_key')
app_type = config.get('dify.app_type')
```

### 6. 集成到项目中

#### 在DifyWorks中使用
```python
from src.main import DifyWorks

# 初始化
dify = DifyWorks()

# 创建工作流
workflow = dify.create_workflow("数据处理流程", "自动化数据处理")

# 运行工作流
result = dify.run_workflow("数据处理流程")
```

### 7. 常见问题解决

#### API密钥获取
1. 登录 https://dify.ai
2. 创建应用
3. 在 "访问API" 页面获取密钥

#### 错误排查
- 检查API密钥是否正确
- 确认应用类型配置
- 查看API限制和配额

### 8. Cursor集成配置

项目已经配置好Cursor的知识库集成：

- **规则文件**: `.cursor/rules`
- **工作区配置**: `.vscode/settings.json`
- **资源文档**: `docs/dify_resources.md`

当你在Cursor中工作时，它会自动参考这些Dify文档和配置。

### 9. 提示词管理

项目提供了专门的提示词管理：

- **提示词目录**: `prompts/`
- **使用指南**: `prompts/README.md`
- **分类管理**: 工作、编程、学习、创意

---

## 📞 获取帮助

- **官方文档**: https://docs.dify.ai
- **GitHub Issues**: https://github.com/langgenius/dify/issues
- **Discord社区**: https://discord.gg/FngNHpbcY7

> 💡 **提示**: 这个文件已经配置为Cursor的上下文文件，你随时可以通过 `@DIFY_SETUP.md` 来引用这些配置信息。