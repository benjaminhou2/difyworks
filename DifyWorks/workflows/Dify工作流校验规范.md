# Dify 工作流校验规范

## 📋 概述

本文档总结了在 Dify 工作流开发过程中遇到的关键问题和解决方案，形成系统性的校验标准。每次生成 Dify 工作流文件后，必须按照此规范进行全面校验，确保工作流能够正常导入和运行。

## 🔍 核心问题分类

### 1. 节点类型兼容性问题
### 2. 文件上传配置问题  
### 3. 模型能力匹配问题
### 4. 条件分支处理问题
### 5. 变量引用规范问题
### 6. 视觉功能配置问题

---

## 🛠️ 详细校验规范

### 1. 节点类型兼容性校验

#### ❌ 常见错误
```yaml
# 错误：使用不存在的节点类型
type: variable-aggregator  # 此节点类型不被Dify官方支持
type: data-processor      # 此节点类型不被Dify官方支持
type: custom-logic        # 此节点类型不被Dify官方支持
```

#### ✅ 正确标准
**Dify官方支持的节点类型（完整清单）**：
- `start` - 开始节点
- `end` - 结束节点  
- `llm` - LLM节点
- `if-else` - 条件判断节点
- `code` - 代码节点
- `template` - 模板节点
- `http-request` - HTTP请求节点
- `tool` - 工具节点
- `knowledge-retrieval` - 知识检索节点
- `question-classifier` - 问题分类节点
- `iteration` - 迭代节点
- `parameter-extractor` - 参数提取节点

#### 🔧 校验方法
```bash
# 检查是否使用了不支持的节点类型
grep -n "type:" your_workflow.yml | grep -v -E "(start|end|llm|if-else|code|template|http-request|tool|knowledge-retrieval|question-classifier|iteration|parameter-extractor)"
```

#### 📝 校验清单
- [ ] 所有节点类型都在官方支持清单中
- [ ] 没有使用自定义或第三方节点类型
- [ ] 节点类型拼写正确，无大小写错误

---

### 2. 文件上传配置校验

#### ❌ 常见错误
```yaml
# 错误：使用不兼容的文件类型定义
variables:
- type: files          # 在某些版本可能不兼容
- type: file_upload    # 错误的类型名称
- type: media          # 错误的类型名称
```

#### ✅ 正确标准
```yaml
# 正确：使用官方标准的文件上传配置
variables:
- label: 视频文件
  type: file           # 使用标准的file类型
  variable: video_files
  required: true
```

#### 🔧 校验方法
```bash
# 检查文件上传配置
grep -A 5 -B 5 "type: file" your_workflow.yml
```

#### 📝 校验清单
- [ ] 文件上传类型与变量名匹配（见下方匹配规则）
- [ ] 包含正确的 `allowed_file_types` 配置
- [ ] 包含正确的 `allowed_file_extensions` 配置
- [ ] 设置了合理的文件大小限制

#### 🔗 变量名与类型匹配规则
```yaml
# ✅ 正确匹配
- variable: video_file    # 单数变量名
  type: file             # 单数类型

- variable: video_files   # 复数变量名
  type: files            # 复数类型

# ❌ 错误匹配  
- variable: video_files   # 复数变量名
  type: file             # 单数类型 - 会导致上传失败

- variable: video_file    # 单数变量名
  type: files            # 复数类型 - 语义不一致
```

---

### 3. 模型能力匹配校验

#### ❌ 常见错误
```yaml
# 错误：使用不支持视频分析的模型
model:
  name: gpt-4-turbo      # 只支持静态图像，不支持视频
  name: gpt-3.5-turbo    # 不支持视觉功能
  name: claude-3-haiku   # 视频支持有限
```

#### ✅ 正确标准
```yaml
# 正确：使用支持视频分析的模型
model:
  name: gpt-4o           # 支持多模态视频分析
  provider: langgenius/openai/openai
vision:
  enabled: true          # 启用视觉功能
```

#### 🔧 校验方法
```bash
# 检查模型配置
grep -A 3 "model:" your_workflow.yml
grep -A 2 "vision:" your_workflow.yml
```

