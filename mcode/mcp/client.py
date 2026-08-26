from __future__ import annotations

import logging
import os
from contextlib import AsyncExitStack
from typing import Any

import httpx

from mcode.config import MCPServerConfig, build_child_env, resolve_env_vars

logger = logging.getLogger(__name__)

# 延迟导入外部 mcp 包，避免与 mcode.mcp 包名冲突
_mcp_imported = False
_ClientSession = None
_types = None
_StdioServerParameters = None
_stdio_client = None
_streamable_http_client = None


def _import_mcp():
    """延迟导入外部 mcp 包"""
    global _mcp_imported, _ClientSession, _types, _StdioServerParameters, _stdio_client, _streamable_http_client
    if _mcp_imported:
        return
    import importlib
    _mod = importlib.import_module("mcp")
    _types = _mod.types
    _session_mod = importlib.import_module("mcp.client.session")
    _ClientSession = _session_mod.ClientSession
    _stdio_mod = importlib.import_module("mcp.client.stdio")
    _StdioServerParameters = _stdio_mod.StdioServerParameters
    _stdio_client = _stdio_mod.stdio_client
    _streamable_http_mod = importlib.import_module("mcp.client.streamable_http")
    _streamable_http_client = _streamable_http_mod.streamable_http_client
    _mcp_imported = True


class MCPClient:
    def __init__(self, config: MCPServerConfig) -> None:
        self.config = config
        self.name = config.name
        self._session = None
        self._stack: AsyncExitStack | None = None
        self._alive = False
        self._init_result = None


    @property
    def is_alive(self) -> bool:
        return self._alive

    @property
    def instructions(self) -> str:
        """返回 MCP 服务器的 instructions（来自 InitializeResult）。"""
        if self._init_result is not None and self._init_result.instructions:
            return self._init_result.instructions
        return ""


    async def connect(self) -> None:
        if self._alive:
            return

        _import_mcp()

        self._stack = AsyncExitStack()
        await self._stack.__aenter__()

        try:
            if self.config.is_stdio:
                read, write = await self._connect_stdio()
            else:
                read, write = await self._connect_http()

            session = await self._stack.enter_async_context(
                _ClientSession(read, write)
            )
            self._init_result = await session.initialize()
            self._session = session
            self._alive = True
            logger.info("MCP server '%s' connected", self.name)
        except Exception:
            await self._cleanup_stack()
            raise


    async def _connect_stdio(self) -> tuple[Any, Any]:
        assert self._stack is not None
        assert self.config.command is not None

        params = _StdioServerParameters(
            command=self.config.command,
            args=self.config.args,
            env=build_child_env(self.config.env),
        )
        devnull = open(os.devnull, "w")
        self._stack.callback(devnull.close)
        read, write = await self._stack.enter_async_context(
            _stdio_client(params, errlog=devnull)
        )
        return read, write

    async def _connect_http(self) -> tuple[Any, Any]:
        assert self._stack is not None
        assert self.config.url is not None

        resolved_headers = {
            k: resolve_env_vars(v) for k, v in self.config.headers.items()
        }
        http_client = httpx.AsyncClient(
            headers=resolved_headers,
            follow_redirects=True,
        )
        await self._stack.enter_async_context(http_client)

        result = await self._stack.enter_async_context(
            _streamable_http_client(self.config.url, http_client=http_client)
        )
        read, write = result[0], result[1]
        return read, write


    async def list_tools(self) -> list:
        assert self._session is not None
        result = await self._session.list_tools()
        return list(result.tools)


    async def call_tool(
        self, name: str, arguments: dict[str, Any]
    ):
        assert self._session is not None
        return await self._session.call_tool(name, arguments)

    async def close(self) -> None:
        self._alive = False
        self._session = None
        await self._cleanup_stack()

    async def _cleanup_stack(self) -> None:
        if self._stack is not None:
            try:
                await self._stack.__aexit__(None, None, None)
            except RuntimeError as e:
                if "cancel scope" in str(e):
                    logger.debug("Cancel scope cleanup (expected during shutdown): %s", e)
                else:
                    raise
            except Exception:
                logger.debug("Error closing stack for '%s'", self.name, exc_info=True)
            self._stack = None
