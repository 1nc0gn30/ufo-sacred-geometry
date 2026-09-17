"""UFO Sacred Geometry Studio UI & REST API Server.

Pure standard library HTTP & REST server (ThreadingHTTPServer) serving the
Web CAD Studio (design influenced by Material 3), live parametric vector endpoints, and CNC/DXF/OBJ
geometry export pipelines.
100% Python Standard Library.
"""

from __future__ import annotations

import cgi
import json
import math
import os
import platform
import sys
import time
import urllib.parse
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Attempt relative/package imports with robust fallbacks
try:
    from .compat import get_platform_info, normalize_path, read_text_safe
    from .models import Arc, Circle, GeometryAST, LineSegment, PatternPreset, Point2D, Point3D, Polygon, Spline
except ImportError:
    # Fallback if executed directly or in standalone mode
    from compat import get_platform_info, normalize_path, read_text_safe  # type: ignore
    from models import Arc, Circle, GeometryAST, LineSegment, PatternPreset, Point2D, Point3D, Polygon, Spline  # type: ignore

SERVER_START_TIME = time.time()
GENERATION_COUNT = 0


# ---------------------------------------------------------------------------
# Core Presets & Helper Generator Dispatcher
# ---------------------------------------------------------------------------

CATALOG_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "flower_of_life",
        "title": "Flower of Life",
        "category": "sacred",
        "description": "Sacred Genesis geometry containing 19 overlapping circles with hexagonal triangular lattice spacing.",
        "default_parameters": {
            "radius": 50.0,
            "rings": 3,
            "outer_rings": True,
            "completion_arcs": True,
            "stroke_width": 1.2,
            "color": "#ffd700",
        },
        "tags": ["sacred_geometry", "flower_of_life", "hexagonal", "ancient"],
        "difficulty": "medium",
    },
    {
        "id": "seed_of_life",
        "title": "Seed of Life",
        "category": "sacred",
        "description": "The fundamental 7-circle core of creation with 6 outer petals surrounding 1 central sphere.",
        "default_parameters": {
            "radius": 60.0,
            "outer_circle": True,
            "stroke_width": 1.5,
            "color": "#ffd700",
        },
        "tags": ["sacred_geometry", "seed_of_life", "genesis"],
        "difficulty": "beginner",
    },
    {
        "id": "metatrons_cube",
        "title": "Metatron's Cube",
        "category": "platonic",
        "description": "Fruit of Life foundation mapping all 5 Platonic Solids with 13 informational spheres and 78 harmonic lines.",
        "default_parameters": {
            "radius": 35.0,
            "include_outer_bounds": True,
            "stroke_width": 1.0,
            "node_color": "#ffd700",
            "line_color": "#00f0ff",
        },
        "tags": ["platonic_solids", "metatron", "sacred_geometry"],
        "difficulty": "advanced",
    },
    {
        "id": "sri_yantra",
        "title": "Sri Yantra Maha",
        "category": "sacred",
        "description": "Ancient sacred diagram of 9 interlocking triangles centered at the Bindu point generating 43 sub-triangles.",
        "default_parameters": {
            "scale": 180.0,
            "lotus_petals": 16,
            "include_bhupura": True,
            "stroke_width": 1.2,
            "color": "#ffd700",
        },
        "tags": ["sri_yantra", "tantra", "bindu", "sacred_geometry"],
        "difficulty": "master",
    },
    {
        "id": "fibonacci_spiral",
        "title": "Fibonacci Golden Spiral",
        "category": "fractal",
        "description": "Pure logarithmic golden spiral based on the golden ratio phi = (1 + sqrt(5))/2 ≈ 1.6180339887.",
        "default_parameters": {
            "scale": 8.0,
            "turns": 6,
            "growth_factor": 1.6180339887,
            "draw_golden_rectangles": True,
            "stroke_width": 1.5,
            "color": "#00ffff",
        },
        "tags": ["golden_ratio", "fibonacci", "phi", "logarithmic_spiral"],
        "difficulty": "medium",
    },
    {
        "id": "sunflower_phyllotaxis",
        "title": "Sunflower Phyllotaxis",
        "category": "fractal",
        "description": "Vogel model of botanical disc packing maximizing seed density with the golden angle 137.507764°.",
        "default_parameters": {
            "count": 300,
            "scaling": 12.0,
            "divergence_angle_deg": 137.507764,
            "dot_radius": 3.5,
            "color": "#fbbf24",
        },
        "tags": ["botany", "phyllotaxis", "golden_angle", "vogel"],
        "difficulty": "medium",
    },
    {
        "id": "milk_hill_crop_circle",
        "title": "Milk Hill 409 Agro-Glyph",
        "category": "crop",
        "description": "Colossal August 2001 Wiltshire crop formation consisting of 409 circles distributed across 6 spiral arms.",
        "default_parameters": {
            "radius": 220.0,
            "arms": 6,
            "circles_per_arm": 68,
            "spiral_tightness": 1.5,
            "stroke_width": 1.0,
            "color": "#f59e0b",
        },
        "tags": ["crop_circle", "milk_hill", "agro_glyph", "wiltshire"],
        "difficulty": "master",
    },
    {
        "id": "julia_set_crop_circle",
        "title": "Julia Set Agro-Glyph",
        "category": "crop",
        "description": "Stonehenge 1996 agro-glyph manifesting computer-generated Julia set fractal mathematics in wheat.",
        "default_parameters": {
            "radius": 200.0,
            "circles_count": 151,
            "stroke_width": 1.2,
            "color": "#38bdf8",
        },
        "tags": ["crop_circle", "julia_set", "fractal", "stonehenge"],
        "difficulty": "advanced",
    },
    {
        "id": "merkaba",
        "title": "Merkaba Star Tetrahedron",
        "category": "platonic",
        "description": "Counter-rotating light vehicle formed by two intersecting 3D regular tetrahedra in isometric projection.",
        "default_parameters": {
            "size": 180.0,
            "wireframe_axes": True,
            "stroke_width": 1.5,
            "color": "#a855f7",
        },
        "tags": ["merkaba", "star_tetrahedron", "platonic", "light_body"],
        "difficulty": "medium",
    },
    {
        "id": "vesica_piscis",
        "title": "Vesica Piscis",
        "category": "sacred",
        "description": "The sacred intersection of two circles of equal radius whose centers lie on each other's circumference.",
        "default_parameters": {
            "radius": 150.0,
            "draw_axes": True,
            "stroke_width": 1.5,
            "color": "#3b82f6",
        },
        "tags": ["vesica_piscis", "sacred_dyad", "root_3"],
        "difficulty": "beginner",
    },
    {
        "id": "tree_of_life",
        "title": "Tree of Life (Kabbalah)",
        "category": "sacred",
        "description": "10 divine emanations interconnected by 22 harmonic pathways mapping universal consciousness.",
        "default_parameters": {
            "scale": 120.0,
            "node_radius": 14.0,
            "overlay_flower": True,
            "stroke_width": 1.5,
            "path_color": "#00ffff",
            "node_color": "#ffd700",
        },
        "tags": ["tree_of_life", "kabbalah", "sephiroth"],
        "difficulty": "advanced",
    },
    {
        "id": "torus_vortex",
        "title": "Torus Vector Equilibrium",
        "category": "fractal",
        "description": "Dynamic toroidal energy vortex with nested harmonic streamlines and vector equilibrium.",
        "default_parameters": {
            "major_radius": 180.0,
            "minor_radius": 70.0,
            "strands": 24,
            "stroke_width": 1.0,
            "color": "#10b981",
        },
        "tags": ["torus", "vortex", "vector_equilibrium"],
        "difficulty": "advanced",
    },
]