#### 📝 校验清单
- [ ] 视频分析任务使用 `gpt-4o` 或其他支持视频的模型
- [ ] 需要视觉分析的节点启用了 `vision: enabled: true`
- [ ] 模型provider配置正确
- [ ] 模型参数设置合理（temperature、max_tokens等）

---

### 4. 条件分支处理校验

#### ❌ 常见错误
```yaml
# 错误：添加不支持的聚合节点
- type: variable-aggregator    # 不存在的节点类型
- type: data-merger           # 不存在的节点类型
```

#### ✅ 正确标准
```yaml
# 正确：使用原生条件分支连接
edges:
- id: 1736412004000-1736412006000  # 长视频分析 -> 下游节点
  source: '1736412004000'
  target: '1736412006000'
- id: 1736412005000-1736412006000  # 短视频分析 -> 下游节点  
  source: '1736412005000'
  target: '1736412006000'

# 在下游节点中引用多个分支输出
prompt_template:
- role: system
  text: '基于分析结果：{{#1736412004000.text#}}{{#1736412005000.text#}}'
```

#### 🔧 校验方法
```bash
# 检查条件分支连接
grep -A 10 -B 5 "if-else" your_workflow.yml
grep -n "{{#.*text#}}" your_workflow.yml
```

#### 📝 校验清单
- [ ] 条件分支使用标准的 `if-else` 节点
- [ ] 分支输出正确连接到下游节点
- [ ] 下游节点能处理空值情况
- [ ] 变量引用语法正确

---

### 5. 变量引用规范校验

#### ❌ 常见错误
```yaml
# 错误的变量引用语法
text: '{{$1736412001000.video_files}}'     # 错误的$语法
text: '{{1736412001000.video_files}}'      # 缺少#符号
text: '{{#1736412001000.video_files}}'     # 缺少结束#
text: '{#1736412001000.video_files#}'      # 错误的大括号数量
```

#### ✅ 正确标准
```yaml
# 正确的变量引用语法
text: '{{#1736412001000.video_files#}}'    # 完整正确的语法
text: '{{#nodeId.fieldName#}}'             # 标准格式
```

#### 🔧 校验方法
```bash
# 检查变量引用语法
grep -n "{{.*}}" your_workflow.yml | grep -v "{{#.*#}}"
```

#### 📝 校验清单
- [ ] 所有变量引用使用 `{{#nodeId.field#}}` 格式
- [ ] 节点ID引用存在且正确
- [ ] 字段名称拼写正确
- [ ] 没有使用过时的语法格式

---

### 6. 视觉功能配置校验

#### ❌ 常见错误
```yaml
# 错误：需要分析视频但未启用视觉功能
vision:
  enabled: false         # 视频分析节点必须启用
# 或完全缺少vision配置
```

#### ✅ 正确标准
```yaml
# 正确：视频/图像分析节点配置
vision:
  enabled: true          # 明确启用视觉功能
```

#### 🔧 校验方法
```bash
# 检查视觉功能配置
grep -A 2 -B 2 "vision:" your_workflow.yml
```

#### 📝 校验清单
- [ ] 需要分析视频/图像的LLM节点启用了vision
- [ ] 基本信息分析节点启用了vision
- [ ] 视觉分析节点启用了vision
- [ ] 其他相关分析节点根据需要启用了vision

---

### 7. 连接结构校验

#### ❌ 常见错误
```yaml
# 错误：不匹配的连接类型
edges:
- data:
    sourceType: llm
    targetType: aggregator  # 目标类型不存在
```

#### ✅ 正确标准
```yaml
# 正确：匹配的连接配置
edges:
- data:
    sourceType: llm       # 源节点类型
    targetType: llm       # 目标节点类型匹配实际节点
  source: '1736412004000' # 源节点ID存在
  target: '1736412006000' # 目标节点ID存在
```

#### 🔧 校验方法
```bash
# 检查连接结构
grep -A 5 "edges:" your_workflow.yml
```

#### 📝 校验清单
- [ ] 所有edge的sourceType和targetType与实际节点类型匹配
- [ ] 所有source和target ID在nodes中存在
- [ ] 连接形成有效的工作流路径
- [ ] 没有孤立或无法到达的节点

