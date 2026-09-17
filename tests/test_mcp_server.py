"""Unit tests for Model Context Protocol (MCP) JSON-RPC 2.0 Server."""

import json
import pytest

from ufo_sacred_geometry.mcp_server import MCPServer


@pytest.fixture
def mcp_server() -> MCPServer:
    return MCPServer()


def test_mcp_initialization(mcp_server):
    """Verify MCP initialize handshake returns server info and capabilities."""
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05"},
    }
    resp = mcp_server.handle_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 1
    assert "result" in resp
    assert "serverInfo" in resp["result"]
    assert resp["result"]["serverInfo"]["name"] == "ufo-sacred-geometry"


def test_mcp_ping(mcp_server):
    """Verify ping method."""
    req = {"jsonrpc": "2.0", "id": 2, "method": "ping"}
    resp = mcp_server.handle_request(req)
    assert resp["id"] == 2
    assert "result" in resp


def test_mcp_tools_list(mcp_server):
    """Verify tools/list registers all 7 geometry tools."""
    req = {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}
    resp = mcp_server.handle_request(req)
    tools = resp["result"]["tools"]
    tool_names = [t["name"] for t in tools]

    expected_tools = [
        "geometry_generate",
        "geometry_export_svg",
        "geometry_export_dxf",
        "geometry_export_obj",
        "geometry_presets",
        "geometry_phyllotaxis",
        "geometry_diagnostics",
    ]
    for expected in expected_tools:
        assert expected in tool_names


def test_mcp_tool_call_generate(mcp_server):
    """Verify tools/call geometry_generate creates valid AST and SVG output."""
    req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "geometry_generate",
            "arguments": {
                "pattern": "flower_of_life",
                "radius": 80.0,
                "iterations": 2,
                "theme": "gold",
                "include_svg": True,
            },
        },
    }
    resp = mcp_server.handle_request(req)
    assert resp["id"] == 4
    result = resp["result"]
    assert "content" in result
    content_text = result["content"][0]["text"]
    parsed = json.loads(content_text)
    assert parsed["name"] == "flower_of_life"
    assert parsed["primitive_count"] > 0
    assert "svg" in parsed


def test_mcp_tool_call_export_svg(mcp_server):
    """Verify tools/call geometry_export_svg returns raw SVG markup."""
    req = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "geometry_export_svg",
            "arguments": {"pattern": "metatrons_cube", "theme": "neon_matrix"},
        },
    }
    resp = mcp_server.handle_request(req)
    svg_text = resp["result"]["content"][0]["text"]
    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg_text
    assert '</svg>' in svg_text


def test_mcp_tool_call_export_dxf(mcp_server):
    """Verify tools/call geometry_export_dxf returns DXF content."""
    req = {
        "jsonrpc": "2.0",
        "id": 6,
        "method": "tools/call",
        "params": {
            "name": "geometry_export_dxf",
            "arguments": {"pattern": "flower_of_life", "radius": 100.0},
        },
    }
    resp = mcp_server.handle_request(req)
    dxf_text = resp["result"]["content"][0]["text"]
    assert "SECTION" in dxf_text
    assert "EOF" in dxf_text


def test_mcp_tool_call_export_obj(mcp_server):
    """Verify tools/call geometry_export_obj returns OBJ content."""
    req = {
        "jsonrpc": "2.0",
        "id": 7,
        "method": "tools/call",
        "params": {
            "name": "geometry_export_obj",
            "arguments": {"pattern": "merkaba", "radius": 100.0, "extrusion": 6.0},
        },
    }
    resp = mcp_server.handle_request(req)
    obj_text = resp["result"]["content"][0]["text"]
    assert "v " in obj_text
    assert "f " in obj_text


def test_mcp_tool_call_presets(mcp_server):
    """Verify tools/call geometry_presets returns catalog list."""
    req = {
        "jsonrpc": "2.0",
        "id": 8,
        "method": "tools/call",
        "params": {"name": "geometry_presets", "arguments": {"category": "all"}},
    }
    resp = mcp_server.handle_request(req)
    data = json.loads(resp["result"]["content"][0]["text"])
    assert data["count"] > 0
    assert len(data["presets"]) > 0


def test_mcp_resources_and_prompts(mcp_server):
    """Verify resources/list, resources/read, prompts/list, and prompts/get."""
    # Resources
    res_list = mcp_server.handle_request({"jsonrpc": "2.0", "id": 9, "method": "resources/list"})
    assert len(res_list["result"]["resources"]) >= 2

    res_read = mcp_server.handle_request(
        {"jsonrpc": "2.0", "id": 10, "method": "resources/read", "params": {"uri": "geometry://presets"}}
    )
    assert "contents" in res_read["result"]

    # Prompts
    pr_list = mcp_server.handle_request({"jsonrpc": "2.0", "id": 11, "method": "prompts/list"})
    assert len(pr_list["result"]["prompts"]) >= 2

    pr_get = mcp_server.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 12,
            "method": "prompts/get",
            "params": {"name": "geometry_create_crop_circle", "arguments": {"glyph_type": "milk_hill"}},
        }
    )
    assert "messages" in pr_get["result"]


def test_mcp_invalid_requests(mcp_server):
    """Verify error responses for invalid method or missing tool."""
    bad_method = mcp_server.handle_request({"jsonrpc": "2.0", "id": 99, "method": "unknown_method"})
    assert "error" in bad_method
    assert bad_method["error"]["code"] == -32601

    bad_tool = mcp_server.handle_request(
        {"jsonrpc": "2.0", "id": 100, "method": "tools/call", "params": {"name": "non_existent_tool"}}
    )
    assert "error" in bad_tool