def generate_pattern_ast(pattern_id: str, params: Optional[Dict[str, Any]] = None) -> GeometryAST:
    """Dynamically generate a GeometryAST for a given pattern ID and parameters."""
    global GENERATION_COUNT
    GENERATION_COUNT += 1

    p = params or {}
    pattern_id = pattern_id.lower().strip().replace("-", "_")

    # Try importing specialized generators if available
    try:
        if pattern_id in ("flower_of_life", "seed_of_life", "egg_of_life", "fruit_of_life", "tree_of_life"):
            from .generators import flower_of_life as fol_mod
            if pattern_id == "flower_of_life":
                return fol_mod.generate_flower_of_life(
                    radius=float(p.get("radius", 40.0)),
                    rings=int(p.get("rings", 3)),
                    outer_rings=bool(p.get("outer_rings", True)),
                    stroke_width=float(p.get("stroke_width", 1.2)),
                    color=str(p.get("color", "#ffd700")),
                )
            elif pattern_id == "seed_of_life":
                return fol_mod.generate_seed_of_life(
                    radius=float(p.get("radius", 60.0)),
                    stroke_width=float(p.get("stroke_width", 1.5)),
                    color=str(p.get("color", "#ffd700")),
                )
            elif pattern_id == "tree_of_life":
                return fol_mod.generate_tree_of_life(
                    scale=float(p.get("scale", 120.0)),
                    node_radius=float(p.get("node_radius", 14.0)),
                    stroke_width=float(p.get("stroke_width", 1.5)),
                )
    except Exception:
        pass

    try:
        if pattern_id == "metatrons_cube":
            from .generators import metatrons_cube as meta_mod
            if hasattr(meta_mod, "generate_metatrons_cube"):
                return meta_mod.generate_metatrons_cube(
                    radius=float(p.get("radius", 35.0)),
                    stroke_width=float(p.get("stroke_width", 1.0)),
                )
    except Exception:
        pass

    try:
        if pattern_id in ("fibonacci_spiral", "sunflower_phyllotaxis"):
            from .generators import fibonacci_spiral as fib_mod
            if pattern_id == "fibonacci_spiral" and hasattr(fib_mod, "generate_fibonacci_spiral"):
                return fib_mod.generate_fibonacci_spiral(
                    scale=float(p.get("scale", 8.0)),
                    turns=int(p.get("turns", 6)),
                    stroke_width=float(p.get("stroke_width", 1.5)),
                )
            elif pattern_id == "sunflower_phyllotaxis" and hasattr(fib_mod, "generate_sunflower_phyllotaxis"):
                return fib_mod.generate_sunflower_phyllotaxis(
                    count=int(p.get("count", 300)),
                    scaling=float(p.get("scaling", 12.0)),
                )
    except Exception:
        pass

    # Built-in robust geometric generator fallback (guaranteed zero-dependency generation)
    return _generate_fallback_geometry(pattern_id, p)


