"""
Data models and typed schemas for Tool-Foundry Wasm synthesis.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import time


class ToolLanguage(str, Enum):
    RUST = "rust"
    C = "c"
    ASSEMBLY_SCRIPT = "assemblyscript"


@dataclass
class ToolSpec:
    tool_name: str
    description: str
    language: ToolLanguage
    source_code: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    created_at: float = field(default_factory=time.time)


@dataclass
class CompiledWasmTool:
    tool_id: str
    tool_name: str
    wasm_bytecode_hex: str
    compilation_time_ms: float
    memory_limit_mb: int = 16
    is_mounted: bool = False
    registered_at: float = field(default_factory=time.time)


@dataclass
class WasmExecutionResult:
    tool_name: str
    output: Dict[str, Any]
    execution_time_ms: float
    memory_consumed_kb: float
    exit_code: int = 0
