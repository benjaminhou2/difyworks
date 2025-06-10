#!/bin/bash

# Dify 工作流自动校验脚本
# 版本: v1.0
# 作者: DifyWorks
# 用途: 自动校验 Dify 工作流 YAML 文件的兼容性和规范性

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ 错误: 请提供工作流文件路径${NC}"
    echo "用法: $0 <workflow_file.yml>"
    exit 1
fi

WORKFLOW_FILE="$1"

# 检查文件是否存在
if [ ! -f "$WORKFLOW_FILE" ]; then
    echo -e "${RED}❌ 错误: 文件不存在: $WORKFLOW_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 开始校验 Dify 工作流文件: $WORKFLOW_FILE${NC}"
echo "=================================================="

# 校验结果统计
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# 工具函数：记录检查结果
check_result() {
    local status=$1
    local message=$2
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    case $status in
        "pass")
            echo -e "${GREEN}✅ $message${NC}"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            ;;
        "fail")
            echo -e "${RED}❌ $message${NC}"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            ;;
        "warn")
            echo -e "${YELLOW}⚠️ $message${NC}"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            ;;
    esac
}

# 1. 节点类型兼容性校验
echo -e "\n${PURPLE}1️⃣ 节点类型兼容性校验${NC}"
echo "--------------------------------------"

# 支持的节点类型列表
SUPPORTED_TYPES="start|end|llm|if-else|code|template|http-request|tool|knowledge-retrieval|question-classifier|iteration|parameter-extractor"

# 检查是否使用了不支持的节点类型
INVALID_TYPES=$(grep -n "type:" "$WORKFLOW_FILE" | grep -v -E "($SUPPORTED_TYPES)" | grep -v "sourceType\|targetType")

if [ -z "$INVALID_TYPES" ]; then
    check_result "pass" "节点类型检查通过"
else
    check_result "fail" "发现不支持的节点类型:"
    echo "$INVALID_TYPES"
fi

# 检查节点类型拼写
MISSPELLED_TYPES=$(grep -n "type:" "$WORKFLOW_FILE" | grep -E "(strat|ned|llm-|ifelse|conde)")
if [ -z "$MISSPELLED_TYPES" ]; then
    check_result "pass" "节点类型拼写检查通过"
else
    check_result "fail" "发现节点类型拼写错误:"
    echo "$MISSPELLED_TYPES"
fi

# 2. 文件上传配置校验
echo -e "\n${PURPLE}2️⃣ 文件上传配置校验${NC}"
echo "--------------------------------------"

# 检查文件上传类型配置
if grep -q "type: file" "$WORKFLOW_FILE"; then
    check_result "pass" "使用了标准的 'type: file' 配置"
else
    if grep -q "type: files" "$WORKFLOW_FILE"; then
        check_result "warn" "使用了 'type: files'，建议使用 'type: file'"
    fi
fi

# 检查文件扩展名配置
if grep -q "allowed_file_extensions:" "$WORKFLOW_FILE"; then
    check_result "pass" "包含文件扩展名配置"
else
    if grep -q "type: file" "$WORKFLOW_FILE"; then
        check_result "warn" "文件上传节点缺少扩展名配置"
    fi
fi

# 检查变量名与类型匹配
MISMATCHED_FILES=$(grep -A 3 "variable: .*_files" "$WORKFLOW_FILE" | grep -B 3 "type: file" | grep "variable:")
if [ ! -z "$MISMATCHED_FILES" ]; then
    check_result "fail" "发现变量名与类型不匹配（复数变量名使用单数类型）:"
    echo "$MISMATCHED_FILES"
else
    check_result "pass" "变量名与文件类型匹配检查通过"
fi

# 检查 max_length 参数合理性
NULL_MAX_LENGTH=$(grep -n "max_length: null" "$WORKFLOW_FILE")
if [ ! -z "$NULL_MAX_LENGTH" ]; then
    check_result "fail" "发现 max_length 为 null 的配置，可能影响组件渲染:"
    echo "$NULL_MAX_LENGTH"
else
    check_result "pass" "max_length 参数配置检查通过"
fi