def _generate_fallback_geometry(pattern_id: str, p: Dict[str, Any]) -> GeometryAST:
    """Generate high-precision AST geometry directly using standard library math."""
    radius = float(p.get("radius", 180.0))
    stroke = float(p.get("stroke_width", 1.5))
    color = str(p.get("color", "#4285f4"))
    c0 = Point2D(0.0, 0.0)

    ast = GeometryAST(
        title=pattern_id.replace("_", " ").title(),
        description=f"Generated {pattern_id} geometry.",
        parameters=p,
        tags=[pattern_id, "sacred_geometry"],
    )

    if pattern_id in ("flower_of_life", "seed_of_life"):
        rings = 1 if pattern_id == "seed_of_life" else int(p.get("rings", 3))
        ast.add_circle(c0, radius, stroke_width=stroke, color=color)
        for r in range(1, rings + 1):
            count = 6 * r
            for i in range(count):
                ang = (i * 2.0 * math.pi) / count
                cp = Point2D.from_polar(r * radius, ang, c0)
                ast.add_circle(cp, radius, stroke_width=stroke, color=color)
        if p.get("outer_rings", True):
            ast.add_circle(c0, (rings + 1) * radius, stroke_width=stroke * 1.5, color=color)

    elif pattern_id == "metatrons_cube":
        nodes = [c0]
        dist = radius * 0.75
        for i in range(6):
            ang = i * (math.pi / 3.0)
            nodes.append(Point2D.from_polar(dist, ang, c0))
        for i in range(6):
            ang = i * (math.pi / 3.0) + (math.pi / 6.0)
            nodes.append(Point2D.from_polar(dist * math.sqrt(3), ang, c0))

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                ast.add_line(nodes[i], nodes[j], stroke_width=0.8, color="#38bdf8", opacity=0.7)
        for n in nodes:
            ast.add_circle(n, dist * 0.45, stroke_width=stroke, color=color)

    elif pattern_id == "sri_yantra":
        base_h = radius * 1.5
        tri_heights = [-0.9, -0.6, -0.3, 0.1, 0.4, 0.65, 0.85, -0.15, 0.35]
        tri_widths = [1.6, 1.3, 1.0, 1.4, 1.1, 0.8, 0.5, 0.7, 0.9]
        tri_dirs = [1, 1, 1, 1, -1, -1, -1, -1, -1]

        for i in range(len(tri_heights)):
            y_tip = tri_dirs[i] * (base_h * 0.5 * (1.0 - abs(tri_heights[i])))
            y_base = -tri_dirs[i] * (base_h * 0.45 * abs(tri_heights[i]))
            half_w = (radius * tri_widths[i]) * 0.5
            ast.add_polygon(
                [Point2D(0.0, y_tip), Point2D(-half_w, y_base), Point2D(half_w, y_base)],
                stroke_width=stroke,
                color=color,
            )
        ast.add_circle(c0, 3.0, stroke_width=1.5, color="#f59e0b", fill="#f59e0b")
        ast.add_circle(c0, radius * 1.15, stroke_width=stroke, color=color)
        ast.add_circle(c0, radius * 1.35, stroke_width=stroke * 1.2, color=color)

    elif pattern_id == "fibonacci_spiral":
        phi = 1.618033988749895
        turns = int(p.get("turns", 6))
        max_theta = turns * 2.0 * math.pi
        b = math.log(phi) / (math.pi / 2.0)
        a = 4.0
        pts: List[Point2D] = []
        theta = 0.0
        while theta <= max_theta:
            r = a * math.exp(b * theta * (radius / 200.0))
            pts.append(Point2D(r * math.cos(theta), r * math.sin(theta)))
            theta += 0.05
        ast.add_spline(pts, stroke_width=stroke, color=color)

    elif pattern_id == "sunflower_phyllotaxis":
        count = int(p.get("count", 250))
        golden_angle = 137.507764 * (math.pi / 180.0)
        c = (radius / math.sqrt(count)) * 1.2
        for n in range(1, count + 1):
            r = c * math.sqrt(n)
            theta = n * golden_angle
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            dot_r = max(1.5, min(5.0, (r / radius) * 4.0))
            ast.add_circle(Point2D(x, y), dot_r, stroke_width=1.0, color=color, fill=color)

    elif pattern_id == "milk_hill_crop_circle":
        arms = int(p.get("arms", 6))
        per_arm = int(p.get("circles_per_arm", 60))
        for a in range(arms):
            arm_ang = (a * 2.0 * math.pi) / arms
            for i in range(1, per_arm + 1):
                t = i / float(per_arm)
                spiral_ang = arm_ang + (t * math.pi * 1.5)
                dist = t * radius * 1.35
                dot_r = (math.sin(t * math.pi) * 10.0) + 1.5
                cp = Point2D.from_polar(dist, spiral_ang, c0)
                ast.add_circle(cp, dot_r, stroke_width=1.0, color=color)
        ast.add_circle(c0, radius * 1.45, stroke_width=0.8, color=color)

    elif pattern_id == "merkaba":
        sz = radius * 1.2
        # Upright & inverted triangles in 3D projection
        ast.add_polygon(
            [Point2D(0.0, -sz), Point2D(sz * 0.866, sz * 0.5), Point2D(-sz * 0.866, sz * 0.5)],
            stroke_width=stroke * 1.5,
            color=color,
        )
        ast.add_polygon(
            [Point2D(0.0, sz), Point2D(sz * 0.866, -sz * 0.5), Point2D(-sz * 0.866, -sz * 0.5)],
            stroke_width=stroke * 1.5,
            color=color,
        )
        ast.add_line(Point2D(0.0, -sz), Point2D(0.0, sz), stroke_width=1.0, color="#ffffff", opacity=0.6)
        ast.add_line(Point2D(-sz * 0.866, sz * 0.5), Point2D(sz * 0.866, -sz * 0.5), stroke_width=1.0, color="#ffffff", opacity=0.6)
        ast.add_line(Point2D(sz * 0.866, sz * 0.5), Point2D(-sz * 0.866, -sz * 0.5), stroke_width=1.0, color="#ffffff", opacity=0.6)
        ast.add_circle(c0, sz, stroke_width=0.8, color=color)

    elif pattern_id == "vesica_piscis":
        d = radius * 0.866
        ast.add_circle(Point2D(-d * 0.5, 0.0), radius, stroke_width=stroke, color=color)
        ast.add_circle(Point2D(d * 0.5, 0.0), radius, stroke_width=stroke, color=color)
        ast.add_line(Point2D(-d * 0.5, 0.0), Point2D(d * 0.5, 0.0), stroke_width=1.0, color="#38bdf8")
        ast.add_line(Point2D(0.0, -radius * 0.5), Point2D(0.0, radius * 0.5), stroke_width=1.0, color="#38bdf8")

    else:
        # Generic polygonal rosette
        symmetry = int(p.get("symmetry", 6))
        for i in range(symmetry):
            ang = (i * 2.0 * math.pi) / symmetry
            cp = Point2D.from_polar(radius * 0.6, ang, c0)
            ast.add_circle(cp, radius * 0.6, stroke_width=stroke, color=color)
        ast.add_circle(c0, radius, stroke_width=stroke, color=color)

    return ast


