# 🛸 UFO Sacred Geometry & Crop Circle Synthesizer

> **Parametric CAD Vector Generator, Agro-glyph Harmonics, 3D Mesh Synthesizer, FastMCP Server & Google Material 3 Web Studio.**
> 
> 100% Pure Python Standard Library (Zero External Runtime Dependencies). Compatible with Python 3.9–3.13 on Linux, macOS, Windows, and Termux.

---

## 🌌 Overview

`ufo-sacred-geometry` is an autonomous computational geometry engine designed to mathematically synthesize, render, and export classical sacred geometry, extraterrestrial crop circle agro-glyphs, Golden Ratio harmonics, and Platonic regular polyhedra.

It features publication-grade multi-format exporters:
- **Scalable Vector Graphics (SVG)** with custom Gaussian glow filters, layer grouping, and 5 color themes.
- **AutoCAD DXF (R12/2000)** for CNC milling, waterjet cutters, laser cutters, and plotters.
- **Wavefront 3D OBJ & MTL** with parametric extrusion, base medallion framing, and surface relief.
- **FastMCP Protocol** (JSON-RPC 2.0 stdio server) connecting AI coding agents (Claude Desktop, Cursor, Cline).
- **Google Material 3 Light Mode Web Studio** with real-time SVG canvas rendering, theme switching, and interactive export.

---

## ✨ Features

- **25+ Curated Geometric Archetypes & Presets**:
  - **Classical Sacred Geometry**: Seed of Life, Flower of Life (19 & 61 circles), Egg of Life, Fruit of Life, Tree of Life (Otz Chiim).
  - **Hermetic & Polyhedral Matrix**: Metatron's Cube (78 lines, 13 nodal circles), 5 Platonic Solids (Tetrahedron, Cube, Octahedron, Icosahedron, Dodecahedron), Merkaba Star Tetrahedron.
  - **Golden Ratio & Harmonics**: Fibonacci Whirling Squares, Logarithmic Golden Spiral ($\Phi = 1.6180339$), Sunflower Phyllotaxis (Vogel model with Golden Angle $137.507764^\circ$), Golden Triangle Kepler Spiral.
  - **Vedic & Mystical Yantras**: Authentic Sri Yantra (9 interlocking Shiva/Shakti triangles, 43 sub-triangles, 24 lotus petals, 4-gate Bhupura citadel), Vesica Piscis.
  - **Extraterrestrial Agro-Glyphs**: Milk Hill 409-Circle Julia Set (2001), Barbury Castle Tetrahedron (1991), Chilbolton Binary Code (2001), Triskele Spiral (1996), Torus Vortex Field, (p,q) Torus Knots.
- **Multi-Format Vector & CAD Exporters**:
  - Direct SVG markup with selectable themes (`dark_gold`, `blueprint`, `neon_ufo`, `cosmic_purple`, `light_minimal`) and SVG `<filter>` luminescence.
  - Standard AutoCAD DXF entities (`LINE`, `CIRCLE`, `ARC`, `LWPOLYLINE`) with ACI color mapping.
  - Wavefront OBJ 3D mesh with vertex normal calculation and `.mtl` material shading.
- **Pure Python Standard Library**:
  - Zero external dependencies (`math`, `json`, `dataclasses`, `pathlib`, `http.server`, `urllib`).
  - Cross-platform atomic file I/O and POSIX/Windows path safety.
- **FastMCP Protocol Integration**:
  - Full Model Context Protocol server exposing `geometry_generate`, `geometry_export_svg`, `geometry_export_dxf`, `geometry_export_obj`, `geometry_presets`, `geometry_phyllotaxis`, and `geometry_diagnostics`.

---

## 🚀 Installation & Quickstart

```bash
# Clone the repository
git clone https://github.com/1nc0gn30/ufo-sacred-geometry.git
cd ufo-sacred-geometry

# Install locally in editable mode (or zero-install: run directly with Python)
pip install -e .
```

---

## 💻 CLI Usage

```bash
# List all 25+ geometry & agro-glyph presets
ufo-sacred-geometry presets

# Generate Flower of Life SVG
ufo-sacred-geometry generate flower_of_life --theme gold --output flower.svg

# Generate AutoCAD DXF for laser cutting
ufo-sacred-geometry generate metatrons_cube --format dxf --output metatron.dxf

# Generate 3D OBJ relief medallion for 3D printing
ufo-sacred-geometry generate sri_yantra --format obj --output sri_yantra.obj

# Launch the Google Material 3 Studio Web UI
ufo-sacred-geometry serve --port 8080

# Run Model Context Protocol server over stdio
ufo-sacred-geometry mcp

# Run internal test suite
ufo-sacred-geometry test
```

---

## 🤖 Model Context Protocol (MCP) Setup

Add to your `claude_desktop_config.json` or Cursor/Cline MCP settings:

```json
{
  "mcpServers": {
    "ufo-sacred-geometry": {
      "command": "python3",
      "args": ["-m", "ufo_sacred_geometry.cli", "mcp"]
    }
  }
}
```

---

## 🧪 Testing & CI

```bash
pytest tests/ -v
```

100% test pass rate across all modules on Linux, macOS, and Windows.

---

## 📜 License

MIT License. Designed with precision by the Google Sacred Geometry Studio Team.