# 3. 模型能力匹配校验
echo -e "\n${PURPLE}3️⃣ 模型能力匹配校验${NC}"
echo "--------------------------------------"

# 检查是否使用支持视频的模型
if grep -q "gpt-4o" "$WORKFLOW_FILE"; then
    check_result "pass" "使用了 gpt-4o 支持视频分析"
elif grep -q "gpt-4-vision" "$WORKFLOW_FILE"; then
    check_result "pass" "使用了 gpt-4-vision 支持视觉分析"
else
    if grep -q "gpt-4-turbo" "$WORKFLOW_FILE"; then
        check_result "warn" "使用了 gpt-4-turbo，建议升级到 gpt-4o 以支持视频分析"
    fi
fi

# 检查视觉功能配置
VISION_ENABLED=$(grep -A 2 "vision:" "$WORKFLOW_FILE" | grep "enabled: true" | wc -l)
LLM_NODES=$(grep -c "type: llm" "$WORKFLOW_FILE")

if [ "$VISION_ENABLED" -gt 0 ]; then
    check_result "pass" "已启用视觉功能 ($VISION_ENABLED 个节点)"
else
    if [ "$LLM_NODES" -gt 0 ]; then
        check_result "warn" "存在 LLM 节点但未启用视觉功能"
    fi
fi

# 4. 变量引用规范校验
echo -e "\n${PURPLE}4️⃣ 变量引用规范校验${NC}"
echo "--------------------------------------"

# 检查错误的变量引用语法
INVALID_REFS=$(grep -n "{{.*}}" "$WORKFLOW_FILE" | grep -v "{{#.*#}}")
if [ -z "$INVALID_REFS" ]; then
    check_result "pass" "变量引用语法检查通过"
else
    check_result "fail" "发现错误的变量引用语法:"
    echo "$INVALID_REFS"
fi

# 检查变量引用的完整性
INCOMPLETE_REFS=$(grep -n "{{#.*}}" "$WORKFLOW_FILE" | grep -v "{{#.*#}}")
if [ ! -z "$INCOMPLETE_REFS" ]; then
    check_result "fail" "发现不完整的变量引用（缺少结束#）:"
    echo "$INCOMPLETE_REFS"
fi

# 5. 条件分支处理校验
echo -e "\n${PURPLE}5️⃣ 条件分支处理校验${NC}"
echo "--------------------------------------"

# 检查是否使用了不存在的聚合节点
AGGREGATOR_TYPES=$(grep -n "type: variable-aggregator\|type: data-merger\|type: aggregator" "$WORKFLOW_FILE")
if [ -z "$AGGREGATOR_TYPES" ]; then
    check_result "pass" "未使用不支持的聚合节点类型"
else
    check_result "fail" "发现不支持的聚合节点类型:"
    echo "$AGGREGATOR_TYPES"
fi

# 检查 if-else 节点配置
IF_ELSE_COUNT=$(grep -c "type: if-else" "$WORKFLOW_FILE")
if [ "$IF_ELSE_COUNT" -gt 0 ]; then
    check_result "pass" "包含 $IF_ELSE_COUNT 个条件判断节点"
    
    # 检查条件配置
    if grep -q "conditions:" "$WORKFLOW_FILE"; then
        check_result "pass" "条件判断节点包含条件配置"
    else
        check_result "fail" "条件判断节点缺少条件配置"
    fi
fi

# 6. 连接结构校验
echo -e "\n${PURPLE}6️⃣ 连接结构校验${NC}"
echo "--------------------------------------"

# 检查边连接配置
if grep -q "edges:" "$WORKFLOW_FILE"; then
    check_result "pass" "包含边连接配置"
    
    # 检查sourceType和targetType匹配
    INVALID_CONNECTIONS=$(grep -A 5 "sourceType:\|targetType:" "$WORKFLOW_FILE" | grep -E "sourceType: aggregator|targetType: aggregator")
    if [ -z "$INVALID_CONNECTIONS" ]; then
        check_result "pass" "连接类型检查通过"
    else
        check_result "fail" "发现不匹配的连接类型"
    fi
else
    check_result "fail" "缺少边连接配置"
fi

# 7. 文件结构校验
echo -e "\n${PURPLE}7️⃣ 文件结构校验${NC}"
echo "--------------------------------------"