# ---------------------------------------------------------------------------
# High-Fidelity Exporters for REST endpoints
# ---------------------------------------------------------------------------

def export_ast_to_svg(ast: GeometryAST, padding: float = 20.0) -> str:
    """Generate clean, standalone SVG XML string from GeometryAST."""
    try:
        from .exporters import svg as svg_mod
        if hasattr(svg_mod, "export_svg"):
            return svg_mod.export_svg(ast, padding=padding)
    except Exception:
        pass

    bb = ast.bounds()
    min_x = math.floor(bb.min_x - padding)
    min_y = math.floor(bb.min_y - padding)
    width = math.ceil(bb.width + 2.0 * padding)
    height = math.ceil(bb.height + 2.0 * padding)

    if width <= 0 or height <= 0:
        min_x, min_y, width, height = -300, -300, 600, 600

    out: List[str] = [
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x} {min_y} {width} {height}" width="{width}mm" height="{height}mm">',
        f'  <title>{ast.title}</title>',
        f'  <desc>{ast.description}</desc>',
        '  <g id="geometry_layer">',
    ]

    for line in ast.lines:
        out.append(
            f'    <line x1="{line.start.x:.3f}" y1="{line.start.y:.3f}" x2="{line.end.x:.3f}" y2="{line.end.y:.3f}" stroke="{line.color}" stroke-width="{line.stroke_width:.2f}" opacity="{line.opacity:.2f}"/>'
        )

    for circle in ast.circles:
        fill = circle.fill or "none"
        out.append(
            f'    <circle cx="{circle.center.x:.3f}" cy="{circle.center.y:.3f}" r="{circle.radius:.3f}" stroke="{circle.color}" stroke-width="{circle.stroke_width:.2f}" fill="{fill}" opacity="{circle.opacity:.2f}"/>'
        )

    for arc in ast.arcs:
        sp = arc.start_point
        ep = arc.end_point
        large_arc = 1 if arc.span_angle > math.pi else 0
        out.append(
            f'    <path d="M {sp.x:.3f} {sp.y:.3f} A {arc.radius:.3f} {arc.radius:.3f} 0 {large_arc} 1 {ep.x:.3f} {ep.y:.3f}" stroke="{arc.color}" stroke-width="{arc.stroke_width:.2f}" fill="none" opacity="{arc.opacity:.2f}"/>'
        )

    for poly in ast.polygons:
        pts = " ".join(f"{p.x:.3f},{p.y:.3f}" for p in poly.points)
        fill = poly.fill or "none"
        tag = "polygon" if poly.closed else "polyline"
        out.append(
            f'    <{tag} points="{pts}" stroke="{poly.color}" stroke-width="{poly.stroke_width:.2f}" fill="{fill}" opacity="{poly.opacity:.2f}"/>'
        )

    for spline in ast.splines:
        sampled = spline.sample_points(12)
        if sampled:
            pts = " ".join(f"{p.x:.3f},{p.y:.3f}" for p in sampled)
            out.append(
                f'    <polyline points="{pts}" stroke="{spline.color}" stroke-width="{spline.stroke_width:.2f}" fill="none" opacity="{spline.opacity:.2f}"/>'
            )

    out.append("  </g>")
    out.append("</svg>")
    return "\n".join(out)


