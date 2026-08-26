# MCode

A terminal-based AI coding assistant, similar to Claude Code.

## Features

- **Multi-model support**: Works with Anthropic Claude, OpenAI, and OpenAI-compatible APIs
- **Tool use**: Read/write files, execute commands, search code
- **Streaming responses**: Real-time token-by-token output
- **Permission system**: Configurable safety modes
- **MCP integration**: Extend with Model Context Protocol servers
- **Skills system**: Create and share reusable prompts

## Installation

```bash
pip install mcode
```

Or with `uv`:

```bash
uv pip install mcode
```

## Quick Start

1. Copy the config example:

```bash
cp .mcode/config.yaml.example .mcode/config.yaml
```

2. Edit `.mcode/config.yaml` and add your API key

3. Run:

```bash
mcode
```

## Configuration

See [`.mcode/config.yaml.example`](.mcode/config.yaml.example) for all available options.

## License

MIT
