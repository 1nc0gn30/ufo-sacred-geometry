"""
Model Context Protocol (MCP) Server for UFO Sacred Geometry
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implements the full Model Context Protocol specification over stdio with
JSON-RPC 2.0 transport for AI agents and LLM tool integration.
"""

from __future__ import annotations

import json
import math
import os
import platform
import sys
import time
import traceback
from typing import Any, Callable, Dict, List, Optional

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
)


class MCPServer:
    """Standard Model Context Protocol (MCP) Server implementing JSON-RPC 2.0 over stdio."""

    PROTOCOL_VERSION = "2024-11-05"

    def __init__(self, name: str = "ufo-sacred-geometry", version: str = __version__) -> None:
        self.name = name
        self.version = version
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.tool_handlers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.prompts: Dict[str, Dict[str, Any]] = {}

        self._register_tools()
        self._register_resources()
        self._register_prompts()

    def _log(self, message: str) -> None:
        """Logs diagnostic message to stderr (keeping stdout pure JSON-RPC stream)."""
        sys.stderr.write(f"[{self.name} MCP] {message}\n")
        sys.stderr.flush()

    def _register_tools(self) -> None:
        # Tool 1: geometry_generate
        self.register_tool(
            name="geometry_generate",
            description="Generate sacred geometry or crop circle pattern AST and vector SVG with custom mathematical parameters and visual theme.",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Pattern type or preset ID: flower_of_life, metatrons_cube, fibonacci_spiral, sri_yantra, crop_circle, merkaba, torus, phyllotaxis, or a preset ID.",
                        "default": "flower_of_life",
                    },
                    "radius": {
                        "type": "number",
                        "description": "Base radius in millimeters/units (e.g. 50.0 - 180.0).",
                        "default": 100.0,
                    },
                    "iterations": {
                        "type": "integer",
                        "description": "Number of concentric rings or recursion depth (1-8).",
                        "default": 2,
                    },
                    "petals": {
                        "type": "integer",
                        "description": "Petal count for Sri Yantra or mandala structures (e.g. 8, 16, 24).",
                        "default": 16,
                    },
                    "scale": {
                        "type": "number",
                        "description": "Affine uniform scale multiplier.",
                        "default": 1.0,
                    },
                    "theme": {
                        "type": "string",
                        "description": "Color theme palette.",
                        "enum": ["gold", "blueprint", "neon_matrix", "obsidian_dark", "light_minimal"],
                        "default": "gold",
                    },
                    "glyph_type": {
                        "type": "string",
                        "description": "Crop glyph variant (for crop_circle): julia_set, pi_glyph, barbury_castle.",
                        "default": "julia_set",
                    },
                    "seed_count": {
                        "type": "integer",
                        "description": "Seed count for phyllotaxis distribution (e.g. 100-1000).",
                        "default": 300,
                    },
                    "divergence_angle": {
                        "type": "number",
                        "description": "Divergence angle in degrees for phyllotaxis (default: 137.507764 - Golden Angle).",
                        "default": 137.507764,
                    },
                    "include_svg": {
                        "type": "boolean",
                        "description": "Whether to return the compiled SVG XML text alongside AST metadata.",
                        "default": True,
                    },
                },
                "required": ["pattern"],
            },
            handler=self._tool_geometry_generate,
        )

        # Tool 2: geometry_export_svg
        self.register_tool(
            name="geometry_export_svg",
            description="Export sacred geometry pattern directly as clean, scalable vector SVG XML markup with theme styling and glow filters.",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Pattern type or preset ID.",
                        "default": "metatrons_cube",
                    },
                    "theme": {
                        "type": "string",
                        "description": "Color theme.",
                        "enum": ["gold", "blueprint", "neon_matrix", "obsidian_dark", "light_minimal"],
                        "default": "gold",
                    },
                    "radius": {"type": "number", "default": 120.0},
                    "iterations": {"type": "integer", "default": 2},
                    "stroke_width": {"type": "number", "description": "Custom stroke width override."},
                    "glow": {"type": "boolean", "description": "Enable glow drop-shadow filter.", "default": True},
                    "scale": {"type": "number", "default": 1.0},
                },
                "required": ["pattern"],
            },
            handler=self._tool_geometry_export_svg,
        )

        # Tool 3: geometry_export_dxf
        self.register_tool(
            name="geometry_export_dxf",
            description="Export pattern as standard AutoCAD DXF format (R12/2000) for CNC machining, waterjet, laser cutters, and CAD software.",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Pattern type or preset ID.", "default": "flower_of_life"},
                    "radius": {"type": "number", "default": 100.0},
                    "iterations": {"type": "integer", "default": 2},
                    "scale": {"type": "number", "default": 1.0},
                },
                "required": ["pattern"],
            },
            handler=self._tool_geometry_export_dxf,
        )

        # Tool 4: geometry_export_obj
        self.register_tool(
            name="geometry_export_obj",
            description="Export pattern as 3D embossed mesh (Wavefront OBJ) for 3D printing, Blender, Unreal Engine, and spatial rendering.",
            input_schema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Pattern type or preset ID.", "default": "merkaba"},
                    "radius": {"type": "number", "default": 120.0},
                    "extrusion": {"type": "number", "description": "3D extrusion relief height in millimeters.", "default": 5.0},
                    "bevel": {"type": "boolean", "description": "Apply bevel chamfer.", "default": True},
                    "base_plate": {"type": "boolean", "description": "Add solid structural base plate disc.", "default": False},
                    "scale": {"type": "number", "default": 1.0},
                },
                "required": ["pattern"],
            },
            handler=self._tool_geometry_export_obj,
        )

        # Tool 5: geometry_presets
        self.register_tool(
            name="geometry_presets",
            description="Return comprehensive catalog of built-in sacred geometry, Platonic solid matrices, and UFO crop glyph templates with harmonic ratios.",
            input_schema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category filter: sacred, crop_circle, spiral, yantra, field, or all.",
                        "enum": ["all", "sacred", "crop_circle", "spiral", "yantra", "field"],
                        "default": "all",
                    }
                },
            },
            handler=self._tool_geometry_presets,
        )

        # Tool 6: geometry_phyllotaxis
        self.register_tool(
            name="geometry_phyllotaxis",
            description="Generate Fibonacci phyllotaxis disc spiral (seed distribution, Golden Angle divergence, parastichy spiral rays).",
            input_schema={
                "type": "object",
                "properties": {
                    "seed_count": {"type": "integer", "description": "Total seed count.", "default": 300},
                    "divergence_angle": {
                        "type": "number",
                        "description": "Divergence angle in degrees (Golden Angle = 137.507764°).",
                        "default": 137.507764,
                    },
                    "c_factor": {"type": "number", "description": "Radial scaling factor.", "default": 5.5},
                    "marker_radius": {"type": "number", "description": "Seed marker radius.", "default": 2.4},
                    "theme": {
                        "type": "string",
                        "enum": ["gold", "blueprint", "neon_matrix", "obsidian_dark", "light_minimal"],
                        "default": "gold",
                    },
                },
            },
            handler=self._tool_geometry_phyllotaxis,
        )

        # Tool 7: geometry_diagnostics
        self.register_tool(
            name="geometry_diagnostics",
            description="Run comprehensive multi-OS system diagnostics, benchmark floating point math precision, check CAD/vector exporter readiness.",
            input_schema={"type": "object", "properties": {}},
            handler=self._tool_geometry_diagnostics,
        )

        # Tool 8: geometry_star_polyhedron
        self.register_tool(
            name="geometry_star_polyhedron",
            description="Generate 3D Kepler-Poinsot or Archimedean star polyhedron wireframe projection (cuboctahedron, small_stellated_dodecahedron, great_stellated_dodecahedron, icosidodecahedron, truncated_icosahedron).",
            input_schema={
                "type": "object",
                "properties": {
                    "poly_type": {
                        "type": "string",
                        "description": "Star polyhedron type (cuboctahedron, small_stellated_dodecahedron, great_stellated_dodecahedron, icosidodecahedron, truncated_icosahedron).",
                        "default": "cuboctahedron",
                    },
                    "size": {"type": "number", "default": 130.0},
                    "rot_x": {"type": "number", "default": 0.55},
                    "rot_y": {"type": "number", "default": 0.75},
                    "rot_z": {"type": "number", "default": 0.0},
                    "perspective": {"type": "boolean", "default": False},
                    "theme": {"type": "string", "default": "gold"},
                },
            },
            handler=self._tool_geometry_star_polyhedron,
        )

        # Tool 9: geometry_sacred_resonance
        self.register_tool(
            name="geometry_sacred_resonance",
            description="Generate sacred harmonic resonance cymatic Chladni nodal plate geometry for Solfeggio (174-963Hz), Schumann (7.83Hz), or Planetary frequencies.",
            input_schema={
                "type": "object",
                "properties": {
                    "frequency_key": {
                        "type": "string",
                        "description": "Frequency identifier (e.g. solfeggio_528, solfeggio_396, solfeggio_417, solfeggio_639, solfeggio_741, solfeggio_852, solfeggio_963, schumann_fundamental).",
                        "default": "solfeggio_528",
                    },
                    "radius": {"type": "number", "default": 160.0},
                    "harmonics_count": {"type": "integer", "default": 6},
                    "nodal_lines": {"type": "integer", "default": 12},
                    "theme": {"type": "string", "default": "gold"},
                },
            },
            handler=self._tool_geometry_sacred_resonance,
        )

    def _register_resources(self) -> None:
        self.resources["geometry://presets"] = {
            "uri": "geometry://presets",
            "name": "Sacred Geometry & Crop Glyph Preset Catalog",
            "description": "Full JSON catalog of all built-in sacred geometry patterns, mathematical parameters, and historical origins.",
            "mimeType": "application/json",
        }
        self.resources["geometry://catalog"] = {
            "uri": "geometry://catalog",
            "name": "Harmonic Proportions & Mathematical Constants",
            "description": "Sacred ratio constants (Phi, Pi, Sqrt(2), Sqrt(3), Sqrt(5), Euler), Platonic solid vertices, and dimensional projection matrices.",
            "mimeType": "application/json",
        }

    def _register_prompts(self) -> None:
        self.prompts["geometry_create_crop_circle"] = {
            "name": "geometry_create_crop_circle",
            "description": "Interactive prompt guidance for designing authentic UFO agroglyphs (Milk Hill Julia set, Pi glyph, Barbury Castle) with harmonic ground-flattening parameters.",
            "arguments": [
                {
                    "name": "glyph_type",
                    "description": "Type of crop circle (julia_set, pi_glyph, barbury_castle, sunburst, vortex).",
                    "required": True,
                },
                {
                    "name": "field_diameter_meters",
                    "description": "Real-world field diameter in meters (e.g. 150m for Milk Hill).",
                    "required": False,
                },
            ],
        }
        self.prompts["geometry_create_mandala"] = {
            "name": "geometry_create_mandala",
            "description": "Interactive prompt guidance for synthesizing multi-layered sacred geometry mandalas with concentric harmonics, symmetry folds, and Sri Yantra integration.",
            "arguments": [
                {
                    "name": "symmetry_folds",
                    "description": "Rotational symmetry fold count (e.g. 6, 8, 12, 16, 24).",
                    "required": False,
                },
                {
                    "name": "theme",
                    "description": "Color palette theme (gold, blueprint, neon_matrix, obsidian_dark, light_minimal).",
                    "required": False,
                },
            ],
        }

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> None:
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
        }
        self.tool_handlers[name] = handler

    # -------------------------------------------------------------------------
    # Tool Handlers
    # -------------------------------------------------------------------------
    def _tool_geometry_generate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pattern_name = params.get("pattern", "flower_of_life")
        radius = float(params.get("radius", 100.0))
        iterations = int(params.get("iterations", 2))
        petals = int(params.get("petals", 16))
        scale = float(params.get("scale", 1.0))
        theme = params.get("theme", "gold")
        glyph_type = params.get("glyph_type", "julia_set")
        seed_count = int(params.get("seed_count", 300))
        divergence_angle = float(params.get("divergence_angle", GOLDEN_ANGLE_DEG))
        include_svg = bool(params.get("include_svg", True))

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

        stats = ast.stats() if hasattr(ast, "stats") else {}
        bb = ast.bounds() if hasattr(ast, "bounds") else None
        bounds_dict = {
            "min_x": round(bb.min_x, 3),
            "min_y": round(bb.min_y, 3),
            "max_x": round(bb.max_x, 3),
            "max_y": round(bb.max_y, 3),
            "width": round(bb.width, 3),
            "height": round(bb.height, 3),
        } if bb else {}

        response_data: Dict[str, Any] = {
            "name": pattern_name,
            "title": getattr(ast, "title", pattern_name),
            "version": __version__,
            "primitive_count": stats.get("total_primitives", len(getattr(ast, "lines", [])) + len(getattr(ast, "circles", []))),
            "total_primitives": stats.get("total_primitives", len(getattr(ast, "lines", [])) + len(getattr(ast, "circles", []))),
            "bounds": bounds_dict,
            "parameters": getattr(ast, "parameters", {}),
            "tags": getattr(ast, "tags", []),
            "stats": stats,
        }

        if include_svg:
            response_data["svg"] = export_svg(ast, theme=theme)

        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(response_data, indent=2),
                }
            ],
            "isError": False,
        }

    def _tool_geometry_export_svg(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pattern_name = params.get("pattern", "metatrons_cube")
        theme = params.get("theme", "gold")
        radius = float(params.get("radius", 120.0))
        iterations = int(params.get("iterations", 2))
        stroke_width = params.get("stroke_width")
        if stroke_width is not None:
            stroke_width = float(stroke_width)
        glow = bool(params.get("glow", True))
        scale = float(params.get("scale", 1.0))

        ast = generate_pattern(pattern_name, radius=radius, iterations=iterations, theme=theme)
        if abs(scale - 1.0) > 1e-4:
            ast.scale(scale)

        svg_text = export_svg(ast, theme=theme, stroke_width=stroke_width, glow=glow)
        return {
            "content": [
                {
                    "type": "text",
                    "text": svg_text,
                }
            ],
            "isError": False,
        }

    def _tool_geometry_export_dxf(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pattern_name = params.get("pattern", "flower_of_life")
        radius = float(params.get("radius", 100.0))
        iterations = int(params.get("iterations", 2))
        scale = float(params.get("scale", 1.0))

        ast = generate_pattern(pattern_name, radius=radius, iterations=iterations)
        if abs(scale - 1.0) > 1e-4:
            ast.scale(scale)

        dxf_text = export_dxf(ast)
        return {
            "content": [
                {
                    "type": "text",
                    "text": dxf_text,
                }
            ],
            "isError": False,
        }

    def _tool_geometry_export_obj(self, params: Dict[str, Any]) -> Dict[str, Any]:
        pattern_name = params.get("pattern", "merkaba")
        radius = float(params.get("radius", 120.0))
        extrusion = float(params.get("extrusion", 5.0))
        base_plate = bool(params.get("base_plate", False))
        scale = float(params.get("scale", 1.0))

        ast = generate_pattern(pattern_name, radius=radius)
        if abs(scale - 1.0) > 1e-4:
            ast.scale(scale)

        obj_text = export_obj(ast, extrusion=extrusion, medallion_base=base_plate)
        return {
            "content": [
                {
                    "type": "text",
                    "text": obj_text,
                }
            ],
            "isError": False,
        }

    def _tool_geometry_presets(self, params: Dict[str, Any]) -> Dict[str, Any]:
        category = params.get("category", "all")
        presets = list_presets(category)
        data = [p.to_dict() for p in presets]
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "count": len(data),
                            "category": category,
                            "presets": data,
                        },
                        indent=2,
                    ),
                }
            ],
            "isError": False,
        }

    def _tool_geometry_phyllotaxis(self, params: Dict[str, Any]) -> Dict[str, Any]:
        seed_count = int(params.get("seed_count", 300))
        divergence_angle = float(params.get("divergence_angle", GOLDEN_ANGLE_DEG))
        c_factor = float(params.get("c_factor", 12.0))
        marker_radius = float(params.get("marker_radius", 3.0))
        theme = params.get("theme", "gold")

        ast = generate_phyllotaxis(
            count=seed_count,
            scaling=c_factor,
            divergence_angle_deg=divergence_angle,
            dot_radius=marker_radius,
        )
        svg_text = export_svg(ast, theme=theme)

        stats = ast.stats() if hasattr(ast, "stats") else {}
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "title": "Sunflower Phyllotaxis",
                            "seed_count": seed_count,
                            "divergence_angle_deg": divergence_angle,
                            "golden_angle_ref_deg": GOLDEN_ANGLE_DEG,
                            "phi": PHI,
                            "total_primitives": stats.get("total_primitives", seed_count),
                            "svg": svg_text,
                        },
                        indent=2,
                    ),
                }
            ],
            "isError": False,
        }

    def _tool_geometry_diagnostics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Benchmark floating-point math & geometry generation
        t0 = time.perf_counter()
        test_ast = generate_pattern("metatrons_cube", radius=100.0)
        svg_sample = export_svg(test_ast)
        dxf_sample = export_dxf(test_ast)
        obj_sample = export_obj(test_ast)
        t_elapsed_ms = (time.perf_counter() - t0) * 1000.0

        stats = test_ast.stats() if hasattr(test_ast, "stats") else {}

        diag = {
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
            "capabilities": {
                "generators": [
                    "flower_of_life",
                    "seed_of_life",
                    "egg_of_life",
                    "fruit_of_life",
                    "tree_of_life",
                    "metatrons_cube",
                    "fibonacci_spiral",
                    "sri_yantra",
                    "crop_circle (milk_hill, julia_set, barbury_castle, chilbolton, triskele)",
                    "merkaba",
                    "torus",
                    "torus_knot",
                    "vesica_piscis",
                    "phyllotaxis",
                ],
                "themes": list(THEMES.keys()),
                "exporters": ["SVG (Vector)", "DXF (AutoCAD R12/2000)", "OBJ (Wavefront 3D Mesh)", "JSON AST"],
                "preset_count": len(PRESETS_CATALOG),
            },
            "benchmark": {
                "test_pattern": "metatrons_cube",
                "primitives_generated": stats.get("total_primitives", 91),
                "svg_bytes": len(svg_sample.encode("utf-8")),
                "dxf_bytes": len(dxf_sample.encode("utf-8")),
                "obj_bytes": len(obj_sample.encode("utf-8")),
                "total_generation_and_export_time_ms": round(t_elapsed_ms, 3),
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        return {
            "content": [{"type": "text", "text": json.dumps(diag, indent=2)}],
            "isError": False,
        }

    def _tool_geometry_star_polyhedron(self, args: Dict[str, Any]) -> Dict[str, Any]:
        from .generators.star_polyhedra import generate_star_polyhedron_projection
        poly_type = str(args.get("poly_type", "cuboctahedron"))
        size = float(args.get("size", 130.0))
        rot_x = float(args.get("rot_x", 0.55))
        rot_y = float(args.get("rot_y", 0.75))
        rot_z = float(args.get("rot_z", 0.0))
        perspective = bool(args.get("perspective", False))
        theme = str(args.get("theme", "gold"))

        ast = generate_star_polyhedron_projection(
            poly_type=poly_type,
            size=size,
            rot_x=rot_x,
            rot_y=rot_y,
            rot_z=rot_z,
            perspective=perspective,
        )
        svg_out = export_svg(ast, theme=theme)
        res_data = {
            "title": ast.title,
            "poly_type": poly_type,
            "vertices_3d_count": len(ast.points3d),
            "lines_count": len(ast.lines),
            "svg_xml": svg_out,
            "parameters": ast.parameters,
        }
        return {
            "content": [{"type": "text", "text": json.dumps(res_data, indent=2)}],
            "isError": False,
        }

    def _tool_geometry_sacred_resonance(self, args: Dict[str, Any]) -> Dict[str, Any]:
        from .generators.star_polyhedra import generate_cymatic_resonance_pattern, get_sacred_frequency
        freq_key = str(args.get("frequency_key", "solfeggio_528"))
        radius = float(args.get("radius", 160.0))
        harmonics_count = int(args.get("harmonics_count", 6))
        nodal_lines = int(args.get("nodal_lines", 12))
        theme = str(args.get("theme", "gold"))

        ast = generate_cymatic_resonance_pattern(
            frequency_key=freq_key,
            radius=radius,
            harmonics_count=harmonics_count,
            nodal_lines=nodal_lines,
        )
        freq_info = get_sacred_frequency(freq_key)
        svg_out = export_svg(ast, theme=theme)
        res_data = {
            "title": ast.title,
            "frequency_hz": freq_info.freq_hz,
            "chakra_or_planet": freq_info.chakra_or_planet,
            "description": freq_info.description,
            "circles_count": len(ast.circles),
            "lines_count": len(ast.lines),
            "svg_xml": svg_out,
        }
        return {
            "content": [{"type": "text", "text": json.dumps(res_data, indent=2)}],
            "isError": False,
        }

    # -------------------------------------------------------------------------
    # JSON-RPC 2.0 Dispatch Engine
    # -------------------------------------------------------------------------
    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if not method:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": "Invalid Request: missing method"},
            }

        try:
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": self.PROTOCOL_VERSION,
                        "capabilities": {
                            "tools": {},
                            "resources": {},
                            "prompts": {},
                        },
                        "serverInfo": {
                            "name": self.name,
                            "version": self.version,
                        },
                    },
                }

            elif method in ("notifications/initialized", "initialized"):
                # Initialized notification; no response required
                return None

            elif method == "ping":
                return {"jsonrpc": "2.0", "id": req_id, "result": {}}

            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": list(self.tools.values())},
                }

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                if tool_name not in self.tool_handlers:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {
                            "code": -32601,
                            "message": f"Tool '{tool_name}' not found. Available tools: {', '.join(self.tools.keys())}",
                        },
                    }
                handler = self.tool_handlers[tool_name]
                tool_result = handler(arguments)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": tool_result,
                }

            elif method == "resources/list":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"resources": list(self.resources.values())},
                }

            elif method == "resources/read":
                uri = params.get("uri")
                if uri == "geometry://presets":
                    catalog_data = [p.to_dict() for p in list_presets()]
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "contents": [
                                {
                                    "uri": "geometry://presets",
                                    "mimeType": "application/json",
                                    "text": json.dumps(catalog_data, indent=2),
                                }
                            ]
                        },
                    }
                elif uri == "geometry://catalog":
                    catalog_info = {
                        "constants": {
                            "phi": PHI,
                            "golden_angle_deg": GOLDEN_ANGLE_DEG,
                            "pi": math.pi,
                            "e": math.e,
                            "sqrt_2": math.sqrt(2.0),
                            "sqrt_3": math.sqrt(3.0),
                            "sqrt_5": math.sqrt(5.0),
                        },
                        "platonic_solids": {
                            "tetrahedron": {"faces": 4, "vertices": 4, "edges": 6, "element": "Fire"},
                            "hexahedron_cube": {"faces": 6, "vertices": 8, "edges": 12, "element": "Earth"},
                            "octahedron": {"faces": 8, "vertices": 6, "edges": 12, "element": "Air"},
                            "dodecahedron": {"faces": 12, "vertices": 20, "edges": 30, "element": "Aether/Universe"},
                            "icosahedron": {"faces": 20, "vertices": 12, "edges": 30, "element": "Water"},
                        },
                        "crop_circle_indices": [
                            "Milk Hill 2001 (Triple Julia Set - 409 Circles)",
                            "Stonehenge 1996 (Julia Set - 151 Circles)",
                            "Barbury Castle 1991 (Tetrahedron Ratchet Spiral)",
                            "Barbury Castle 2008 (Pi Glyph 10 Decimal Steps)",
                            "Chilbolton 2001 (Arecibo Reply Binary Agroglyph)",
                        ],
                    }
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "contents": [
                                {
                                    "uri": "geometry://catalog",
                                    "mimeType": "application/json",
                                    "text": json.dumps(catalog_info, indent=2),
                                }
                            ]
                        },
                    }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32602, "message": f"Resource URI '{uri}' not found"},
                    }

            elif method == "prompts/list":
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"prompts": list(self.prompts.values())},
                }

            elif method == "prompts/get":
                prompt_name = params.get("name")
                if prompt_name == "geometry_create_crop_circle":
                    glyph_type = params.get("arguments", {}).get("glyph_type", "julia_set")
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "description": "Design authentic UFO Crop Circle Agroglyphs with field parameters",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": {
                                        "type": "text",
                                        "text": (
                                            f"Generate an authentic {glyph_type} UFO crop circle agroglyph. "
                                            "Calculate precise logarithmic spiral arcs, concentric field perimeter lines, "
                                            "swirled crop lay nodes, and export as SVG with the 'gold' theme and DXF for CNC plotter rendering."
                                        ),
                                    },
                                }
                            ],
                        },
                    }
                elif prompt_name == "geometry_create_mandala":
                    folds = params.get("arguments", {}).get("symmetry_folds", "16")
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "description": "Design multi-layered Sacred Geometry Mandalas",
                            "messages": [
                                {
                                    "role": "user",
                                    "content": {
                                        "type": "text",
                                        "text": (
                                            f"Synthesize a {folds}-fold sacred geometry mandala combining Sri Yantra interlocking triangles, "
                                            "dual concentric lotus petal rings, and Metatron's Cube harmonic connecting lines. "
                                            "Include vibrant theme palettes, AST representation, and 3D OBJ relief extrusion."
                                        ),
                                    },
                                }
                            ],
                        },
                    }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Prompt '{prompt_name}' not found"},
                    }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method '{method}' not recognized"},
                }

        except Exception as exc:
            self._log(f"Error handling method '{method}': {exc}\n{traceback.format_exc()}")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error executing '{method}': {str(exc)}",
                },
            }

    # -------------------------------------------------------------------------
    # Stdio Transport Listener
    # -------------------------------------------------------------------------
    def run_stdio(self) -> None:
        """Starts the MCP server reading JSON-RPC 2.0 requests from stdio."""
        self._log(f"Starting MCP stdio server (v{self.version}) with {len(self.tools)} tools registered...")

        stdin = sys.stdin
        stdout = sys.stdout

        while True:
            try:
                line = stdin.readline()
                if not line:
                    break  # EOF

                line = line.strip()
                if not line:
                    continue

                # Handle Content-Length header framing if present
                if line.lower().startswith("content-length:"):
                    parts = line.split(":")
                    content_length = int(parts[1].strip())
                    # Consume following blank line
                    blank = stdin.readline()
                    raw_payload = stdin.read(content_length)
                else:
                    raw_payload = line

                try:
                    request = json.loads(raw_payload)
                except json.JSONDecodeError as jde:
                    err_resp = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": f"Parse error: {str(jde)}"},
                    }
                    stdout.write(json.dumps(err_resp) + "\n")
                    stdout.flush()
                    continue

                # Process single request or batch
                if isinstance(request, list):
                    responses = []
                    for req in request:
                        resp = self.handle_request(req)
                        if resp is not None:
                            responses.append(resp)
                    if responses:
                        stdout.write(json.dumps(responses) + "\n")
                        stdout.flush()
                else:
                    response = self.handle_request(request)
                    if response is not None:
                        stdout.write(json.dumps(response) + "\n")
                        stdout.flush()

            except KeyboardInterrupt:
                self._log("Shutting down MCP stdio server on SIGINT.")
                break
            except Exception as e:
                self._log(f"Unhandled loop error: {e}\n{traceback.format_exc()}")


def main() -> None:
    server = MCPServer()
    server.run_stdio()


if __name__ == "__main__":
    main()