def export_ast_to_dxf(ast: GeometryAST) -> str:
    """Generate AutoCAD R12 / CNC Laser-Cut compliant DXF string."""
    try:
        from .exporters import dxf as dxf_mod
        if hasattr(dxf_mod, "export_dxf"):
            return dxf_mod.export_dxf(ast)
    except Exception:
        pass

    out: List[str] = [
        "0", "SECTION", "2", "HEADER", "9", "$ACADVER", "1", "AC1009", "0", "ENDSEC",
        "0", "SECTION", "2", "TABLES", "0", "TABLE", "2", "LAYER", "70", "1",
        "0", "LAYER", "2", "0", "70", "0", "62", "7", "6", "CONTINUOUS",
        "0", "ENDTAB", "0", "ENDSEC",
        "0", "SECTION", "2", "ENTITIES",
    ]

    for line in ast.lines:
        out.extend([
            "0", "LINE", "8", line.layer or "0",
            "10", f"{line.start.x:.4f}", "20", f"{line.start.y:.4f}", "30", "0.0",
            "11", f"{line.end.x:.4f}", "21", f"{line.end.y:.4f}", "31", "0.0",
        ])

    for circle in ast.circles:
        out.extend([
            "0", "CIRCLE", "8", circle.layer or "0",
            "10", f"{circle.center.x:.4f}", "20", f"{circle.center.y:.4f}", "30", "0.0",
            "40", f"{circle.radius:.4f}",
        ])

    for poly in ast.polygons:
        out.extend([
            "0", "POLYLINE", "8", poly.layer or "0", "66", "1", "70", "1" if poly.closed else "0",
        ])
        for p in poly.points:
            out.extend([
                "0", "VERTEX", "8", poly.layer or "0",
                "10", f"{p.x:.4f}", "20", f"{p.y:.4f}", "30", "0.0",
            ])
        out.extend(["0", "SEQEND"])

    for spline in ast.splines:
        sampled = spline.sample_points(12)
        out.extend([
            "0", "POLYLINE", "8", spline.layer or "0", "66", "1", "70", "1" if spline.closed else "0",
        ])
        for p in sampled:
            out.extend([
                "0", "VERTEX", "8", spline.layer or "0",
                "10", f"{p.x:.4f}", "20", f"{p.y:.4f}", "30", "0.0",
            ])
        out.extend(["0", "SEQEND"])

    out.extend(["0", "ENDSEC", "0", "EOF", ""])
    return "\n".join(out)