---

### 8. 文件结构校验

#### ✅ 必需的顶级结构
```yaml
app:                    # 应用配置
  description: ""       # 应用描述
  icon: ""             # 应用图标
  mode: workflow       # 模式必须是workflow
  name: ""             # 应用名称

dependencies:           # 依赖配置
- type: marketplace    # 市场依赖类型

kind: app              # 资源类型
version: 0.3.0         # 版本号

workflow:              # 工作流配置
  features:            # 功能配置
  graph:               # 图配置
    edges: []          # 连接配置
    nodes: []          # 节点配置
```

#### 📝 校验清单
- [ ] 包含所有必需的顶级字段
- [ ] version字段与Dify版本兼容
- [ ] mode设置为workflow
- [ ] 依赖配置正确

---

## 🚀 完整校验流程

### 第一步：自动化校验
```bash
#!/bin/bash
# Dify工作流自动校验脚本

WORKFLOW_FILE="$1"

echo "🔍 开始校验 Dify 工作流文件: $WORKFLOW_FILE"

# 1. 节点类型校验
echo "1️⃣ 检查节点类型..."
INVALID_TYPES=$(grep -n "type:" "$WORKFLOW_FILE" | grep -v -E "(start|end|llm|if-else|code|template|http-request|tool)")
if [ ! -z "$INVALID_TYPES" ]; then
    echo "❌ 发现不支持的节点类型:"
    echo "$INVALID_TYPES"
else
    echo "✅ 节点类型检查通过"
fi

# 2. 变量引用校验
echo "2️⃣ 检查变量引用语法..."
INVALID_REFS=$(grep -n "{{.*}}" "$WORKFLOW_FILE" | grep -v "{{#.*#}}")
if [ ! -z "$INVALID_REFS" ]; then
    echo "❌ 发现错误的变量引用语法:"
    echo "$INVALID_REFS"
else
    echo "✅ 变量引用语法检查通过"
fi

# 3. 模型配置校验
echo "3️⃣ 检查模型配置..."
grep -q "gpt-4o\|gpt-4-vision" "$WORKFLOW_FILE"
if [ $? -eq 0 ]; then
    echo "✅ 使用了支持视频的模型"
else
    echo "⚠️ 建议使用 gpt-4o 等支持视频分析的模型"
fi

echo "🎉 自动校验完成！"
```

### 第二步：手动校验
1. **功能完整性检查**
   - [ ] 工作流逻辑符合需求
   - [ ] 所有分支路径都有效
   - [ ] 输出变量配置正确

2. **性能优化检查**  
   - [ ] 模型参数设置合理
   - [ ] 提示词长度适中
   - [ ] 避免不必要的重复计算

3. **用户体验检查**
   - [ ] 错误处理机制完善
   - [ ] 提示信息清晰友好
   - [ ] 响应时间在可接受范围

### 第三步：测试验证
1. **导入测试**
   - [ ] 能成功导入到Dify平台
   - [ ] 所有节点正确加载
   - [ ] 没有配置错误提示

2. **功能测试**
   - [ ] 使用真实数据测试工作流
   - [ ] 验证每个节点的输出
   - [ ] 确认最终结果符合预期

---

## 📚 参考资源

### 官方文档
- [Dify 工作流文档](https://docs.dify.ai/zh-hans/user-guide/workflow)
- [Dify 节点类型说明](https://docs.dify.ai/zh-hans/user-guide/workflow/node)

### 常用检查命令
```bash
# 检查文件格式
yamllint your_workflow.yml

# 检查节点类型
grep -n "type:" your_workflow.yml

# 检查变量引用  
grep -n "{{.*}}" your_workflow.yml

# 检查模型配置
grep -A 3 "model:" your_workflow.yml
```

---

## 📝 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v1.0 | 2024-01-09 | 初始版本，基于短视频分析工作流问题总结 |

---

**校验规范版本**: v1.0  
**适用范围**: Dify v0.3.0+ 工作流文件  
**维护状态**: 活跃维护  
**反馈渠道**: 遇到新问题请及时更新此文档 