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
    generate_pattern as catalog_generate_pattern,
    get_catalog_summary,
    get_preset as catalog_get_preset,
    list_categories,
    list_presets as catalog_list_presets,
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
    generate_torus_knot,
    generate_tree_of_life,
    generate_triskele_glyph,
    generate_vesica_piscis,
    get_metatrons_13_centers,
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

# Compatibility alias for Point and Line
Point = Point2D
Line = LineSegment

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

PRESETS_CATALOG: Dict[str, PatternPreset] = PRESETS


def get_preset(preset_id: str) -> Optional[PatternPreset]:
    """Retrieve a preset definition by its unique identifier."""
    return catalog_get_preset(preset_id)


def list_presets(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[PatternPreset]:
    """Query presets with optional filtering by category, tag, or difficulty."""
    return catalog_list_presets(category=category, tag=tag, difficulty=difficulty)


def generate_pattern(
    pattern_id: str,
    custom_params: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> GeometryAST:
    """Master generator dispatcher routing pattern requests with keyword translation."""
    return catalog_generate_pattern(pattern_id, custom_params=custom_params, **kwargs)


# -----------------------------------------------------------------------------
# Exporters Wrapper Functions
# -----------------------------------------------------------------------------
def export_svg(
    ast_or_pattern: Union[GeometryAST, str],
    file_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    theme: str = "dark_gold",
    stroke_width: Optional[float] = None,
    glow: Optional[bool] = None,
    padding: float = 45.0,
    **kwargs: Any,
) -> str:
    """Exports geometry pattern as publication-grade vector SVG XML markup."""
    if isinstance(ast_or_pattern, str):
        ast = generate_pattern(ast_or_pattern, **kwargs)
    else:
        ast = ast_or_pattern

    target_path = file_path or output_path
    theme_name = THEME_MAP.get(theme, theme)
    return raw_export_svg(
        ast,
        file_path=target_path,
        theme=theme_name,
        glow=glow,
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

    target_path = file_path or output_path
    return raw_export_dxf(ast, file_path=target_path, **kwargs)


def export_obj(
    ast_or_pattern: Union[GeometryAST, str],
    file_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    extrusion: float = 5.0,
    relief_depth: Optional[float] = None,
    medallion_base: Optional[bool] = None,
    base_type: str = "cylinder",
    **kwargs: Any,
) -> str:
    """Exports geometry as 3D embossed mesh (Wavefront OBJ)."""
    if isinstance(ast_or_pattern, str):
        ast = generate_pattern(ast_or_pattern, **kwargs)
    else:
        ast = ast_or_pattern

    target_path = file_path or output_path
    eff_relief = relief_depth if relief_depth is not None else extrusion
    return raw_export_obj(
        ast,
        file_path=target_path,
        relief_depth=eff_relief,
        medallion_base=medallion_base,
        base_type=base_type,
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
    "generate_torus_knot",
    "generate_vesica_piscis",
    # Exporters
    "export_svg",
    "export_dxf",
    "export_obj",
    "SVGExporter",
    "DXFExporter",
    "OBJExporter",
    "SVG_THEMES",
    # Compat
    "get_platform_info",
    "is_windows",
    "is_macos",
    "is_linux",
    "is_termux",
    "normalize_path",
    "atomic_write_text",
    "atomic_write_bytes",
    "read_text_safe",
    "read_json_safe",
    "write_json_safe",
    "safe_delete",
]