def export_ast_to_obj(ast: GeometryAST) -> str:
    """Generate Wavefront OBJ 3D mesh string."""
    try:
        from .exporters import obj as obj_mod
        if hasattr(obj_mod, "export_obj"):
            return obj_mod.export_obj(ast)
    except Exception:
        pass

    out: List[str] = [
        f"# UFO Sacred Geometry Studio OBJ Export - {ast.title}",
        "# Units: Millimeters (mm)",
        "o SacredGeometry",
    ]
    v_idx = 1

    for circle in ast.circles:
        segs = 32
        for i in range(segs):
            ang = (i * 2.0 * math.pi) / segs
            x = circle.center.x + circle.radius * math.cos(ang)
            y = circle.center.y + circle.radius * math.sin(ang)
            out.append(f"v {x:.4f} {y:.4f} 0.0000")
        line_indices = " ".join(str(v_idx + i) for i in range(segs))
        out.append(f"l {line_indices} {v_idx}")
        v_idx += segs

    for line in ast.lines:
        out.append(f"v {line.start.x:.4f} {line.start.y:.4f} 0.0000")
        out.append(f"v {line.end.x:.4f} {line.end.y:.4f} 0.0000")
        out.append(f"l {v_idx} {v_idx + 1}")
        v_idx += 2

    for poly in ast.polygons:
        for p in poly.points:
            out.append(f"v {p.x:.4f} {p.y:.4f} 0.0000")
        face_indices = " ".join(str(v_idx + i) for i in range(len(poly.points)))
        tag = "f" if poly.closed and len(poly.points) >= 3 else "l"
        out.append(f"{tag} {face_indices}")
        v_idx += len(poly.points)

    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# HTTP Request Handler & Server
# ---------------------------------------------------------------------------

