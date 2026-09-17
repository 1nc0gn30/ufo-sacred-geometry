"""High-Fidelity SVG Vector Exporter for Sacred Geometry & Crop Circles.

Features:
- Dark Mode Neon, Sacred Gold, Cosmic Cyan, Technical Blueprint, and Light Minimal themes
- SVG Gaussian Blur Glow Filters (`feGaussianBlur` + `feMerge`)
- Layer grouping `<g id="...">` with per-layer styling
- Exact arc math with SVG path `A` commands
- High-precision coordinate formatting
- Self-contained standalone SVG with XML declaration and viewBox
- Pure Python standard library with atomic file write support.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..compat import atomic_write_text
from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Polygon, Spline

# Preset Color Themes
SVG_THEMES: Dict[str, Dict[str, Any]] = {
    "dark_gold": {
        "bg_color_1": "#0f0f18",
        "bg_color_2": "#05050a",
        "default_stroke": "#ffd700",
        "glow_color": "#ffaa00",
        "grid_color": "#2a2215",
        "text_color": "#e0c068",
        "show_glow": True,
    },
    "neon_ufo": {
        "bg_color_1": "#0c1022",
        "bg_color_2": "#04050d",
        "default_stroke": "#00f0ff",
        "glow_color": "#39ff14",
        "grid_color": "#112233",
        "text_color": "#00f0ff",
        "show_glow": True,
    },
    "cosmic_purple": {
        "bg_color_1": "#180828",
        "bg_color_2": "#080210",
        "default_stroke": "#e056fd",
        "glow_color": "#bf00ff",
        "grid_color": "#2c153f",
        "text_color": "#f3a4ff",
        "show_glow": True,
    },
    "blueprint": {
        "bg_color_1": "#0e2a47",
        "bg_color_2": "#071626",
        "default_stroke": "#e0fbfc",
        "glow_color": "#48cae4",
        "grid_color": "#1b3b5f",
        "text_color": "#8da9c4",
        "show_glow": False,
    },
    "light_minimal": {
        "bg_color_1": "#ffffff",
        "bg_color_2": "#f5f6fa",
        "default_stroke": "#1a1a24",
        "glow_color": "#718093",
        "grid_color": "#e1e2e6",
        "text_color": "#2f3640",
        "show_glow": False,
    },
    "monochrome_laser": {
        "bg_color_1": "#000000",
        "bg_color_2": "#000000",
        "default_stroke": "#ffffff",
        "glow_color": "#ffffff",
        "grid_color": "#222222",
        "text_color": "#ffffff",
        "show_glow": False,
    },
}

# Theme aliases for CLI and UI compatibility
SVG_THEMES["gold"] = SVG_THEMES["dark_gold"]
SVG_THEMES["sacred_gold"] = SVG_THEMES["dark_gold"]
SVG_THEMES["neon_matrix"] = SVG_THEMES["neon_ufo"]
SVG_THEMES["obsidian_dark"] = SVG_THEMES["dark_gold"]


class SVGExporter:
    """Configurable SVG Vector Exporter for Sacred Geometry AST."""

    def __init__(
        self,
        theme: str = "dark_gold",
        width: float = 900.0,
        height: float = 900.0,
        padding: float = 45.0,
        precision: int = 4,
        glow: Optional[bool] = None,
        custom_bg: Optional[str] = None,
        include_metadata_header: bool = True,
    ) -> None:
        self.theme_name = theme if theme in SVG_THEMES else "dark_gold"
        self.theme = SVG_THEMES[self.theme_name]
        self.width = width
        self.height = height
        self.padding = padding
        self.precision = precision
        self.glow = glow if glow is not None else self.theme.get("show_glow", False)
        self.custom_bg = custom_bg
        self.include_metadata_header = include_metadata_header

    def _fmt(self, val: float) -> str:
        """Format floating point numbers to configured precision without trailing zeroes."""
        formatted = f"{val:.{self.precision}f}"
        if "." in formatted:
            formatted = formatted.rstrip("0").rstrip(".")
        return formatted

    def _render_line(self, line: LineSegment) -> str:
        x1, y1 = self._fmt(line.start.x), self._fmt(line.start.y)
        x2, y2 = self._fmt(line.end.x), self._fmt(line.end.y)
        sw = self._fmt(line.stroke_width)
        op = f' stroke-opacity="{line.opacity:.2f}"' if line.opacity < 1.0 else ""
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{line.color}" stroke-width="{sw}"{op}/>'

    def _render_circle(self, c: Circle) -> str:
        cx, cy = self._fmt(c.center.x), self._fmt(c.center.y)
        r = self._fmt(c.radius)
        sw = self._fmt(c.stroke_width)
        fill_attr = f'fill="{c.fill}"' if c.fill else 'fill="none"'
        op = f' stroke-opacity="{c.opacity:.2f}"' if c.opacity < 1.0 else ""
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{c.color}" stroke-width="{sw}" {fill_attr}{op}/>'

    def _render_arc(self, a: Arc) -> str:
        r = self._fmt(a.radius)
        sw = self._fmt(a.stroke_width)
        op = f' stroke-opacity="{a.opacity:.2f}"' if a.opacity < 1.0 else ""

        # Sweep angle
        sweep_rad = (a.end_angle - a.start_angle) % (2.0 * math.pi)
        if sweep_rad < 0:
            sweep_rad += 2.0 * math.pi

        # If full circle
        if abs(sweep_rad) < 1e-4 or abs(sweep_rad - 2.0 * math.pi) < 1e-4:
            cx, cy = self._fmt(a.center.x), self._fmt(a.center.y)
            return f'<circle cx="{cx}" cy="{cy}" r="{r}" stroke="{a.color}" stroke-width="{sw}" fill="none"{op}/>'

        # Start and end coordinates
        p1 = a.start_point
        p2 = a.end_point
        x1, y1 = self._fmt(p1.x), self._fmt(p1.y)
        x2, y2 = self._fmt(p2.x), self._fmt(p2.y)

        large_arc = "1" if sweep_rad > math.pi else "0"
        sweep_flag = "1"

        d = f"M {x1} {y1} A {r} {r} 0 {large_arc} {sweep_flag} {x2} {y2}"
        return f'<path d="{d}" stroke="{a.color}" stroke-width="{sw}" fill="none"{op}/>'

    def _render_polygon(self, poly: Polygon) -> str:
        if not poly.points:
            return ""
        pts_str = " ".join(f"{self._fmt(p.x)},{self._fmt(p.y)}" for p in poly.points)
        sw = self._fmt(poly.stroke_width)
        fill_attr = f'fill="{poly.fill}"' if poly.fill else 'fill="none"'
        op = f' stroke-opacity="{poly.opacity:.2f}"' if poly.opacity < 1.0 else ""
        tag = "polygon" if poly.closed else "polyline"
        return f'<{tag} points="{pts_str}" stroke="{poly.color}" stroke-width="{sw}" {fill_attr}{op}/>'

    def _render_spline(self, sp: Spline) -> str:
        sampled = sp.sample_points(samples_per_segment=14)
        if not sampled:
            return ""
        pts_str = " ".join(f"{self._fmt(p.x)},{self._fmt(p.y)}" for p in sampled)
        sw = self._fmt(sp.stroke_width)
        op = f' stroke-opacity="{sp.opacity:.2f}"' if sp.opacity < 1.0 else ""
        tag = "polygon" if sp.closed else "polyline"
        return f'<{tag} points="{pts_str}" stroke="{sp.color}" stroke-width="{sw}" fill="none"{op}/>'

    def export(self, ast: GeometryAST) -> str:
        """Export the given GeometryAST into a complete SVG document string."""
        # Calculate bounds
        bb = ast.bounds()

        # ViewBox computation
        min_x = bb.min_x - self.padding
        min_y = bb.min_y - self.padding
        vb_w = max(1.0, bb.width + 2.0 * self.padding)
        vb_h = max(1.0, bb.height + 2.0 * self.padding)

        # Make viewBox square if width and height are equal
        if abs(vb_w - vb_h) > 1e-4:
            dim = max(vb_w, vb_h)
            min_x -= (dim - vb_w) / 2.0
            min_y -= (dim - vb_h) / 2.0
            vb_w = dim
            vb_h = dim

        vb_str = f"{self._fmt(min_x)} {self._fmt(min_y)} {self._fmt(vb_w)} {self._fmt(vb_h)}"

        # Group primitives by layer
        layers_map: Dict[str, List[str]] = {}

        for line in ast.lines:
            layers_map.setdefault(line.layer, []).append(self._render_line(line))

        for circle in ast.circles:
            layers_map.setdefault(circle.layer, []).append(self._render_circle(circle))

        for arc in ast.arcs:
            layers_map.setdefault(arc.layer, []).append(self._render_arc(arc))

        for poly in ast.polygons:
            layers_map.setdefault(poly.layer, []).append(self._render_polygon(poly))

        for spline in ast.splines:
            layers_map.setdefault(spline.layer, []).append(self._render_spline(spline))

        # Build SVG Document
        lines: List[str] = [
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_str}" width="{self._fmt(self.width)}" height="{self._fmt(self.height)}">',
            "  <defs>",
        ]

        # Radial Background Gradient
        bg1 = self.custom_bg or self.theme["bg_color_1"]
        bg2 = self.theme["bg_color_2"]
        lines.append('    <radialGradient id="bg_grad" cx="50%" cy="50%" r="75%">')
        lines.append(f'      <stop offset="0%" stop-color="{bg1}"/>')
        lines.append(f'      <stop offset="100%" stop-color="{bg2}"/>')
        lines.append("    </radialGradient>")

        # Glow Filter
        if self.glow:
            lines.append('    <filter id="sacred_glow" x="-30%" y="-30%" width="160%" height="160%">')
            lines.append('      <feGaussianBlur stdDeviation="3.0" result="coloredBlur"/>')
            lines.append("      <feMerge>")
            lines.append('        <feMergeNode in="coloredBlur"/>')
            lines.append('        <feMergeNode in="SourceGraphic"/>')
            lines.append("      </feMerge>")
            lines.append("    </filter>")

        lines.append("  </defs>")

        # Background Rect
        lines.append(
            f'  <rect x="{self._fmt(min_x)}" y="{self._fmt(min_y)}" width="{self._fmt(vb_w)}" height="{self._fmt(vb_h)}" fill="url(#bg_grad)"/>'
        )

        # Layers Render
        filter_attr = ' filter="url(#sacred_glow)"' if self.glow else ""

        lines.append(f'  <g id="geometry_content"{filter_attr} stroke-linecap="round" stroke-linejoin="round">')

        for layer_name, layer_items in layers_map.items():
            lines.append(f'    <g id="layer_{layer_name}">')
            for item in layer_items:
                lines.append(f"      {item}")
            lines.append("    </g>")

        lines.append("  </g>")

        # Optional Title/Metadata Watermark Header
        if self.include_metadata_header and ast.title:
            tx = min_x + 20.0
            ty = min_y + vb_h - 20.0
            lines.append(f'  <g id="metadata" opacity="0.6">')
            lines.append(
                f'    <text x="{self._fmt(tx)}" y="{self._fmt(ty)}" fill="{self.theme["text_color"]}" font-family="sans-serif, monospace" font-size="12" letter-spacing="1.5">{ast.title.upper()}</text>'
            )
            lines.append("  </g>")

        lines.append("</svg>")
        return "\n".join(lines) + "\n"

    def export_to_file(self, ast: GeometryAST, output_path: Union[str, Path]) -> Path:
        """Export AST to SVG file atomically."""
        svg_content = self.export(ast)
        return atomic_write_text(output_path, svg_content)


def export_svg(
    ast: GeometryAST,
    file_path: Optional[Union[str, Path]] = None,
    theme: str = "dark_gold",
    width: float = 900.0,
    height: float = 900.0,
    padding: float = 45.0,
    glow: Optional[bool] = None,
    show_glow: Optional[bool] = None,
    custom_bg: Optional[str] = None,
    stroke_width: Optional[float] = None,
    **kwargs: Any,
) -> str:
    """Convenience function to export GeometryAST to SVG string and optional file."""
    effective_glow = glow if glow is not None else show_glow
    exporter = SVGExporter(
        theme=theme,
        width=width,
        height=height,
        padding=padding,
        glow=effective_glow,
        custom_bg=custom_bg,
    )
    svg_str = exporter.export(ast)
    if file_path:
        exporter.export_to_file(ast, file_path)
    return svg_str

