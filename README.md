# MCode

基于终端的 AI 编程助手，类似 Claude Code。

## 功能特性

- **多模型支持**: 支持 Anthropic Claude、OpenAI 及 OpenAI 兼容 API
- **工具调用**: 读写文件、执行命令、搜索代码
- **流式响应**: 实时逐 token 输出
- **权限系统**: 可配置的安全模式
- **MCP 集成**: 通过 Model Context Protocol 扩展功能
- **技能系统**: 创建和分享可复用的提示词

## 安装

```bash
pip install mcode
```

或使用 `uv`:

```bash
uv pip install mcode
```

## 快速开始

1. 复制配置示例：

```bash
cp .mcode/config.yaml.example .mcode/config.yaml
```

2. 编辑 `.mcode/config.yaml`，填入你的 API Key

3. 运行：

```bash
mcode
```

## 配置

参见 [`.mcode/config.yaml.example`](.mcode/config.yaml.example) 了解所有可用选项。

## 许可证

MIT
