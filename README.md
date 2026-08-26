# MCode

基于终端的 AI 编程助手。支持多种 LLM 模型，具备文件读写、命令执行、代码搜索等能力，帮助你高效完成编程任务。

## 功能特性

### 核心能力

- **多模型支持**: Anthropic Claude、OpenAI、OpenAI 兼容 API（如 DeepSeek、GLM 等）
- **流式响应**: 实时逐 token 输出，即时查看生成结果
- **工具调用**: 读写文件、执行 Shell 命令、搜索代码
- **思考模式**: 支持 Claude extended thinking，展示推理过程

### 安全机制

- **权限系统**: 四种模式可选（default、acceptEdits、plan、bypassPermissions）
- **路径沙箱**: 限制文件操作范围，防止误操作
- **危险命令检测**: 自动识别并拦截高危命令
- **权限规则**: 支持用户级、项目级权限规则配置

### 扩展功能

- **MCP 集成**: 通过 Model Context Protocol 接入外部工具服务
- **技能系统**: 创建和分享可复用的提示词模板
- **Hook 系统**: 在工具执行前后插入自定义逻辑
- **多 Agent**: 支持 Fork 子 Agent 和团队协作模式

### 会话管理

- **上下文压缩**: 自动管理对话长度，避免超出 token 限制
- **会话持久化**: 保存历史会话，支持回溯
- **记忆系统**: 自动提取关键信息，跨会话记忆

## 安装

### 使用 pip

```bash
pip install mcode
```

### 使用 uv（推荐）

```bash
uv pip install mcode
```

### 从源码安装

```bash
git clone https://github.com/solitude-1107/Mcode.git
cd Mcode
uv pip install -e .
```

## 快速开始

### 1. 配置

复制配置示例并编辑：

```bash
cp .mcode/config.yaml.example .mcode/config.yaml
```

编辑 `.mcode/config.yaml`，填入你的 API Key：

```yaml
providers:
  - name: anthropic
    protocol: anthropic
    base_url: https://api.anthropic.com
    model: claude-sonnet-4-20250514
    api_key: "your-api-key-here"
```

或设置环境变量：

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### 2. 启动

```bash
mcode
```

### 3. 使用

直接输入问题或任务，MCode 会自动调用合适的工具完成：

```
> 帮我读取 main.py 文件并解释它的功能

> 在当前目录搜索所有 TODO 注释

> 创建一个简单的 HTTP 服务器
```

## 命令行参数

```bash
mcode [OPTIONS]

选项:
  --mode MODE          权限模式 (覆盖配置文件)
  -p PROMPT            非交互模式：执行提示词并输出结果
  --output-format TYPE  输出格式: text (默认) 或 stream-json
  --remote             远程模式：启动 WebSocket 服务器
```

### 示例

```bash
# 交互模式
mcode

# 指定权限模式
mcode --mode bypassPermissions

# 非交互模式
mcode -p "列出当前目录的所有 Python 文件"

# JSON 输出（适合脚本集成）
mcode -p "解释这段代码" --output-format stream-json

# 远程模式（浏览器访问 http://localhost:18888）
mcode --remote
```

## 内置工具

| 工具 | 说明 |
|------|------|
| `ReadFile` | 读取文件内容 |
| `WriteFile` | 写入文件 |
| `EditFile` | 编辑文件（精确替换） |
| `Bash` | 执行 Shell 命令 |
| `Glob` | 文件模式匹配搜索 |
| `Grep` | 内容搜索（正则支持） |
| `AskUser` | 向用户提问 |
| `Agent` | 调用子 Agent |
| `TaskCreate/Update/List` | 任务管理 |
| `TeamCreate/Delete` | 团队协作 |

## 内置命令

在交互模式下，以 `/` 开头输入命令：

| 命令 | 说明 |
|------|------|
| `/help` | 显示帮助 |
| `/clear` | 清空对话 |
| `/compact` | 压缩上下文 |
| `/session` | 会话管理 |
| `/memory` | 记忆管理 |
| `/permission` | 权限管理 |
| `/mcp` | MCP 服务器管理 |
| `/skill` | 技能管理 |
| `/sandbox` | 沙箱管理 |
| `/status` | 显示状态 |

## 配置说明

配置文件支持两个位置：

- **全局配置**: `~/.mcode/config.yaml`
- **项目配置**: `.mcode/config.yaml`（项目根目录）

项目配置会覆盖全局配置。详细选项参见 [`.mcode/config.yaml.example`](.mcode/config.yaml.example)。

### 权限模式

| 模式 | 说明 |
|------|------|
| `default` | 默认模式，危险操作需确认 |
| `acceptEdits` | 自动接受文件编辑 |
| `plan` | 规划模式，只读不写 |
| `bypassPermissions` | 跳过所有权限检查 |

## 目录结构

```
项目根目录/
├── .mcode/
│   ├── config.yaml          # 项目配置
│   ├── permissions.yaml     # 项目权限规则
│   ├── permissions.local.yaml  # 本地权限规则（不上传）
│   ├── sessions/            # 会话记录
│   ├── skills/              # 技能定义
│   └── debug.log            # 调试日志
├── mcode/                   # 源代码
│   ├── agent.py             # Agent 核心逻辑
│   ├── client.py            # LLM 客户端
│   ├── config.py            # 配置解析
│   ├── tools/               # 工具实现
│   ├── commands/            # 命令处理
│   └── ...
└── config.yaml              # 根目录配置（优先级最高）
```

## 开发

### 环境要求

- Python >= 3.11
- uv（推荐）

### 安装开发依赖

```bash
uv pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

## 许可证

MIT
