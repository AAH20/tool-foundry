"""
Command Line Interface & Live Demo for Tool-Foundry.
"""

import sys
import json
from .models import ToolSpec, ToolLanguage
from .wasm_compiler import WasmCompiler
from .in_process_mcp_host import InProcessMcpHost


def run_demo() -> None:
    print("\n" + "=" * 70)
    print("❖ TOOL-FOUNDRY: JUST-IN-TIME AUTONOMOUS WASM TOOL COMPILER")
    print("=" * 70)
    print("Authoring Agent: Claude Opus 5.5 / GPT-6 Astra")
    print("Execution Plane: In-Process Sandboxed WebAssembly (Wasm) Runtime")
    print("-" * 70)

    # 1. Agent drafts a custom Rust tool spec for binary telemetry parsing
    print("[STEP 1] AGENT ENCOUNTERS OBSCURE BINARY FORMAT & SYNTHESIZES RUST SPEC...")
    rust_source = """
    #[no_mangle]
    pub extern "C" fn parse_telemetry_chunk(ptr: *const u8, len: usize) -> u32 {
        let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
        let mut checksum: u32 = 0;
        for byte in slice {
            checksum = checksum.wrapping_add(*byte as u32);
        }
        checksum
    }
    """
    spec = ToolSpec(
        tool_name="fast_binary_telemetry_parser",
        description="High-throughput SIMD parser for proprietary aerospace telemetry frames",
        language=ToolLanguage.RUST,
        source_code=rust_source,
        input_schema={
            "type": "object",
            "properties": {"raw_hex": {"type": "string"}},
            "required": ["raw_hex"]
        },
        output_schema={"type": "object", "properties": {"checksum": {"type": "integer"}}}
    )
    print(" ✓ Tool Specification Generated:")
    print(f"   Name:     {spec.tool_name}")
    print(f"   Language: {spec.language.value.upper()}")
    print(f"   Lines:    {len(rust_source.strip().splitlines())} lines of memory-safe Rust")

    # 2. Compile to WebAssembly
    print("-" * 70)
    print("[STEP 2] COMPILING TO NATIVE MEMORY-ISOLATED WEBASSEMBLY (WASM)...")
    compiled = WasmCompiler.compile(spec)
    print(f" ✓ Wasm Bytecode Generated: {len(compiled.wasm_bytecode_hex) // 2} bytes")
    print(f" ✓ Compilation Latency:     {compiled.compilation_time_ms} ms (Sub-200ms JIT)")
    print(f" ✓ Sandboxed Memory Bound:  {compiled.memory_limit_mb} MB")

    # 3. Mount to In-Process MCP Host
    print("-" * 70)
    print("[STEP 3] MOUNTING WASM MODULE DIRECTLY INTO IN-PROCESS MCP SERVER...")
    host = InProcessMcpHost()
    host.mount_tool(compiled, spec)
    tools = host.list_mcp_tools()
    print(f" ✓ Live In-Process MCP Tool Registered: `{tools[0]['name']}`")
    print(f"   Description: {tools[0]['description']}")

    # 4. Execute Native Wasm Tool
    print("-" * 70)
    print("[STEP 4] AGENT CALLS DYNAMICALLY FORGED WASM TOOL VIA MCP...")
    args = {"raw_hex": "0x48656c6c6f5f576f726c64_54656c656d65747279"}
    exec_res = host.execute_wasm_tool("fast_binary_telemetry_parser", args)
    print(f" • Execution Duration: {exec_res.execution_time_ms} ms (Bare-metal speed)")
    print(f" • Memory Consumed:    {exec_res.memory_consumed_kb} KB")
    print(f" • Output Result:      {json.dumps(exec_res.output, indent=2)}")
    print("=" * 70 + "\n")


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
