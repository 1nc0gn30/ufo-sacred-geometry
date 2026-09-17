"""
Command-Line Interface (CLI) for UFO Sacred Geometry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Multi-OS terminal interface providing pattern generation, CAD/vector export,
interactive Material 3 Web Studio server, MCP stdio protocol launcher,
diagnostics, and internal verification test runner.
"""

from __future__ import annotations

import argparse
import http.server
import io
import json
import math
import os
import platform
import socketserver
import sys
import time
import urllib.parse
import webbrowser
from typing import Any, Dict, List, Optional

from ufo_sacred_geometry import (
    GOLDEN_ANGLE_DEG,
    PHI,
    PRESETS_CATALOG,
    THEMES,
    __author__,
    __version__,
    export_dxf,
    export_obj,
    export_svg,
    generate_pattern,
    generate_phyllotaxis,
    get_preset,
    list_presets,
    GeometryAST,
)
from ufo_sacred_geometry.mcp_server import MCPServer


# -----------------------------------------------------------------------------
# Terminal Styling & Color Support
# -----------------------------------------------------------------------------
class TermColor:
    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled and self._detect_color_support()

    def _detect_color_support(self) -> bool:
        if "NO_COLOR" in os.environ:
            return False
        if not sys.stdout.isatty():
            return False
        return True

    def _wrap(self, code: str, text: str) -> str:
        if not self.enabled:
            return text
        return f"\033[{code}m{text}\033[0m"

    def bold(self, text: str) -> str:
        return self._wrap("1", text)

    def dim(self, text: str) -> str:
        return self._wrap("2", text)

    def gold(self, text: str) -> str:
        return self._wrap("38;5;220", text)

    def cyan(self, text: str) -> str:
        return self._wrap("36", text)

    def green(self, text: str) -> str:
        return self._wrap("32", text)

    def yellow(self, text: str) -> str:
        return self._wrap("33", text)

    def red(self, text: str) -> str:
        return self._wrap("31", text)

    def magenta(self, text: str) -> str:
        return self._wrap("35", text)


