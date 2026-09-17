"""
UFO Sacred Geometry & Crop Circle Pattern Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pure Python 3 standard library engine for generating sacred geometry,
UFO crop circle agroglyphs, Golden Ratio harmonics, and multi-format CAD/vector exports (SVG, DXF, OBJ).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from .compat import (
    atomic_write_bytes,
    atomic_write_text,
    get_platform_info,
    is_linux,
    is_macos,
    is_termux,
    is_windows,
    normalize_path,
    read_json_safe,
    read_text_safe,
    safe_delete,
    write_json_safe,
)
from .catalog import (
    PRESETS,
    get_catalog_summary,
    get_preset,
    list_categories,
    list_presets,
    list_tags,
)
from .exporters import (
    DXFExporter,
    OBJExporter,
    SVG_THEMES,
    SVGExporter,
    export_dxf as raw_export_dxf,
    export_obj as raw_export_obj,
    export_svg as raw_export_svg,
)
from .generators import (
    generate_barbury_castle_glyph,
    generate_chilbolton_binary_glyph,
    generate_crop_circle,
    generate_egg_of_life,
    generate_fibonacci_sequence,
    generate_flower_of_life,
    generate_fruit_of_life,
    generate_golden_rectangles,
    generate_golden_spiral,
    generate_golden_triangle_spiral,
    generate_julia_set_glyph,
    generate_merkaba,
    generate_metatrons_cube,
    generate_milk_hill_glyph,
    generate_phyllotaxis,
    generate_platonic_solid_projection,
    generate_seed_of_life,
    generate_sri_yantra,
    generate_torus,
    generate_golden_ratio_torus,
    generate_torus_knot,
    generate_tree_of_life,
    generate_triskele_glyph,
    generate_vesica_piscis,
    get_metatrons_13_centers,
    generate_star_polyhedron_projection,
    generate_cymatic_resonance_pattern,
    get_sacred_frequency,
    list_sacred_frequencies,
    SacredFrequency,
    SACRED_FREQUENCY_MATRIX,
)
from .models import (
    Arc,
    BoundingBox,
    Circle,
    GeometryAST,
    LineSegment,
    PatternPreset,
    Point2D,
    Point3D,
    Polygon,
    Spline,
)

__version__ = "0.1.0"
__author__ = "UFO Sacred Geometry Architecture Team"
__license__ = "MIT"

PHI = (1.0 + math.sqrt(5.0)) / 2.0  # 1.618033988749895 - The Golden Ratio
GOLDEN_ANGLE_DEG = 360.0 * (1.0 - 1.0 / PHI)  # 137.50776405003785 degrees
GOLDEN_ANGLE_RAD = math.radians(GOLDEN_ANGLE_DEG)

# Compatibility alias for Point & Line & PRESETS_CATALOG
Point = Point2D
Line = LineSegment
PRESETS_CATALOG = PRESETS

# Standard Theme Definitions
THEMES: Dict[str, Dict[str, Any]] = {
    "gold": {
        "name": "Sacred Gold",
        "bg": "#0d0e15",
        "primary": "#d4af37",
        "secondary": "#f5d77f",
        "accent": "#ffd700",
        "tertiary": "#8a7322",
        "fill": "rgba(212, 175, 55, 0.08)",
        "glow": "#f5d77f",
        "grid": "#1f2230",
        "text": "#f5d77f",
    },
    "blueprint": {
        "name": "Architectural Blueprint",
        "bg": "#0a192f",
        "primary": "#00e5ff",
        "secondary": "#4fc3f7",
        "accent": "#80d8ff",
        "tertiary": "#007799",
        "fill": "rgba(0, 229, 255, 0.06)",
        "glow": "#00e5ff",
        "grid": "#172a45",
        "text": "#80d8ff",
    },
    "neon_matrix": {
        "name": "Matrix Phosphor",
        "bg": "#050805",
        "primary": "#00ff66",
        "secondary": "#39ff14",
        "accent": "#adff2f",
        "tertiary": "#006622",
        "fill": "rgba(0, 255, 102, 0.07)",
        "glow": "#00ff66",
        "grid": "#0d1a0d",
        "text": "#39ff14",
    },
    "obsidian_dark": {
        "name": "Obsidian Starlight",
        "bg": "#0f172a",
        "primary": "#38bdf8",
        "secondary": "#94a3b8",
        "accent": "#e2e8f0",
        "tertiary": "#475569",
        "fill": "rgba(56, 189, 248, 0.05)",
        "glow": "#38bdf8",
        "grid": "#1e293b",
        "text": "#e2e8f0",
    },
    "light_minimal": {
        "name": "Minimalist Slate",
        "bg": "#f8fafc",
        "primary": "#1e293b",
        "secondary": "#475569",
        "accent": "#0284c7",
        "tertiary": "#cbd5e1",
        "fill": "rgba(30, 41, 59, 0.04)",
        "glow": "#0284c7",
        "grid": "#e2e8f0",
        "text": "#0f172a",
    },
}

# Theme mapping between internal names and SVG exporter theme names
THEME_MAP = {
    "gold": "dark_gold",
    "dark_gold": "dark_gold",
    "blueprint": "blueprint",
    "neon_matrix": "neon_ufo",
    "neon_ufo": "neon_ufo",
    "obsidian_dark": "cosmic_purple",
    "cosmic_purple": "cosmic_purple",
    "light_minimal": "light_minimal",
}


# -----------------------------------------------------------------------------
# Master Generator Dispatcher
# -----------------------------------------------------------------------------
def generate_pattern(pattern_type: str, **kwargs: Any) -> GeometryAST:
    """Master generator dispatcher for all sacred geometry and crop glyph patterns."""
    clean_type = pattern_type.lower().strip().replace("-", "_")

    # If preset requested
    if clean_type in PRESETS:
        preset = PRESETS[clean_type]
        merged_args = dict(preset.default_parameters)
        merged_args.update(kwargs)
        return _dispatch_pattern_generation(preset.id, merged_args)

    return _dispatch_pattern_generation(clean_type, kwargs)


def _dispatch_pattern_generation(pattern_id: str, p: Dict[str, Any]) -> GeometryAST:
    """Internal router invoking specific generator functions with safe argument mapping."""
    # Flower of life family
    if pattern_id in ("flower_of_life", "flower_of_life_classic", "flower_of_life_extended"):
        radius = float(p.get("radius", 50.0))
        rings = int(p.get("iterations", p.get("rings", 3)))
        outer_rings = bool(p.get("outer_rings", True))
        stroke_width = float(p.get("stroke_width", 1.2))
        color = str(p.get("color", "#ffd700"))
        return generate_flower_of_life(radius=radius, rings=rings, outer_rings=outer_rings, stroke_width=stroke_width, color=color)

    elif pattern_id == "seed_of_life":
        radius = float(p.get("radius", 60.0))
        stroke_width = float(p.get("stroke_width", 1.5))
        color = str(p.get("color", "#ffd700"))
        return generate_seed_of_life(radius=radius, stroke_width=stroke_width, color=color)

    elif pattern_id == "egg_of_life":
        radius = float(p.get("radius", 50.0))
        stroke_width = float(p.get("stroke_width", 1.4))
        return generate_egg_of_life(radius=radius, stroke_width=stroke_width)

    elif pattern_id == "fruit_of_life":
        radius = float(p.get("radius", 35.0))
        stroke_width = float(p.get("stroke_width", 1.2))
        return generate_fruit_of_life(radius=radius, stroke_width=stroke_width)

    elif pattern_id == "tree_of_life":
        scale = float(p.get("scale", 120.0))
        node_radius = float(p.get("node_radius", 14.0))
        stroke_width = float(p.get("stroke_width", 1.5))
        return generate_tree_of_life(scale=scale, node_radius=node_radius, stroke_width=stroke_width)

    # Metatron's Cube
    elif pattern_id == "metatrons_cube":
        radius = float(p.get("radius", 35.0))
        stroke_width = float(p.get("stroke_width", 1.0))
        circle_color = str(p.get("circle_color", "#ffd700"))
        line_color = str(p.get("line_color", "#00f0ff"))
        return generate_metatrons_cube(radius=radius, stroke_width=stroke_width, circle_color=circle_color, line_color=line_color)

    elif pattern_id in ("platonic_tetrahedron", "tetrahedron"):
        return generate_platonic_solid_projection(solid_type="tetrahedron", **p)
    elif pattern_id in ("platonic_cube", "cube", "hexahedron"):
        return generate_platonic_solid_projection(solid_type="cube", **p)
    elif pattern_id in ("platonic_octahedron", "octahedron"):
        return generate_platonic_solid_projection(solid_type="octahedron", **p)
    elif pattern_id in ("platonic_icosahedron", "icosahedron"):
        return generate_platonic_solid_projection(solid_type="icosahedron", **p)
    elif pattern_id in ("platonic_dodecahedron", "dodecahedron"):
        return generate_platonic_solid_projection(solid_type="dodecahedron", **p)

    # Fibonacci / Golden Ratio
    elif pattern_id in ("fibonacci_spiral", "golden_spiral", "fibonacci_golden_spiral"):
        scale = float(p.get("scale", 8.0))
        iterations = float(p.get("iterations", p.get("turns", 6.0)))
        growth_factor = float(p.get("growth_factor", 0.3063489))
        stroke_width = float(p.get("stroke_width", 1.5))
        color = str(p.get("color", "#00ffff"))
        return generate_golden_spiral(iterations=iterations, growth_factor=growth_factor, scale=scale, stroke_width=stroke_width, color=color)

    elif pattern_id in ("golden_rectangles", "whirling_squares"):
        iterations = int(p.get("iterations", 8))
        initial_size = float(p.get("initial_size", 12.0))
        stroke_width = float(p.get("stroke_width", 1.2))
        return generate_golden_rectangles(iterations=iterations, initial_size=initial_size, stroke_width=stroke_width)

    elif pattern_id in ("phyllotaxis", "sunflower_phyllotaxis", "fibonacci_phyllotaxis", "fibonacci_phyllotaxis_500"):
        num_points = int(p.get("num_points", p.get("count", p.get("seed_count", 350))))
        spread = float(p.get("spread", p.get("scaling", p.get("c_factor", 4.5))))
        point_radius = float(p.get("point_radius", p.get("marker_radius", p.get("dot_radius", 2.8))))
        stroke_width = float(p.get("stroke_width", 1.0))
        seed_color = str(p.get("seed_color", p.get("color", "#ffd700")))
        return generate_phyllotaxis(num_points=num_points, spread=spread, point_radius=point_radius, stroke_width=stroke_width, seed_color=seed_color)

    elif pattern_id in ("golden_triangle_spiral", "golden_triangle", "sublime_triangle"):
        iterations = int(p.get("iterations", 9))
        initial_size = float(p.get("initial_size", 240.0))
        stroke_width = float(p.get("stroke_width", 1.2))
        return generate_golden_triangle_spiral(iterations=iterations, initial_size=initial_size, stroke_width=stroke_width)

    # Sri Yantra
    elif pattern_id in ("sri_yantra", "sri_yantra_mahameru"):
        size = float(p.get("radius", p.get("size", 180.0)))
        show_petals = bool(p.get("show_petals", True))
        show_bhupura = bool(p.get("show_bhupura", True))
        show_bindu = bool(p.get("show_bindu", True))
        stroke_width = float(p.get("stroke_width", 1.0))
        return generate_sri_yantra(size=size, show_petals=show_petals, show_bhupura=show_bhupura, show_bindu=show_bindu, stroke_width=stroke_width)

    # Crop Circles
    elif pattern_id in ("crop_circle", "crop_circle_milk_hill", "milk_hill"):
        style = str(p.get("style", p.get("glyph_type", "milk_hill")))
        scale = float(p.get("radius", p.get("scale", 220.0)))
        stroke_width = float(p.get("stroke_width", 0.8))
        if pattern_id == "crop_circle_milk_hill" or style in ("milk_hill", "409_circles"):
            return generate_milk_hill_glyph(scale=scale, stroke_width=stroke_width)
        return generate_crop_circle(style=style, scale=scale, stroke_width=stroke_width)

    elif pattern_id in ("crop_circle_julia_set", "julia_set"):
        scale = float(p.get("radius", p.get("scale", 200.0)))
        num_circles = int(p.get("num_circles", 151))
        return generate_julia_set_glyph(scale=scale, num_circles=num_circles)

    elif pattern_id in ("crop_circle_barbury_castle", "barbury_castle"):
        scale = float(p.get("radius", p.get("scale", 180.0)))
        return generate_barbury_castle_glyph(scale=scale)

    elif pattern_id in ("crop_circle_pi", "pi_glyph"):
        scale = float(p.get("radius", p.get("scale", 180.0)))
        return generate_crop_circle(style="barbury_castle", scale=scale)

    elif pattern_id in ("crop_circle_chilbolton", "chilbolton"):
        scale = float(p.get("radius", p.get("scale", 200.0)))
        return generate_chilbolton_binary_glyph(scale=scale)

    elif pattern_id in ("crop_circle_triskele", "triskele"):
        scale = float(p.get("radius", p.get("scale", 180.0)))
        return generate_triskele_glyph(scale=scale)

    # Merkaba & Torus
    elif pattern_id in ("merkaba", "merkaba_star", "merkaba_star_tetrahedron"):
        radius = float(p.get("radius", 120.0))
        stroke_width = float(p.get("stroke_width", 1.4))
        return generate_merkaba(radius=radius, stroke_width=stroke_width)

    elif pattern_id in ("torus", "torus_vortex", "torus_vortex_field"):
        major_radius = float(p.get("major_radius", p.get("radius", 120.0)))
        minor_radius = float(p.get("minor_radius", 45.0))
        u_steps = int(p.get("u_steps", p.get("rings", p.get("flow_strands", 32))))
        v_steps = int(p.get("v_steps", 16))
        stroke_width = float(p.get("stroke_width", 0.8))
        return generate_torus(major_radius=major_radius, minor_radius=minor_radius, u_steps=u_steps, v_steps=v_steps, stroke_width=stroke_width)

    elif pattern_id in ("golden_torus", "golden_ratio_torus", "phi_torus"):
        radius = float(p.get("radius", 120.0))
        phi_strands = int(p.get("phi_strands", p.get("strands", 24)))
        v_samples = int(p.get("v_samples", 40))
        stroke_width = float(p.get("stroke_width", 1.0))
        return generate_golden_ratio_torus(radius=radius, phi_strands=phi_strands, v_samples=v_samples, stroke_width=stroke_width)

    elif pattern_id in ("torus_knot", "torus_knot_trefoil"):
        p_val = int(p.get("p", 3))
        q_val = int(p.get("q", 8))
        major_radius = float(p.get("major_radius", 140.0))
        minor_radius = float(p.get("minor_radius", 60.0))
        return generate_torus_knot(p=p_val, q=q_val, major_radius=major_radius, minor_radius=minor_radius)

    elif pattern_id == "vesica_piscis":
        radius = float(p.get("radius", 140.0))
        stroke_width = float(p.get("stroke_width", 1.4))
        return generate_vesica_piscis(radius=radius, stroke_width=stroke_width)

    # Fallback
    try:
        return generate_crop_circle(style=pattern_id, scale=float(p.get("radius", 180.0)))
    except Exception:
        return generate_flower_of_life(radius=float(p.get("radius", 50.0)), rings=int(p.get("iterations", 3)))


# -----------------------------------------------------------------------------
# Exporters Wrapper Functions
# -----------------------------------------------------------------------------
def export_svg(
    ast_or_pattern: Union[GeometryAST, str],
    file_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    theme: str = "dark_gold",
    stroke_width: Optional[float] = None,
    glow: bool = True,
    padding: float = 20.0,
    **kwargs: Any,
) -> str:
    """Exports geometry pattern as publication-grade vector SVG XML markup."""
    if isinstance(ast_or_pattern, str):
        ast = generate_pattern(ast_or_pattern, **kwargs)
    else:
        ast = ast_or_pattern

    target_path = file_path or output_path or kwargs.get("file_path") or kwargs.get("output_path")
    theme_name = THEME_MAP.get(theme, theme)
    return raw_export_svg(
        ast,
        file_path=target_path,
        theme=theme_name,
        show_glow=glow,
        padding=padding,
        stroke_width=stroke_width,
        **kwargs,
    )


def export_dxf(
    ast_or_pattern: Union[GeometryAST, str],
    file_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    **kwargs: Any,
) -> str:
    """Exports geometry as standard AutoCAD DXF for CNC/laser cutting."""
    if isinstance(ast_or_pattern, str):
        ast = generate_pattern(ast_or_pattern, **kwargs)
    else:
        ast = ast_or_pattern

    target_path = file_path or output_path or kwargs.get("file_path") or kwargs.get("output_path")
    return raw_export_dxf(ast, file_path=target_path, **kwargs)


def export_obj(
    ast_or_pattern: Union[GeometryAST, str],
    file_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    base_type: str = "cylinder",
    base_thickness: float = 4.0,
    extrusion: float = 1.8,
    relief_height: float = 1.8,
    relief_depth: Optional[float] = None,
    medallion_base: Optional[bool] = None,
    stroke_width_3d: float = 0.8,
    **kwargs: Any,
) -> str:
    """Exports geometry as 3D embossed mesh (Wavefront OBJ)."""
    if isinstance(ast_or_pattern, str):
        ast = generate_pattern(ast_or_pattern, **kwargs)
    else:
        ast = ast_or_pattern

    target_path = file_path or output_path or kwargs.get("file_path") or kwargs.get("output_path")
    effective_relief = relief_depth if relief_depth is not None else (extrusion if extrusion != 1.8 else relief_height)
    return raw_export_obj(
        ast,
        file_path=target_path,
        base_type=base_type,
        base_thickness=base_thickness,
        relief_height=effective_relief,
        medallion_base=medallion_base,
        stroke_width_3d=stroke_width_3d,
        **kwargs,
    )


__all__ = [
    # Metadata
    "__version__",
    "__author__",
    "__license__",
    "PHI",
    "GOLDEN_ANGLE_DEG",
    "GOLDEN_ANGLE_RAD",
    "THEMES",
    "THEME_MAP",
    # Geometry Primitives & AST
    "Point",
    "Point2D",
    "Point3D",
    "Line",
    "LineSegment",
    "Circle",
    "Arc",
    "Polygon",
    "Spline",
    "BoundingBox",
    "GeometryAST",
    "PatternPreset",
    # Presets Catalog
    "PRESETS",
    "PRESETS_CATALOG",
    "get_preset",
    "list_presets",
    "list_categories",
    "list_tags",
    "get_catalog_summary",
    # Master Pattern Generation
    "generate_pattern",
    # Individual Pattern Generators
    "generate_seed_of_life",
    "generate_flower_of_life",
    "generate_egg_of_life",
    "generate_fruit_of_life",
    "generate_tree_of_life",
    "generate_metatrons_cube",
    "generate_platonic_solid_projection",
    "get_metatrons_13_centers",
    "generate_fibonacci_sequence",
    "generate_golden_rectangles",
    "generate_golden_spiral",
    "generate_phyllotaxis",
    "generate_golden_triangle_spiral",
    "generate_sri_yantra",
    "generate_crop_circle",
    "generate_milk_hill_glyph",
    "generate_julia_set_glyph",
    "generate_barbury_castle_glyph",
    "generate_chilbolton_binary_glyph",
    "generate_triskele_glyph",
    "generate_merkaba",
    "generate_torus",
    "generate_golden_ratio_torus",
    "generate_torus_knot",
    "generate_vesica_piscis",
    "generate_star_polyhedron_projection",
    "generate_cymatic_resonance_pattern",
    "get_sacred_frequency",
    "list_sacred_frequencies",
    "SacredFrequency",
    "SACRED_FREQUENCY_MATRIX",
    # Exporters
    "export_svg",
    "export_dxf",
    "export_obj",
    "SVGExporter",
    "DXFExporter",
    "OBJExporter",
    "SVG_THEMES",
    # Compat
    "atomic_write_bytes",
    "atomic_write_text",
    "get_platform_info",
    "is_linux",
    "is_macos",
    "is_termux",
    "is_windows",
    "normalize_path",
    "read_text_safe",
    "read_json_safe",
    "write_json_safe",
    "safe_delete",
]