# 检查必需的顶级字段
REQUIRED_FIELDS=("app:" "dependencies:" "kind:" "version:" "workflow:")
for field in "${REQUIRED_FIELDS[@]}"; do
    if grep -q "^$field" "$WORKFLOW_FILE"; then
        check_result "pass" "包含必需字段: $field"
    else
        check_result "fail" "缺少必需字段: $field"
    fi
done

# 检查模式设置
if grep -q "mode: workflow" "$WORKFLOW_FILE"; then
    check_result "pass" "模式设置为 workflow"
else
    check_result "fail" "模式未设置为 workflow"
fi

# 8. YAML 格式校验
echo -e "\n${PURPLE}8️⃣ YAML 格式校验${NC}"
echo "--------------------------------------"

# 检查YAML格式（如果安装了yamllint）
if command -v yamllint &> /dev/null; then
    if yamllint "$WORKFLOW_FILE" &> /dev/null; then
        check_result "pass" "YAML 格式校验通过"
    else
        check_result "fail" "YAML 格式错误，请检查语法"
        echo "运行以下命令查看详细错误:"
        echo "yamllint $WORKFLOW_FILE"
    fi
else
    check_result "warn" "未安装 yamllint，跳过 YAML 格式校验"
fi

# 9. 安全性检查
echo -e "\n${PURPLE}9️⃣ 安全性检查${NC}"
echo "--------------------------------------"

# 检查是否包含敏感信息
SENSITIVE_PATTERNS=("password|secret|token|key" "api_key|apikey" "credential")
for pattern in "${SENSITIVE_PATTERNS[@]}"; do
    SENSITIVE_FOUND=$(grep -i "$pattern" "$WORKFLOW_FILE" | grep -v "variable\|label")
    if [ ! -z "$SENSITIVE_FOUND" ]; then
        check_result "warn" "发现可能的敏感信息，请确认是否安全"
    fi
done

if [ -z "$(grep -i "password\|secret\|token\|key\|api_key\|apikey\|credential" "$WORKFLOW_FILE" | grep -v "variable\|label")" ]; then
    check_result "pass" "未发现明显的敏感信息"
fi

# 输出校验摘要
echo -e "\n${BLUE}📊 校验摘要${NC}"
echo "=================================================="
echo -e "总检查项: ${BLUE}$TOTAL_CHECKS${NC}"
echo -e "✅ 通过: ${GREEN}$PASSED_CHECKS${NC}"
echo -e "❌ 失败: ${RED}$FAILED_CHECKS${NC}"
echo -e "⚠️ 警告: ${YELLOW}$WARNING_CHECKS${NC}"

# 计算通过率
if [ "$TOTAL_CHECKS" -gt 0 ]; then
    PASS_RATE=$(( (PASSED_CHECKS * 100) / TOTAL_CHECKS ))
    echo -e "通过率: ${BLUE}$PASS_RATE%${NC}"
fi

# 给出最终建议
echo -e "\n${BLUE}💡 建议${NC}"
echo "=================================================="

if [ "$FAILED_CHECKS" -eq 0 ]; then
    if [ "$WARNING_CHECKS" -eq 0 ]; then
        echo -e "${GREEN}🎉 恭喜！工作流文件完全符合规范，可以导入 Dify！${NC}"
    else
        echo -e "${YELLOW}⚠️ 工作流基本符合规范，但有一些建议优化的地方。${NC}"
        echo -e "${YELLOW}建议处理警告项后再导入 Dify。${NC}"
    fi
else
    echo -e "${RED}❌ 发现 $FAILED_CHECKS 个错误，必须修复后才能正常导入 Dify。${NC}"
    echo -e "${RED}请参考 'Dify工作流校验规范.md' 文档进行修复。${NC}"
fi

echo -e "\n${BLUE}📚 相关文档${NC}"
echo "- Dify工作流校验规范.md"
echo "- https://docs.dify.ai/zh-hans/user-guide/workflow"

# 根据检查结果设置退出代码
if [ "$FAILED_CHECKS" -gt 0 ]; then
    exit 1
else
    exit 0
fi 