"""
Tool-Foundry: Just-In-Time Autonomous Wasm Tool Synthesizer for AI Agents.
Enables agents to forge, compile, and mount native memory-isolated WebAssembly tools in under 200ms.
"""

from .models import (
    ToolLanguage,
    ToolSpec,
    CompiledWasmTool,
    WasmExecutionResult,
)
from .wasm_compiler import WasmCompiler
from .in_process_mcp_host import InProcessMcpHost

__version__ = "1.0.0"
__all__ = [
    "ToolLanguage",
    "ToolSpec",
    "CompiledWasmTool",
    "WasmExecutionResult",
    "WasmCompiler",
    "InProcessMcpHost",
]
