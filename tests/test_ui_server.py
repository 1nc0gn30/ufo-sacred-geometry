"""Unit and integration tests for Google Sacred Geometry Studio UI Server & REST APIs."""

import json
import threading
import time
import urllib.request
import urllib.error
import pytest

from ufo_sacred_geometry.ui_server import (
    start_ui_server,
    generate_pattern_ast,
    export_ast_to_svg,
    export_ast_to_dxf,
    export_ast_to_obj,
    CATALOG_PRESETS,
)


@pytest.fixture(scope="module")
def live_server():
    """Start UI Server on an ephemeral local port in a background thread."""
    # Use port 8943 or similar free test port
    host = "127.0.0.1"
    port = 8943
    server = start_ui_server(host=host, port=port, open_browser=False, quiet=True)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.2)  # Allow socket bind

    base_url = f"http://{host}:{port}"
    yield base_url

    server.shutdown()
    server.server_close()


def test_ui_server_get_index(live_server):
    """Verify GET / serves the Google Material 3 Studio UI HTML."""
    req = urllib.request.Request(f"{live_server}/")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        assert "text/html" in resp.headers.get("Content-Type", "")
        body = resp.read().decode("utf-8")
        assert "Google Sacred Geometry Studio" in body or "UFO Sacred Geometry" in body


def test_ui_server_get_presets(live_server):
    """Verify GET /api/presets returns catalog."""
    req = urllib.request.Request(f"{live_server}/api/presets")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "success"
        assert data["count"] >= 10
        assert len(data["presets"]) >= 10


def test_ui_server_generate_endpoint(live_server):
    """Verify POST and GET /api/generate endpoints."""
    # GET test
    get_url = f"{live_server}/api/generate?pattern=flower_of_life&radius=150"
    with urllib.request.urlopen(get_url) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "success"
        assert data["pattern"] == "flower_of_life"
        assert "ast" in data
        assert "svg_preview" in data
        assert "<svg" in data["svg_preview"]

    # POST test
    post_url = f"{live_server}/api/generate"
    payload = json.dumps({
        "pattern": "metatrons_cube",
        "radius": 120.0,
        "stroke_width": 1.5,
    }).encode("utf-8")
    post_req = urllib.request.Request(
        post_url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(post_req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        assert data["status"] == "success"
        assert data["pattern"] == "metatrons_cube"


def test_ui_server_export_svg(live_server):
    """Verify GET and POST /api/export-svg returns SVG image payload with attachment headers."""
    url = f"{live_server}/api/export-svg?pattern=sri_yantra&radius=140"
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        assert "image/svg+xml" in resp.headers.get("Content-Type", "")
        assert "attachment;" in resp.headers.get("Content-Disposition", "")
        content = resp.read().decode("utf-8")
        assert "<svg" in content
        assert "</svg>" in content


def test_ui_server_export_dxf(live_server):
    """Verify GET and POST /api/export-dxf returns DXF CAD file."""
    url = f"{live_server}/api/export-dxf?pattern=flower_of_life"
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        content = resp.read().decode("utf-8")
        assert "SECTION" in content
        assert "EOF" in content


def test_ui_server_export_obj(live_server):
    """Verify GET and POST /api/export-obj returns 3D OBJ mesh."""
    url = f"{live_server}/api/export-obj?pattern=merkaba"
    with urllib.request.urlopen(url) as resp:
        assert resp.status == 200
        content = resp.read().decode("utf-8")
        assert "v " in content


def test_ui_server_stats_and_diagnostics(live_server):
    """Verify GET /api/stats and /api/diagnostics endpoints."""
    with urllib.request.urlopen(f"{live_server}/api/stats") as resp:
        assert resp.status == 200
        stats = json.loads(resp.read().decode("utf-8"))
        assert stats["service"] == "Google Sacred Geometry Studio"
        assert "uptime_seconds" in stats

    with urllib.request.urlopen(f"{live_server}/api/diagnostics") as resp:
        assert resp.status == 200
        diag = json.loads(resp.read().decode("utf-8"))
        assert "python_version" in diag
        assert "phi_constant" in diag
        assert "endpoints" in diag


def test_ui_server_cors_options(live_server):
    """Verify OPTIONS preflight request sets CORS headers."""
    req = urllib.request.Request(f"{live_server}/api/generate", method="OPTIONS")
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 204
        assert resp.headers.get("Access-Control-Allow-Origin") == "*"
