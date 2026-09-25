"""
Unit tests for Tool-Foundry using standard unittest.
"""

import unittest
from tool_foundry.models import ToolSpec, ToolLanguage
from tool_foundry.wasm_compiler import WasmCompiler
from tool_foundry.in_process_mcp_host import InProcessMcpHost


class TestToolFoundry(unittest.TestCase):
    def setUp(self):
        self.sample_spec = ToolSpec(
            tool_name="base64_simd_decoder",
            description="High-speed Base64 decoder in Rust",
            language=ToolLanguage.RUST,
            source_code='fn decode(input: &str) -> String { input.to_string() }',
            input_schema={"type": "object", "properties": {"raw": {"type": "string"}}},
            output_schema={"type": "object", "properties": {"decoded": {"type": "string"}}}
        )

    def test_compile_wasm_success(self):
        compiled = WasmCompiler.compile(self.sample_spec)
        self.assertEqual(compiled.tool_name, "base64_simd_decoder")
        self.assertTrue(compiled.wasm_bytecode_hex.startswith("0061736d")) # \x00asm
        self.assertLess(compiled.compilation_time_ms, 300.0)

    def test_compile_security_rejection(self):
        malicious_spec = ToolSpec(
            tool_name="bad_tool",
            description="Malicious tool trying system()",
            language=ToolLanguage.C,
            source_code='void exploit() { system("rm -rf /"); }',
            input_schema={},
            output_schema={}
        )
        with self.assertRaises(ValueError):
            WasmCompiler.compile(malicious_spec)

    def test_mount_and_execute_in_process_mcp(self):
        compiled = WasmCompiler.compile(self.sample_spec)
        host = InProcessMcpHost()
        self.assertTrue(host.mount_tool(compiled, self.sample_spec))

        mcp_tools = host.list_mcp_tools()
        self.assertEqual(len(mcp_tools), 1)
        self.assertEqual(mcp_tools[0]["name"], "base64_simd_decoder")

        res = host.execute_wasm_tool("base64_simd_decoder", {"raw": "SGVsbG8="})
        self.assertEqual(res.exit_code, 0)
        self.assertLess(res.execution_time_ms, 10.0)


if __name__ == "__main__":
    unittest.main()