class SacredGeometryRequestHandler(BaseHTTPRequestHandler):
    """Threading HTTP Handler serving static UI assets and REST API endpoints."""

    server_version = "SacredGeometryStudio/1.0.0"

    def do_OPTIONS(self) -> None:
        """Handle CORS pre-flight requests."""
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        """Route GET requests to static assets or REST endpoints."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Static Web UI routes
        if path in ("/", "/index.html"):
            self._serve_studio_ui()
            return

        # REST API Routes
        if path in ("/api/presets", "/presets"):
            self._handle_get_presets()
        elif path == "/api/generate":
            params = {k: v[0] for k, v in query.items()}
            pattern = params.pop("pattern", "flower_of_life")
            self._handle_generate(pattern, params)
        elif path == "/api/export-svg":
            params = {k: v[0] for k, v in query.items()}
            pattern = params.pop("pattern", "flower_of_life")
            self._handle_export(pattern, params, "svg")
        elif path == "/api/export-dxf":
            params = {k: v[0] for k, v in query.items()}
            pattern = params.pop("pattern", "flower_of_life")
            self._handle_export(pattern, params, "dxf")
        elif path == "/api/export-obj":
            params = {k: v[0] for k, v in query.items()}
            pattern = params.pop("pattern", "flower_of_life")
            self._handle_export(pattern, params, "obj")
        elif path in ("/api/stats", "/stats"):
            self._handle_get_stats()
        elif path in ("/api/diagnostics", "/diagnostics"):
            self._handle_get_diagnostics()
        elif path in ("/api/health", "/health"):
            self._send_json({"status": "healthy", "uptime_seconds": round(time.time() - SERVER_START_TIME, 2)})
        else:
            # Check if requested file exists in public/ directory
            public_file = self._find_public_file(path.lstrip("/"))
            if public_file and public_file.is_file():
                self._serve_file(public_file)
            else:
                self._send_json({"error": "Endpoint not found", "path": path}, status=HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        """Route POST requests for parametric generation and exports."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Read JSON body
        body = self._read_json_body()
        pattern = body.get("pattern", "flower_of_life")
        params = body.get("parameters", body)

        if path == "/api/generate":
            self._handle_generate(pattern, params)
        elif path == "/api/export-svg":
            self._handle_export(pattern, params, "svg")
        elif path == "/api/export-dxf":
            self._handle_export(pattern, params, "dxf")
        elif path == "/api/export-obj":
            self._handle_export(pattern, params, "obj")
        else:
            self._send_json({"error": "Invalid POST endpoint", "path": path}, status=HTTPStatus.NOT_FOUND)

    def _handle_get_presets(self) -> None:
        """Return preset catalog."""
        self._send_json({"status": "success", "count": len(CATALOG_PRESETS), "presets": CATALOG_PRESETS})

    def _handle_generate(self, pattern: str, params: Dict[str, Any]) -> None:
        """Generate geometry and return AST + SVG preview + stats."""
        try:
            t0 = time.perf_counter()
            ast = generate_pattern_ast(pattern, params)
            svg_content = export_ast_to_svg(ast)
            elapsed_ms = (time.perf_counter() - t0) * 1000.0

            response_data = {
                "status": "success",
                "pattern": pattern,
                "execution_time_ms": round(elapsed_ms, 3),
                "ast": ast.to_dict(),
                "svg_preview": svg_content,
                "stats": ast.stats(),
            }
            self._send_json(response_data)
        except Exception as e:
            self._send_json({"status": "error", "message": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _handle_export(self, pattern: str, params: Dict[str, Any], fmt: str) -> None:
        """Export geometry in specific format with direct download headers."""
        try:
            ast = generate_pattern_ast(pattern, params)
            filename = f"{pattern}_sacred_geometry.{fmt}"

            if fmt == "svg":
                data = export_ast_to_svg(ast)
                mime = "image/svg+xml; charset=utf-8"
            elif fmt == "dxf":
                data = export_ast_to_dxf(ast)
                mime = "application/dxf"
            elif fmt == "obj":
                data = export_ast_to_obj(ast)
                mime = "text/plain; charset=utf-8"
            else:
                self._send_json({"error": f"Unsupported format: {fmt}"}, status=HTTPStatus.BAD_REQUEST)
                return

            payload = data.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self._send_cors_headers()
            self.send_header("Content-Type", mime)
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as e:
            self._send_json({"status": "error", "message": str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _handle_get_stats(self) -> None:
        """Return engine operational metrics."""
        self._send_json({
            "service": "UFO Sacred Geometry Studio",
            "version": "1.0.0",
            "uptime_seconds": round(time.time() - SERVER_START_TIME, 2),
            "generated_geometries_count": GENERATION_COUNT,
            "registered_presets_count": len(CATALOG_PRESETS),
            "supported_exporters": ["svg", "dxf", "obj", "json", "png"],
        })

    def _handle_get_diagnostics(self) -> None:
        """Return system and mathematical diagnostics."""
        diag = get_platform_info()
        diag["uptime_seconds"] = round(time.time() - SERVER_START_TIME, 2)
        diag["phi_constant"] = 1.618033988749895
        diag["root_3_constant"] = math.sqrt(3)
        diag["golden_angle_deg"] = 137.507764
        diag["endpoints"] = [
            "GET /",
            "GET /api/presets",
            "POST /api/generate",
            "POST /api/export-svg",
            "POST /api/export-dxf",
            "POST /api/export-obj",
            "GET /api/stats",
            "GET /api/diagnostics",
            "GET /api/health",
        ]
        self._send_json(diag)

    def _serve_studio_ui(self) -> None:
        """Serve UFO Sacred Geometry Studio web application."""
        html_file = self._find_public_file("index.html")
        if html_file and html_file.is_file():
            self._serve_file(html_file, content_type="text/html; charset=utf-8")
            return

        # Fallback embedded HTML if file is missing
        embedded_html = "<!-- UFO Sacred Geometry Studio Fallback UI -->"
        payload = embedded_html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _find_public_file(self, rel_path: str) -> Optional[Path]:
        """Search for a file in public/ relative to package, cwd, or repo root."""
        search_dirs = [
            Path(__file__).resolve().parent.parent.parent / "public",
            Path.cwd() / "public",
            Path(__file__).resolve().parent / "public",
        ]
        for d in search_dirs:
            target = (d / rel_path).resolve()
            if target.exists() and target.is_file():
                return target
        return None

    def _serve_file(self, file_path: Path, content_type: Optional[str] = None) -> None:
        """Serve static file from disk."""
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            if not content_type:
                ext = file_path.suffix.lower()
                mime_map = {
                    ".html": "text/html; charset=utf-8",
                    ".css": "text/css; charset=utf-8",
                    ".js": "application/javascript; charset=utf-8",
                    ".json": "application/json; charset=utf-8",
                    ".svg": "image/svg+xml; charset=utf-8",
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".ico": "image/x-icon",
                }
                content_type = mime_map.get(ext, "application/octet-stream")

            self.send_response(HTTPStatus.OK)
            self._send_cors_headers()
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self._send_json({"error": f"Failed to serve file: {e}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def _send_json(self, data: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        """Serialize and send JSON response."""
        payload = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_cors_headers(self) -> None:
        """Send open CORS headers."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def _read_json_body(self) -> Dict[str, Any]:
        """Read and parse JSON body from incoming POST request."""
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length <= 0:
                return {}
            raw_body = self.rfile.read(length).decode("utf-8")
            return json.loads(raw_body)
        except Exception:
            return {}

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress noisy request logs in production while keeping errors."""
        if hasattr(self.server, "quiet") and self.server.quiet:
            return
        super().log_message(format, *args)


# ---------------------------------------------------------------------------
# Server Startup & CLI Interface
# ---------------------------------------------------------------------------

def start_ui_server(
    host: str = "127.0.0.1",
    port: int = 8080,
    open_browser: bool = False,
    quiet: bool = False,
) -> ThreadingHTTPServer:
    """Instantiate and start the Sacred Geometry Studio HTTP Server."""
    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, SacredGeometryRequestHandler)
    setattr(httpd, "quiet", quiet)

    url = f"http://{host}:{port}"
    if not quiet:
        print(f"\n✨ UFO Sacred Geometry Studio running at: {url}")
        print(f"✨ REST API Endpoints active on /api/presets, /api/generate, /api/export-svg")
        print("Press Ctrl+C to stop.\n")

    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    return httpd


def run_server_cli() -> None:
    """CLI Entry point to launch UI server."""
    import argparse

    parser = argparse.ArgumentParser(description="UFO Sacred Geometry Studio UI Server")
    parser.add_argument("--host", default="127.0.0.1", help="Binding host interface (default: 127.0.0.1)")
    parser.add_argument("--port", "-p", type=int, default=8080, help="HTTP port (default: 8080)")
    parser.add_argument("--open", "-o", action="store_true", help="Open studio UI in default browser")
    parser.add_argument("--quiet", "-q", action="store_true", help="Quiet mode (minimal logging)")

    args = parser.parse_args()

    httpd = start_ui_server(host=args.host, port=args.port, open_browser=args.open, quiet=args.quiet)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Sacred Geometry Studio...")
        httpd.server_close()


if __name__ == "__main__":
    run_server_cli()