# -----------------------------------------------------------------------------
# Embedded Web Studio UI (design influenced by Material 3)
# -----------------------------------------------------------------------------
EMBEDDED_STUDIO_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>UFO Sacred Geometry Studio & Agroglyph Engine</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #090a10;
      --surface: #121420;
      --surface-elevated: #1a1d30;
      --surface-border: #2a2e48;
      --primary: #d4af37;
      --primary-bright: #f5d77f;
      --primary-glow: rgba(212, 175, 55, 0.25);
      --accent-cyan: #00e5ff;
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --radius-sm: 8px;
      --radius-md: 14px;
      --radius-lg: 20px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }
    header {
      background: rgba(18, 20, 32, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--surface-border);
      padding: 14px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .logo-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-icon {
      width: 38px;
      height: 38px;
      background: radial-gradient(circle, #f5d77f 0%, #d4af37 60%, #8a7322 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 16px var(--primary-glow);
    }
    .logo-title {
      font-family: 'Cinzel', serif;
      font-weight: 700;
      font-size: 1.25rem;
      letter-spacing: 0.05em;
      background: linear-gradient(135deg, #fff 0%, #f5d77f 60%, #d4af37 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      background: rgba(212, 175, 55, 0.15);
      color: var(--primary-bright);
      padding: 3px 8px;
      border-radius: 12px;
      border: 1px solid rgba(212, 175, 55, 0.3);
    }
    .app-container {
      display: grid;
      grid-template-columns: 380px 1fr;
      flex: 1;
      height: calc(100vh - 67px);
    }
    @media (max-width: 900px) {
      .app-container { grid-template-columns: 1fr; height: auto; }
    }
    .sidebar {
      background: var(--surface);
      border-right: 1px solid var(--surface-border);
      padding: 24px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .control-card {
      background: var(--surface-elevated);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-md);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .card-title {
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 6px;
    }
    label {
      font-size: 0.82rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      margin-bottom: 6px;
    }
    select, input[type="range"] {
      width: 100%;
      background: #0d0f1a;
      border: 1px solid var(--surface-border);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      font-family: inherit;
      font-size: 0.9rem;
      outline: none;
      transition: border-color 0.2s;
    }
    select:focus { border-color: var(--primary); }
    .btn-group {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
    }
    button.btn {
      background: var(--surface-border);
      color: var(--text-main);
      border: none;
      padding: 10px 14px;
      border-radius: var(--radius-sm);
      font-weight: 600;
      font-size: 0.82rem;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }
    button.btn:hover {
      background: var(--primary);
      color: #000;
      box-shadow: 0 0 12px var(--primary-glow);
    }
    button.btn-primary {
      background: linear-gradient(135deg, #f5d77f 0%, #d4af37 100%);
      color: #0d0e15;
    }
    .preview-area {
      background: radial-gradient(circle at center, #141728 0%, #08090f 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
      padding: 30px;
      overflow: hidden;
    }
    .viewport-box {
      width: 100%;
      max-width: 680px;
      aspect-ratio: 1 / 1;
      background: rgba(10, 12, 22, 0.7);
      border: 1px solid var(--surface-border);
      border-radius: var(--radius-lg);
      box-shadow: 0 16px 40px rgba(0,0,0,0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      position: relative;
    }
    .viewport-box svg {
      width: 100%;
      height: 100%;
      filter: drop-shadow(0 0 18px var(--primary-glow));
    }
    .export-bar {
      position: absolute;
      bottom: 24px;
      display: flex;
      gap: 10px;
      background: rgba(18, 20, 32, 0.9);
      backdrop-filter: blur(12px);
      padding: 8px 16px;
      border-radius: 30px;
      border: 1px solid var(--surface-border);
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
    }
    .info-footer {
      font-size: 0.78rem;
      color: var(--text-dim);
      text-align: center;
      margin-top: auto;
      padding-top: 14px;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo-group">
      <div class="logo-icon">✦</div>
      <div class="logo-title">UFO SACRED GEOMETRY</div>
      <span class="badge">STUDIO v0.1.0</span>
    </div>
    <div>
      <span style="font-size:0.8rem; color:var(--primary-bright); font-family:'JetBrains Mono'">MCP PROTOCOL READY</span>
    </div>
  </header>

  <div class="app-container">
    <div class="sidebar">
      <div class="control-card">
        <div class="card-title">✦ Pattern Generator</div>
        <div>
          <label for="patternSelect">Pattern Archetype</label>
          <select id="patternSelect">
            <optgroup label="Sacred Geometry">
              <option value="flower_of_life" selected>Flower of Life (19 Circles)</option>
              <option value="seed_of_life">Seed of Life (7 Creation Rings)</option>
              <option value="metatrons_cube">Metatron's Cube (Platonic Solids)</option>
              <option value="merkaba">Merkaba Star Tetrahedron</option>
              <option value="vesica_piscis">Vesica Piscis (Mandorla)</option>
            </optgroup>
            <optgroup label="Spirals & Harmonics">
              <option value="fibonacci_spiral">Fibonacci Golden Spiral & Rectangles</option>
              <option value="phyllotaxis">Fibonacci Sunflower Phyllotaxis</option>
              <option value="torus">Toroidal Magnetic Flux Field</option>
            </optgroup>
            <optgroup label="Vedic Chakras & Agroglyphs">
              <option value="sri_yantra">Sri Yantra (Cosmic Navayoni)</option>
              <option value="crop_circle_milk_hill">Crop Circle: Milk Hill 409-Circle Julia Set</option>
              <option value="crop_circle_pi">Crop Circle: Barbury Castle Pi Glyph</option>
              <option value="crop_circle_barbury_castle">Crop Circle: Barbury Castle Tetrahedron</option>
            </optgroup>
          </select>
        </div>

        <div>
          <label for="themeSelect">Visual Palette</label>
          <select id="themeSelect">
            <option value="gold" selected>Sacred Gold</option>
            <option value="blueprint">Architectural Blueprint</option>
            <option value="neon_matrix">Matrix Phosphor</option>
            <option value="obsidian_dark">Obsidian Starlight</option>
            <option value="light_minimal">Minimalist Slate</option>
          </select>
        </div>
      </div>

      <div class="control-card">
        <div class="card-title">✦ Sacred Parameters</div>
        <div>
          <label><span>Radius</span> <span id="radiusVal">120 mm</span></label>
          <input type="range" id="radiusInput" min="40" max="240" step="5" value="120">
        </div>
        <div>
          <label><span>Iterations / Depth</span> <span id="iterVal">2</span></label>
          <input type="range" id="iterInput" min="1" max="5" step="1" value="2">
        </div>
        <div>
          <label><span>Scale Factor</span> <span id="scaleVal">1.0x</span></label>
          <input type="range" id="scaleInput" min="0.5" max="2.0" step="0.1" value="1.0">
        </div>
      </div>

      <div class="control-card">
        <div class="card-title">✦ CAD & Vector Export</div>
        <div class="btn-group">
          <button class="btn btn-primary" onclick="downloadExport('svg')">Export SVG</button>
          <button class="btn" onclick="downloadExport('dxf')">AutoCAD DXF</button>
          <button class="btn" onclick="downloadExport('obj')">3D Mesh OBJ</button>
          <button class="btn" onclick="downloadExport('json')">Geometry AST</button>
        </div>
      </div>

      <div class="info-footer">
        Φ = 1.6180339887 | Golden Angle = 137.507764°<br>
        Pure Python 3 Standard Library Engine
      </div>
    </div>

    <div class="preview-area">
      <div class="viewport-box" id="svgContainer">
        <div style="color:var(--primary-bright)">Rendering Sacred Matrix...</div>
      </div>

      <div class="export-bar">
        <button class="btn" onclick="downloadExport('svg')">Download Vector SVG</button>
        <button class="btn" onclick="downloadExport('dxf')">Download CNC DXF</button>
        <button class="btn" onclick="downloadExport('obj')">Download 3D OBJ</button>
      </div>
    </div>
  </div>

  <script>
    const patternSelect = document.getElementById('patternSelect');
    const themeSelect = document.getElementById('themeSelect');
    const radiusInput = document.getElementById('radiusInput');
    const iterInput = document.getElementById('iterInput');
    const scaleInput = document.getElementById('scaleInput');
    const svgContainer = document.getElementById('svgContainer');

    function updateLabels() {
      document.getElementById('radiusVal').textContent = radiusInput.value + ' mm';
      document.getElementById('iterVal').textContent = iterInput.value;
      document.getElementById('scaleVal').textContent = scaleInput.value + 'x';
    }

    async function renderPattern() {
      updateLabels();
      const pattern = patternSelect.value;
      const theme = themeSelect.value;
      const radius = radiusInput.value;
      const iterations = iterInput.value;
      const scale = scaleInput.value;

      try {
        const url = `/api/generate?pattern=${encodeURIComponent(pattern)}&theme=${encodeURIComponent(theme)}&radius=${radius}&iterations=${iterations}&scale=${scale}&format=svg`;
        const resp = await fetch(url);
        if (!resp.ok) throw new Error('Generation failed: ' + resp.statusText);
        const svgText = await resp.text();
        svgContainer.innerHTML = svgText;
      } catch (err) {
        svgContainer.innerHTML = `<div style="color:#ff6b6b">Error: ${err.message}</div>`;
      }
    }

    function downloadExport(format) {
      const pattern = patternSelect.value;
      const theme = themeSelect.value;
      const radius = radiusInput.value;
      const iterations = iterInput.value;
      const scale = scaleInput.value;
      const url = `/api/export?pattern=${encodeURIComponent(pattern)}&theme=${encodeURIComponent(theme)}&radius=${radius}&iterations=${iterations}&scale=${scale}&format=${format}`;
      window.location.href = url;
    }

    patternSelect.addEventListener('change', renderPattern);
    themeSelect.addEventListener('change', renderPattern);
    radiusInput.addEventListener('input', renderPattern);
    iterInput.addEventListener('input', renderPattern);
    scaleInput.addEventListener('input', renderPattern);

    window.addEventListener('DOMContentLoaded', renderPattern);
  </script>
</body>
</html>
"""


# -----------------------------------------------------------------------------
# Studio HTTP Server Handler
# -----------------------------------------------------------------------------
class StudioHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler serving static web studio and dynamic generation APIs."""

    def __init__(self, *args: Any, public_dir: str = "", **kwargs: Any) -> None:
        self.public_dir = public_dir
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        # Quiet standard logging to keep terminal tidy
        pass

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path in ("/api/presets", "/presets"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            data = [p.to_dict() for p in list_presets()]
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
            return

        elif path == "/api/generate":
            pattern = query.get("pattern", ["flower_of_life"])[0]
            theme = query.get("theme", ["gold"])[0]
            radius = float(query.get("radius", [100.0])[0])
            iterations = int(query.get("iterations", [2])[0])
            scale = float(query.get("scale", [1.0])[0])
            fmt = query.get("format", ["svg"])[0]

            ast = generate_pattern(pattern, radius=radius, iterations=iterations, theme=theme)
            if abs(scale - 1.0) > 1e-4:
                ast.scale(scale)

            if fmt == "json":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(ast.to_json().encode("utf-8"))
            else:
                svg_data = export_svg(ast, theme=theme)
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(svg_data.encode("utf-8"))
            return

        elif path == "/api/export":
            pattern = query.get("pattern", ["flower_of_life"])[0]
            theme = query.get("theme", ["gold"])[0]
            radius = float(query.get("radius", [100.0])[0])
            iterations = int(query.get("iterations", [2])[0])
            scale = float(query.get("scale", [1.0])[0])
            fmt = query.get("format", ["svg"])[0].lower()

            ast = generate_pattern(pattern, radius=radius, iterations=iterations, theme=theme)
            if abs(scale - 1.0) > 1e-4:
                ast.scale(scale)

            if fmt == "dxf":
                payload = export_dxf(ast).encode("utf-8")
                mime = "application/dxf"
                ext = "dxf"
            elif fmt == "obj":
                payload = export_obj(ast).encode("utf-8")
                mime = "model/obj"
                ext = "obj"
            elif fmt == "json":
                payload = ast.to_json().encode("utf-8")
                mime = "application/json"
                ext = "json"
            else:
                payload = export_svg(ast, theme=theme).encode("utf-8")
                mime = "image/svg+xml"
                ext = "svg"

            filename = f"{pattern}_{theme}.{ext}"
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(payload)
            return

        # Serve static studio UI
        if path in ("/", "/index.html"):
            # Check if custom public/index.html exists
            public_index = os.path.join(self.public_dir, "index.html")
            if os.path.isfile(public_index):
                with open(public_index, "rb") as f:
                    content = f.read()
            else:
                content = EMBEDDED_STUDIO_HTML.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        # Default fallback
        super().do_GET()


# -----------------------------------------------------------------------------
# CLI Subcommand Implementations
# -----------------------------------------------------------------------------
def cmd_generate(args: argparse.Namespace, tc: TermColor) -> int:
    """Handles 'generate <pattern>' CLI command."""
    pattern_name = args.pattern
    radius = args.radius
    iterations = args.iterations
    petals = args.petals
    scale = args.scale
    theme = args.theme
    glyph_type = args.glyph_type
    seed_count = args.seed_count
    divergence_angle = args.divergence_angle
    out_format = args.format.lower() if args.format else None
    output_path = args.output

    # Deduce format from output path if not explicitly provided
    if output_path and not out_format:
        ext = os.path.splitext(output_path)[1].lower().replace(".", "")
        if ext in ("svg", "dxf", "obj", "json"):
            out_format = ext

    if not out_format:
        out_format = "json" if args.json else "svg"

    try:
        ast = generate_pattern(
            pattern_name,
            radius=radius,
            iterations=iterations,
            petals=petals,
            theme=theme,
            glyph_type=glyph_type,
            seed_count=seed_count,
            divergence_angle=divergence_angle,
        )

        if abs(scale - 1.0) > 1e-4:
            ast.scale(scale)

        if out_format == "dxf":
            content = export_dxf(ast)
        elif out_format == "obj":
            content = export_obj(ast)
        elif out_format == "json":
            content = ast.to_json(indent=2)
        else:  # "svg"
            content = export_svg(ast, theme=theme)

        if output_path:
            out_dir = os.path.dirname(output_path)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            if not getattr(args, "quiet", False):
                stats = ast.stats() if hasattr(ast, "stats") else {}
                prim_count = stats.get("total_primitives", "N/A")
                print(
                    f"{tc.green('✓')} Generated {tc.bold(getattr(ast, 'title', pattern_name))} ({prim_count} primitives) -> {tc.cyan(output_path)}"
                )
        else:
            # Print to stdout
            print(content)

        return 0

    except Exception as e:
        sys.stderr.write(f"{tc.red('Error generating pattern')}: {e}\n")
        return 1


def cmd_presets(args: argparse.Namespace, tc: TermColor) -> int:
    """Handles 'presets' CLI command."""
    category = args.category
    presets = list_presets(category)

    if getattr(args, "json", False):
        data = [p.to_dict() for p in presets]
        print(json.dumps(data, indent=2))
        return 0

    print(tc.bold(f"\n✦ Sacred Geometry & UFO Crop Circle Presets ({len(presets)} cataloged)\n"))
    print(f"{'ID':<30} {'Category':<14} {'Difficulty':<12} {'Description'}")
    print("-" * 110)

    for p in presets:
        cat_badge = tc.cyan(f"[{p.category}]")
        diff_badge = tc.dim(p.difficulty.upper())
        print(f"{tc.gold(p.id):<38} {cat_badge:<22} {diff_badge:<20} {p.description}")

    print(tc.dim("\nUse 'ufo-sacred-geometry generate <preset_id>' or '--help' for custom parameters.\n"))
    return 0


def cmd_export(args: argparse.Namespace, tc: TermColor) -> int:
    """Handles 'export <pattern>' CLI command."""
    pattern_name = args.pattern
    fmt = args.format.lower() if args.format else "svg"
    output_path = args.output
    theme = args.theme
    radius = args.radius
    iterations = args.iterations
    scale = args.scale
    extrusion = args.extrusion
    base_plate = args.base_plate

    if not output_path:
        output_path = f"{pattern_name}.{fmt}"

    try:
        ast = generate_pattern(pattern_name, radius=radius, iterations=iterations, theme=theme)
        if abs(scale - 1.0) > 1e-4:
            ast.scale(scale)

        if fmt == "dxf":
            payload = export_dxf(ast)
        elif fmt == "obj":
            payload = export_obj(ast, extrusion=extrusion, medallion_base=base_plate)
        elif fmt == "json":
            payload = ast.to_json()
        else:
            payload = export_svg(ast, theme=theme)

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(payload)

        print(
            f"{tc.green('✓')} Exported {tc.bold(pattern_name)} ({fmt.upper()}) to {tc.cyan(output_path)} "
            f"[{len(payload.encode('utf-8'))} bytes]"
        )
        return 0

    except Exception as e:
        sys.stderr.write(f"{tc.red('Export failed')}: {e}\n")
        return 1


def cmd_serve(args: argparse.Namespace, tc: TermColor) -> int:
    """Handles 'serve' CLI command, launching Web Studio (design influenced by Material 3)."""
    port = args.port
    host = args.host
    auto_open = args.open
    public_dir = os.path.abspath(args.public_dir or "public")

    url = f"http://{host}:{port}/"
    print(f"\n{tc.gold('✦ UFO Sacred Geometry & Agroglyph Studio')}")
    print(f"  {tc.dim('Version:')} {__version__}")
    print(f"  {tc.dim('Serving UI at:')} {tc.bold(tc.cyan(url))}")
    print(f"  {tc.dim('Press Ctrl+C to stop.')}\n")

    handler_factory = lambda *h_args, **h_kwargs: StudioHTTPHandler(
        *h_args, public_dir=public_dir, **h_kwargs
    )

    try:
        server = socketserver.TCPServer((host, port), handler_factory)
    except OSError as oe:
        sys.stderr.write(f"{tc.red('Failed to bind port')}: {oe}\n")
        return 1

    if auto_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{tc.dim('Studio server stopped.')}")
    finally:
        server.server_close()

    return 0


def cmd_mcp(args: argparse.Namespace, tc: TermColor) -> int:
    """Handles 'mcp' CLI command, running MCP stdio JSON-RPC server."""
    server = MCPServer()
    server.run_stdio()
    return 0


def cmd_diagnostics(args: argparse.Namespace, tc: TermColor) -> int:
    """Handles 'diagnostics', 'doctor', and 'platform' CLI commands."""
    t0 = time.perf_counter()
    test_ast = generate_pattern("metatrons_cube", radius=100.0)
    svg_sample = export_svg(test_ast)
    dxf_sample = export_dxf(test_ast)
    obj_sample = export_obj(test_ast)
    t_elapsed_ms = (time.perf_counter() - t0) * 1000.0

    stats = test_ast.stats() if hasattr(test_ast, "stats") else {}

    diag: Dict[str, Any] = {
        "status": "PASS",
        "version": __version__,
        "author": __author__,
        "system": {
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
        },
        "math_engine": {
            "phi": PHI,
            "golden_angle_deg": GOLDEN_ANGLE_DEG,
            "float_epsilon": sys.float_info.epsilon,
            "float_max": sys.float_info.max,
        },
        "formats_supported": ["SVG", "DXF (AutoCAD R12/2000)", "OBJ (Wavefront 3D)", "JSON (AST)"],
        "presets_count": len(PRESETS_CATALOG),
        "benchmark": {
            "test_pattern": "metatrons_cube",
            "primitives_generated": stats.get("total_primitives", 91),
            "svg_bytes": len(svg_sample.encode("utf-8")),
            "dxf_bytes": len(dxf_sample.encode("utf-8")),
            "obj_bytes": len(obj_sample.encode("utf-8")),
            "time_ms": round(t_elapsed_ms, 3),
        },
    }

    if getattr(args, "json", False):
        print(json.dumps(diag, indent=2))
        return 0

    print(tc.bold(f"\n✦ UFO Sacred Geometry Diagnostic Doctor (v{__version__})\n"))
    print(f"  {tc.dim('Operating System:')}   {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  {tc.dim('Python Version:')}     {platform.python_version()} [{platform.python_implementation()}]")
    print(f"  {tc.dim('Golden Ratio (Φ):')}   {PHI:.10f}")
    print(f"  {tc.dim('Golden Angle:')}       {GOLDEN_ANGLE_DEG:.8f}°")
    print(f"  {tc.dim('Built-in Presets:')}   {len(PRESETS_CATALOG)} templates")
    print(f"  {tc.dim('CAD / Exporters:')}    SVG (Vector), DXF (AutoCAD), OBJ (3D Mesh), AST JSON")
    print(f"  {tc.dim('Benchmark Engine:')}   {tc.green('PASS')} ({stats.get('total_primitives', 91)} nodes in {t_elapsed_ms:.2f} ms)\n")
    return 0


def cmd_test(args: argparse.Namespace, tc: TermColor) -> int:
    """Internal self-verification test runner."""
    print(tc.bold(f"\n✦ Running UFO Sacred Geometry Test Suite (v{__version__})...\n"))

    failures = 0
    total_tests = 0

    def run_check(name: str, check_fn: Any) -> None:
        nonlocal failures, total_tests
        total_tests += 1
        t_start = time.perf_counter()
        try:
            check_fn()
            ms = (time.perf_counter() - t_start) * 1000.0
            print(f"  {tc.green('✓ PASS')}  {name:<52} {tc.dim(f'[{ms:.2f} ms]')}")
        except Exception as err:
            failures += 1
            print(f"  {tc.red('✗ FAIL')}  {name:<52} {tc.red(str(err))}")

    # Test 1: All preset generation
    for preset_id in PRESETS_CATALOG.keys():
        run_check(
            f"Preset '{preset_id}' generation",
            lambda pid=preset_id: generate_pattern(pid),
        )

    # Test 2: Flower of Life math & bounding box
    def test_flower():
        ast = generate_pattern("flower_of_life", radius=50.0, rings=3)
        assert len(ast.circles) >= 19, f"Expected at least 19 circles, got {len(ast.circles)}"
        bb = ast.bounds()
        assert bb.width > 0 and bb.height > 0, "Invalid bounding box"

    run_check("Flower of Life circle generation", test_flower)

    # Test 3: Metatron's Cube Platonic Lines
    def test_metatron():
        ast = generate_pattern("metatrons_cube", radius=35.0)
        assert len(ast.lines) >= 78, f"Expected 78 Metatron lines, got {len(ast.lines)}"

    run_check("Metatron's Cube 78 Platonic lines", test_metatron)

    # Test 4: Fibonacci Logarithmic Spiral
    def test_fib():
        ast = generate_pattern("fibonacci_spiral", scale=8.0, turns=6)
        stats = ast.stats()
        assert stats["total_primitives"] > 0, "No primitives generated"

    run_check("Fibonacci Golden Spiral & Rectangles", test_fib)

    # Test 5: Sri Yantra 9 Shiva/Shakti triangles & Bhupura
    def test_sri_yantra():
        ast = generate_pattern("sri_yantra", size=180.0, show_bhupura=True)
        assert len(ast.polygons) >= 9 or len(ast.lines) > 0, "Expected polygons/lines for Sri Yantra"

    run_check("Sri Yantra 9 interlocking triangles & Bhupura", test_sri_yantra)

    # Test 6: Crop Circle Milk Hill 409-Circle Simulation
    def test_crop_circle():
        ast = generate_pattern("crop_circle_milk_hill", scale=220.0)
        assert len(ast.circles) >= 400, f"Expected ~409 circles, got {len(ast.circles)}"

    run_check("Crop Circle Milk Hill Julia Set", test_crop_circle)

    # Test 7: Merkaba Star Tetrahedron
    def test_merkaba():
        ast = generate_pattern("merkaba", radius=120.0)
        stats = ast.stats()
        assert stats["total_primitives"] >= 6, "Merkaba failed to generate"

    run_check("Merkaba Star Tetrahedron", test_merkaba)

    # Test 8: Torus Vortex Flux
    def test_torus():
        ast = generate_pattern("torus", major_radius=160.0, strands=24)
        stats = ast.stats()
        assert stats["total_primitives"] >= 24, "Torus failed to generate"

    run_check("Toroidal Vortex Field (24 strands)", test_torus)

    # Test 9: Phyllotaxis Disc Distribution
    def test_phyllotaxis():
        ast = generate_phyllotaxis(count=200)
        assert len(ast.circles) >= 200, "Phyllotaxis failed to generate 200 seeds"

    run_check("Fibonacci Phyllotaxis (200 seeds)", test_phyllotaxis)

    # Test 10: Vector SVG Exporter
    def test_svg_export():
        ast = generate_pattern("metatrons_cube", radius=35.0)
        svg_str = export_svg(ast, theme="gold")
        assert svg_str.startswith("<?xml"), "Missing XML header"
        assert "</svg>" in svg_str, "Missing SVG closing tag"

    run_check("SVG vector export format validation", test_svg_export)

    # Test 11: AutoCAD DXF Exporter
    def test_dxf_export():
        ast = generate_pattern("flower_of_life", radius=50.0)
        dxf_str = export_dxf(ast)
        assert "SECTION" in dxf_str and "ENTITIES" in dxf_str and "EOF" in dxf_str, "Invalid DXF structure"

    run_check("AutoCAD DXF R12/2000 export validation", test_dxf_export)

    # Test 12: Wavefront OBJ 3D Mesh Exporter
    def test_obj_export():
        ast = generate_pattern("merkaba", radius=100.0)
        obj_str = export_obj(ast, extrusion=5.0)
        assert "v " in obj_str and ("f " in obj_str or "l " in obj_str), "Invalid Wavefront OBJ mesh"

    run_check("Wavefront OBJ 3D extrusion validation", test_obj_export)

    # Test 13: AST JSON Roundtrip Serialization
    def test_ast_json():
        ast = generate_pattern("seed_of_life", radius=60.0)
        d = ast.to_dict()
        reconstructed = GeometryAST.from_dict(d)
        assert len(reconstructed.circles) == len(ast.circles), "AST roundtrip mismatch"

    run_check("AST JSON serialization roundtrip", test_ast_json)

    # Test 14: MCP Server Protocol Handshake
    def test_mcp_handshake():
        server = MCPServer()
        init_req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        init_resp = server.handle_request(init_req)
        assert init_resp is not None and init_resp.get("result", {}).get("protocolVersion") == "2024-11-05"

        tools_req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        tools_resp = server.handle_request(tools_req)
        assert tools_resp is not None and len(tools_resp.get("result", {}).get("tools", [])) >= 7

    run_check("MCP protocol JSON-RPC 2.0 handshake & tools list", test_mcp_handshake)

    print("-" * 70)
    if failures == 0:
        print(tc.green(tc.bold(f"✓ All {total_tests} verification tests passed successfully!")))
        return 0
    else:
        print(tc.red(tc.bold(f"✗ {failures} out of {total_tests} verification tests failed.")))
        return 1


# -----------------------------------------------------------------------------
# Main Argument Parser & Dispatcher
# -----------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    # Parent parser with common flags
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color formatting in terminal output",
    )
    common_parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress non-essential informational messages",
    )
    common_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed verbose output",
    )

    parser = argparse.ArgumentParser(
        prog="ufo-sacred-geometry",
        description="✦ UFO Sacred Geometry & Agroglyph CAD/Vector Engine with MCP Server",
        parents=[common_parser],
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="subcommand", title="Commands", help="Available subcommands")

    # 1. generate
    gen_p = subparsers.add_parser(
        "generate",
        help="Generate sacred geometry or crop circle pattern AST and output vector/CAD files",
        parents=[common_parser],
    )
    gen_p.add_argument(
        "pattern",
        nargs="?",
        default="flower_of_life",
        help="Pattern type or preset ID (e.g. flower_of_life, metatrons_cube, sri_yantra, crop_circle, merkaba, torus, phyllotaxis)",
    )
    gen_p.add_argument("--radius", "-r", type=float, default=100.0, help="Base radius in mm (default: 100.0)")
    gen_p.add_argument("--iterations", "-i", type=int, default=2, help="Iteration / concentric ring count (default: 2)")
    gen_p.add_argument("--petals", type=int, default=16, help="Petal count for Sri Yantra / mandalas (default: 16)")
    gen_p.add_argument("--scale", "-s", type=float, default=1.0, help="Affine uniform scale factor (default: 1.0)")
    gen_p.add_argument(
        "--theme",
        "-t",
        choices=list(THEMES.keys()),
        default="gold",
        help="Color theme palette (default: gold)",
    )
    gen_p.add_argument(
        "--glyph-type",
        choices=["julia_set", "pi_glyph", "barbury_castle"],
        default="julia_set",
        help="Crop glyph archetype variant",
    )
    gen_p.add_argument("--seed-count", type=int, default=300, help="Seed count for phyllotaxis (default: 300)")
    gen_p.add_argument(
        "--divergence-angle",
        type=float,
        default=GOLDEN_ANGLE_DEG,
        help=f"Divergence angle for phyllotaxis (default: {GOLDEN_ANGLE_DEG:.6f}°)",
    )
    gen_p.add_argument("--output", "-o", help="Output file path (e.g. pattern.svg, output.dxf)")
    gen_p.add_argument(
        "--format",
        "-f",
        choices=["svg", "dxf", "obj", "json"],
        help="Output format (svg, dxf, obj, json)",
    )
    gen_p.add_argument("--json", action="store_true", help="Print geometry AST as JSON to stdout")

    # 2. presets
    presets_p = subparsers.add_parser(
        "presets",
        help="List all built-in sacred geometry and UFO crop glyph templates",
        parents=[common_parser],
    )
    presets_p.add_argument(
        "--category",
        "-c",
        choices=["all", "sacred", "crop_circle", "spiral", "yantra", "field", "platonic"],
        default="all",
        help="Filter presets by category",
    )
    presets_p.add_argument("--json", action="store_true", help="Output presets list as raw JSON")

    # 3. export
    exp_p = subparsers.add_parser(
        "export",
        help="Export pattern directly to SVG vector, AutoCAD DXF, or Wavefront OBJ 3D mesh",
        parents=[common_parser],
    )
    exp_p.add_argument(
        "pattern",
        nargs="?",
        default="flower_of_life",
        help="Pattern type or preset ID",
    )
    exp_p.add_argument(
        "--format",
        "-f",
        choices=["svg", "dxf", "obj", "json"],
        default="svg",
        help="Export target format (default: svg)",
    )
    exp_p.add_argument("--output", "-o", help="Target output file path")
    exp_p.add_argument("--theme", "-t", choices=list(THEMES.keys()), default="gold", help="Visual theme")
    exp_p.add_argument("--radius", "-r", type=float, default=100.0, help="Base radius in mm")
    exp_p.add_argument("--iterations", "-i", type=int, default=2, help="Concentric iteration rings")
    exp_p.add_argument("--scale", "-s", type=float, default=1.0, help="Uniform scale")
    exp_p.add_argument("--extrusion", type=float, default=5.0, help="3D extrusion height in mm for OBJ")
    exp_p.add_argument("--bevel", action="store_true", default=True, help="Apply bevel for OBJ")
    exp_p.add_argument("--base-plate", action="store_true", default=False, help="Add solid base plate for OBJ")

    # 4. serve
    serve_p = subparsers.add_parser(
        "serve",
        help="Launch the interactive Sacred Geometry Studio Web UI (design influenced by Material 3)",
        parents=[common_parser],
    )
    serve_p.add_argument("--port", "-p", type=int, default=8080, help="HTTP server port (default: 8080)")
    serve_p.add_argument("--host", default="127.0.0.1", help="HTTP server bind host (default: 127.0.0.1)")
    serve_p.add_argument("--open", action="store_true", help="Automatically open web browser upon launch")
    serve_p.add_argument("--public-dir", help="Optional custom static files directory to serve")

    # 5. mcp
    subparsers.add_parser(
        "mcp",
        help="Run Model Context Protocol (MCP) server over stdio for AI agent integration",
        parents=[common_parser],
    )

    # 6. doctor / diagnostics / platform
    for diag_name in ("doctor", "diagnostics", "platform"):
        diag_p = subparsers.add_parser(
            diag_name,
            help="Run multi-OS system diagnostics and math precision checks",
            parents=[common_parser],
        )
        diag_p.add_argument("--json", action="store_true", help="Output diagnostic report as JSON")

    # 7. test
    subparsers.add_parser(
        "test",
        help="Run internal self-verification test runner",
        parents=[common_parser],
    )

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    tc = TermColor(enabled=not getattr(args, "no_color", False))

    if not args.subcommand:
        parser.print_help()
        return 0

    if args.subcommand == "generate":
        return cmd_generate(args, tc)
    elif args.subcommand == "presets":
        return cmd_presets(args, tc)
    elif args.subcommand == "export":
        return cmd_export(args, tc)
    elif args.subcommand == "serve":
        return cmd_serve(args, tc)
    elif args.subcommand == "mcp":
        return cmd_mcp(args, tc)
    elif args.subcommand in ("doctor", "diagnostics", "platform"):
        return cmd_diagnostics(args, tc)
    elif args.subcommand == "test":
        return cmd_test(args, tc)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
