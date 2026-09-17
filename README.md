# UFO Sacred Geometry Studio & Agroglyph Architecture 🛸📐

[![CI Multi-OS Test Matrix](https://github.com/1nc0gn30/ufo-sacred-geometry/actions/workflows/ci.yml/badge.svg)](https://github.com/1nc0gn30/ufo-sacred-geometry/actions)
[![Python 3.9 - 3.13](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0%20runtime%20(stdlib%20only)-brightgreen.svg)](https://docs.python.org/3/library/)
[![MCP 2024-11-05 Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0%20Stdio-purple.svg)](https://modelcontextprotocol.io/)
[![AutoCAD DXF & Wavefront OBJ](https://img.shields.io/badge/export-SVG%20%7C%20DXF%20%7C%20OBJ%20%7C%20JSON-orange.svg)](https://en.wikipedia.org/wiki/AutoCAD_DXF)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A pure Python 3 standard library engine and Web CAD Studio (design influenced by Material 3) for synthesizing sacred geometry, extraterrestrial agro-glyphs (crop circles), Platonic solids, harmonic vortex manifolds, and multi-format vector/CAD exports (**SVG**, **AutoCAD DXF R12/2000**, **Wavefront OBJ 3D Meshes**, and **JSON AST**).

---

## 🌟 Architectural Highlights

- **Pure Python 3 Standard Library**: Zero third-party runtime dependencies (`math`, `json`, `dataclasses`, `http.server`, `urllib`, `pathlib`).
- **Studio UI (Design influenced by Material 3)**: Clean typography, subtle elevation cards, interactive dual-engine viewport (SVG + 60 FPS HTML5 Canvas), dynamic layer tree inspector, and real-time AST viewer.
- **Model Context Protocol (MCP) Server**: Full JSON-RPC 2.0 stdio server (`tools/list`, `tools/call`, `resources/list`, `resources/read`, `prompts/list`, `prompts/get`) compatible with Claude Desktop, Cursor, Cline, and Antigravity.
- **Multi-Format CAD / CAM Exporters**:
  - **SVG**: Vector graphics with glowing neon drop-shadow filters (`feGaussianBlur`), layer groups (`<g id="...">`), and 6 color themes.
  - **AutoCAD DXF (R2000 AC1015 / R12)**: Standard entities (`LINE`, `CIRCLE`, `ARC`, `LWPOLYLINE`) with AutoCAD Color Index (ACI 1–7) mapping for CNC routers and laser cutters.
  - **Wavefront OBJ + MTL**: 3D embossed medallion meshes and wireframe polyhedra with surface normals (`vn`) and quad/tri faces (`f`) ready for slicing in Cura/PrusaSlicer.
  - **JSON AST**: Serialized node tree with bounding boxes, layer styles, and parameters.
- **20+ Curated Parametric Presets**: Across 5 cosmological domains (Classical Sacred Geometry, Hermetic & Polyhedral, Golden Ratio Harmonics, Vedic Yantras, Extraterrestrial Agro-Glyphs).

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  🛸 UFO Sacred Geometry Studio    |  CAD / CAM Vector Engineering Matrix    │
 ├───────────────────┬───────────────────────────────────┬─────────────────────┤
 │ Presets Gallery   │  Interactive Viewport (SVG / 2D)  │ Parameter Controls  │
 │ ───────────────── │ ───────────────────────────────── │ ─────────────────── │
 │ • Flower of Life  │              ╭───╮                │ Radius:   100.0 mm  │
 │ • Metatron's Cube │           ╭──┤   ├──╮             │ Iterations:      3  │
 │ • Sri Yantra      │          ╭╯  ╰───╯  ╰╮            │ Symmetry:       12  │
 │ • Milk Hill 409   │         ╭┤     ✡     ├╮           │ Golden Ratio: 1.618 │
 │ • Julia Set 151   │          ╰╮  ╭───╮  ╭╯            │ Stroke:      1.5 px │
 │ • Barbury Castle  │           ╰──┤   ├──╯             │ Theme:  Sacred Gold │
 │ • Merkaba Star    │              ╰───╯                │ ─────────────────── │
 │ • Torus Knot      │                                   │ [ SVG ] [ DXF CNC ] │
 │ • Phyllotaxis     │ Pan: [Drag] Zoom: [Wheel] Reset   │ [ 3D OBJ ] [ JSON ] │
 └───────────────────┴───────────────────────────────────┴─────────────────────┘
```

---

## 📐 Mathematical Foundations

### 1. Golden Ratio & Phyllotaxis Harmonics
- **Golden Ratio ($\Phi$)**:
  $$\Phi = \frac{1 + \sqrt{5}}{2} \approx 1.618033988749895$$
- **Golden Angle ($\theta$)**:
  $$\theta = 360^\circ \times \left(1 - \frac{1}{\Phi}\right) \approx 137.50776405003785^\circ$$
- **Vogel Phyllotaxis Model**:
  $$r_n = c \sqrt{n}, \quad \theta_n = n \times 137.507764^\circ$$
  Generates optimal botanical packing (sunflowers, pinecones) and connects Fibonacci parastichy spirals $(F_k, F_{k+1})$ such as $(21, 34)$ or $(34, 55)$.

### 2. Metatron's Cube & Platonic Polyhedra
- **Fruit of Life**: 13 nodal centers $(0, 2R, 4R)$ arranged in hexagonal symmetry $\mathbb{Z}_6$.
- **Complete Graph ($K_{13}$)**: Connecting all 13 centers produces $\binom{13}{2} = 78$ sacred line segments.
- **Euler Characteristic**:
  $$V - E + F = 2$$
  Yields exact 3D coordinates for all 5 Platonic Solids (Tetrahedron, Hexahedron/Cube, Octahedron, Icosahedron, Dodecahedron) with 3D Euler rotation matrices:
  $$R_x(\alpha) \cdot R_y(\beta) \cdot R_z(\gamma)$$

### 3. Vedic Sri Yantra (Cosmic Navayoni Chakra)
- 9 interlocking primary triangles (4 upright Shiva pointing upward, 5 inverted Shakti pointing downward).
- Intersect to form 43 secondary sub-triangles, surrounding the central bindu point, enveloped by 8-petal and 16-petal lotus circles and the 4-gate Bhupura citadel.

### 4. Extraterrestrial Agro-Glyphs (Crop Circles)
- **Milk Hill 2001 (Triple Julia Set)**: 6 curved spiral arms consisting of 409 mathematically graduating circles discovered in Wiltshire, UK.
- **Stonehenge 1996 (Julia Set)**: 151 circles forming a computer-generated Julia set fractal curve.
- **Barbury Castle 1991 (Tetrahedral Ratchet)**: 3-lobed ratchet spiral inscribed in a spherical triangle.
- **Chilbolton 2001 (Arecibo Reply)**: $73 \times 23$ binary telemetry matrix encoding DNA modifications and silicon biochemistry.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/1nc0gn30/ufo-sacred-geometry.git
cd ufo-sacred-geometry

# Install in editable mode
pip install -e .

# Or run directly with zero installation via python3
python3 -m ufo_sacred_geometry.cli --help
```

---

## 🖥️ UFO Sacred Geometry Studio Web UI

Launch the embedded CAD Studio locally (design influenced by Material 3) with pure Python standard library:

```bash
# Launch Studio UI on default port 8080 (auto-opens browser)
ufo-sacred-geometry serve

# Custom host and port
ufo-sacred-geometry serve --host 0.0.0.0 --port 9000 --no-browser
```

### REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves Studio Web App (design influenced by Material 3) |
| `GET` | `/api/presets` | List all 20+ presets with parameters and metadata |
| `POST` | `/api/generate` | Generate AST and vector SVG markup |
| `POST` | `/api/export-svg` | Download styled SVG vector file |
| `POST` | `/api/export-dxf` | Download AutoCAD DXF file for CNC/laser cutting |
| `POST` | `/api/export-obj` | Download 3D Wavefront OBJ mesh file |
| `GET` | `/api/stats` | Return system capabilities and primitive registry |
| `GET` | `/api/diagnostics` | High-precision float benchmarking and OS info |

---

## 💻 Command Line Interface (CLI)

The `ufo-sacred-geometry` CLI (also available as `sacred-geometry` and `ufogeom`) provides complete scripting capabilities:

```bash
# List all presets
ufo-sacred-geometry presets

# Filter presets by category in JSON format
ufo-sacred-geometry presets --category "Classical Sacred Geometry" --json

# Generate Flower of Life SVG with Sacred Gold theme
ufo-sacred-geometry generate flower_of_life --radius 120 --iterations 3 --theme gold --output flower.svg

# Generate Metatron's Cube DXF for CNC routing
ufo-sacred-geometry export-dxf metatrons_cube --radius 100 --output metatron.dxf

# Generate 3D printable Merkaba Medallion OBJ mesh with cylinder base
ufo-sacred-geometry export-obj merkaba_star --radius 80 --relief 3.5 --base-type cylinder --output merkaba.obj

# Generate Milk Hill 409-circle crop circle
ufo-sacred-geometry generate crop_circle_milk_hill --scale 250 --theme neon_matrix --output milk_hill.svg

# Run diagnostics and math benchmarking
ufo-sacred-geometry diagnostics
```

---

## 🤖 Model Context Protocol (MCP) Server Setup

Integrate `ufo-sacred-geometry` directly with AI agents, Claude Desktop, Cursor, and Cline using the stdio JSON-RPC 2.0 protocol.

### Claude Desktop Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "ufo-sacred-geometry": {
      "command": "python3",
      "args": ["-m", "ufo_sacred_geometry.mcp_server"]
    }
  }
}
```

### Available MCP Tools

1. `geometry_generate`: Synthesize geometry AST and SVG with parametric controls.
2. `geometry_export_svg`: Export SVG with glow filters and custom themes.
3. `geometry_export_dxf`: Export AutoCAD DXF R12/2000 files for laser cutters.
4. `geometry_export_obj`: Export 3D Wavefront OBJ models for 3D printing.
5. `geometry_presets`: Query pattern catalog and historical metadata.
6. `geometry_phyllotaxis`: Generate Vogel sunflower disc spirals.
7. `geometry_diagnostics`: Inspect floating-point precision and hardware capabilities.

---

## 🐍 Python API Reference

```python
import ufo_sacred_geometry as geom

# 1. Generate Flower of Life AST
ast = geom.generate_flower_of_life(radius=50.0, rings=3, outer_rings=True)
print(f"Total Circles: {len(ast.circles)}")

# 2. Export to SVG with Sacred Gold Theme & Glow
svg_code = geom.export_svg(ast, theme="dark_gold", glow=True, file_path="flower.svg")

# 3. Export to AutoCAD DXF for Laser Cutting
dxf_code = geom.export_dxf(ast, file_path="flower.dxf")

# 4. Export to 3D Embossed Wavefront OBJ Medallion
obj_code = geom.export_obj(ast, file_path="flower.obj", relief_depth=4.0, base_type="cylinder")

# 5. Generate Platonic Solid 3D Projections
cube_ast = geom.generate_platonic_solid_projection(solid_type="dodecahedron", size=140.0, rot_x=0.55, rot_y=0.75)

# 6. Generate 409-Circle Milk Hill Crop Circle
milk_hill = geom.generate_milk_hill_glyph(scale=200.0)
print(f"Milk Hill Circles: {len(milk_hill.circles)}")  # 409 circles
```

---

## 🎨 Color Themes

| Theme Key | Visual Description | Background | Primary Stroke | Glow / Accent |
|---|---|---|---|---|
| `gold` / `dark_gold` | Sacred 24K Temple Gold | `#0f0f18` | `#ffd700` | `#ffaa00` |
| `blueprint` | Technical Blueprint | `#0e2a47` | `#e0fbfc` | `#48cae4` |
| `neon_matrix` | Matrix Phosphor Green | `#050805` | `#00ff66` | `#39ff14` |
| `obsidian_dark` | Obsidian Cosmic Purple | `#180828` | `#e056fd` | `#bf00ff` |
| `light_minimal` | Clean Slate (Material 3 Inspired) | `#ffffff` | `#1a1a24` | `#718093` |
| `monochrome_laser`| High-Contrast CNC / Laser Cut | `#000000` | `#ffffff` | None |

---

## 🧪 Comprehensive Test Suite

Run the 100% standard library test suite with pytest:

```bash
# Run all tests across models, generators, exporters, CLI, MCP, and UI server
pytest -v

# Run with test coverage
pytest --cov=ufo_sacred_geometry -v
```

### Test Coverage Architecture

- `tests/test_compat.py`: Cross-platform OS detection, atomic I/O, path normalization (Linux, macOS, Windows, Termux).
- `tests/test_models.py`: 2D/3D affine transformations, bounding boxes, AST serialization/deserialization.
- `tests/test_generators.py`: Parametric geometry generators, Platonic solids, Vogel phyllotaxis, agro-glyphs.
- `tests/test_exporters.py`: SVG XML validation, AutoCAD DXF R2000 structure, Wavefront OBJ/MTL topology.
- `tests/test_cli.py`: Subcommand argument parsing, exit codes, file generation.
- `tests/test_mcp_server.py`: JSON-RPC 2.0 protocol methods, tool handlers, resources, and prompts.
- `tests/test_ui_server.py`: HTTP REST server endpoints, static file delivery, and CORS handling.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.
