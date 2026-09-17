"""Pure Standard Library AutoCAD DXF (R12/R2000 ASCII) Exporter.

Compatible with CNC routers, laser cutters (LightBurn, RDWorks, LaserCut),
vinyl plotters, FreeCAD, AutoCAD, Rhino, and Inkscape.
100% Python Standard Library.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..compat import atomic_write_text
from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Point3D, Polygon, Spline


def hex_to_aci(hex_color: str) -> int:
    """Map Hex/CSS color to closest AutoCAD Color Index (ACI 1..7).

    ACI Standards:
    1 = Red
    2 = Yellow
    3 = Green
    4 = Cyan
    5 = Blue
    6 = Magenta
    7 = White / Black
    """
    clean_hex = hex_color.lstrip("#").lower()
    if len(clean_hex) == 3:
        clean_hex = "".join([c * 2 for c in clean_hex])

    try:
        r = int(clean_hex[0:2], 16)
        g = int(clean_hex[2:4], 16)
        b = int(clean_hex[4:6], 16)
    except (ValueError, IndexError):
        return 7  # Default white

    # Check color distance to primary ACI palette
    aci_palette = {
        1: (255, 0, 0),  # Red
        2: (255, 255, 0),  # Yellow / Gold
        3: (0, 255, 0),  # Green
        4: (0, 255, 255),  # Cyan
        5: (0, 0, 255),  # Blue
        6: (255, 0, 255),  # Magenta
        7: (255, 255, 255),  # White
    }

    best_aci = 7
    best_dist = float("inf")
    for aci, (pr, pg, pb) in aci_palette.items():
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < best_dist:
            best_dist = dist
            best_aci = aci

    return best_aci


class DXFExporter:
    """AutoCAD R2000 (AC1015) ASCII DXF Exporter for CNC & Laser Machining."""

    def __init__(
        self,
        precision: int = 6,
        units_mm: bool = True,
        default_layer: str = "0",
    ) -> None:
        self.precision = precision
        self.units_mm = units_mm
        self.default_layer = default_layer

    def _fmt(self, val: float) -> str:
        """Format coordinate float for DXF."""
        return f"{val:.{self.precision}f}"

    def export(self, ast: GeometryAST) -> str:
        """Serialize GeometryAST to ASCII DXF R2000 string."""
        bb = ast.bounds()

        # Discover all unique layers in AST
        layer_names = set(ast.layers.keys())
        for l in ast.lines:
            layer_names.add(l.layer)
        for c in ast.circles:
            layer_names.add(c.layer)
        for a in ast.arcs:
            layer_names.add(a.layer)
        for p in ast.polygons:
            layer_names.add(p.layer)
        for s in ast.splines:
            layer_names.add(s.layer)

        if not layer_names:
            layer_names.add("0")

        lines: List[str] = []

        def add_code(code: int, val: Any) -> None:
            lines.append(f"{code:>3}")
            lines.append(str(val))

        # -------------------------------------------------------------
        # 1. HEADER SECTION
        # -------------------------------------------------------------
        add_code(0, "SECTION")
        add_code(2, "HEADER")

        # AutoCAD Version R2000 (AC1015)
        add_code(9, "$ACADVER")
        add_code(1, "AC1015")

        # Units: 4 = Millimeters, 1 = Inches
        add_code(9, "$INSUNITS")
        add_code(70, 4 if self.units_mm else 1)

        # Drawing Extents
        add_code(9, "$EXTMIN")
        add_code(10, self._fmt(bb.min_x))
        add_code(20, self._fmt(bb.min_y))
        add_code(30, "0.0")

        add_code(9, "$EXTMAX")
        add_code(10, self._fmt(bb.max_x))
        add_code(20, self._fmt(bb.max_y))
        add_code(30, "0.0")

        add_code(0, "ENDSEC")

        # -------------------------------------------------------------
        # 2. TABLES SECTION
        # -------------------------------------------------------------
        add_code(0, "SECTION")
        add_code(2, "TABLES")

        # LTYPE Table
        add_code(0, "TABLE")
        add_code(2, "LTYPE")
        add_code(70, 1)

        add_code(0, "LTYPE")
        add_code(2, "CONTINUOUS")
        add_code(70, 64)
        add_code(3, "Solid line")
        add_code(72, 65)
        add_code(73, 0)
        add_code(40, "0.0")

        add_code(0, "ENDTAB")

        # LAYER Table
        add_code(0, "TABLE")
        add_code(2, "LAYER")
        add_code(70, len(layer_names))

        for l_name in sorted(layer_names):
            layer_meta = ast.layers.get(l_name, {})
            hex_c = layer_meta.get("color", "#00ffff")
            aci_color = hex_to_aci(hex_c)

            add_code(0, "LAYER")
            add_code(2, l_name)
            add_code(70, 0)
            add_code(62, aci_color)
            add_code(6, "CONTINUOUS")

        add_code(0, "ENDTAB")
        add_code(0, "ENDSEC")

        # -------------------------------------------------------------
        # 3. BLOCKS SECTION (Empty)
        # -------------------------------------------------------------
        add_code(0, "SECTION")
        add_code(2, "BLOCKS")
        add_code(0, "ENDSEC")

        # -------------------------------------------------------------
        # 4. ENTITIES SECTION
        # -------------------------------------------------------------
        add_code(0, "SECTION")
        add_code(2, "ENTITIES")

        # Render LineSegments -> LINE
        for line in ast.lines:
            add_code(0, "LINE")
            add_code(8, line.layer or self.default_layer)
            add_code(62, hex_to_aci(line.color))
            # Start Point
            add_code(10, self._fmt(line.start.x))
            add_code(20, self._fmt(line.start.y))
            add_code(30, "0.0")
            # End Point
            add_code(11, self._fmt(line.end.x))
            add_code(21, self._fmt(line.end.y))
            add_code(31, "0.0")

        # Render Circles -> CIRCLE
        for circle in ast.circles:
            add_code(0, "CIRCLE")
            add_code(8, circle.layer or self.default_layer)
            add_code(62, hex_to_aci(circle.color))
            # Center Point
            add_code(10, self._fmt(circle.center.x))
            add_code(20, self._fmt(circle.center.y))
            add_code(30, "0.0")
            # Radius
            add_code(40, self._fmt(circle.radius))

        # Render Arcs -> ARC
        for arc in ast.arcs:
            start_deg = math.degrees(arc.start_angle) % 360.0
            end_deg = math.degrees(arc.end_angle) % 360.0

            add_code(0, "ARC")
            add_code(8, arc.layer or self.default_layer)
            add_code(62, hex_to_aci(arc.color))
            # Center Point
            add_code(10, self._fmt(arc.center.x))
            add_code(20, self._fmt(arc.center.y))
            add_code(30, "0.0")
            # Radius
            add_code(40, self._fmt(arc.radius))
            # Start and End Angles in degrees
            add_code(50, self._fmt(start_deg))
            add_code(51, self._fmt(end_deg))

        # Render Polygons -> LWPOLYLINE
        for poly in ast.polygons:
            if not poly.points:
                continue
            add_code(0, "LWPOLYLINE")
            add_code(8, poly.layer or self.default_layer)
            add_code(62, hex_to_aci(poly.color))
            add_code(90, len(poly.points))
            add_code(70, 1 if poly.closed else 0)  # 1 = closed, 0 = open
            add_code(43, "0.0")  # Constant width

            for p in poly.points:
                add_code(10, self._fmt(p.x))
                add_code(20, self._fmt(p.y))

        # Render Splines -> sampled LWPOLYLINE
        for spline in ast.splines:
            pts = spline.sample_points(samples_per_segment=16)
            if not pts:
                continue
            add_code(0, "LWPOLYLINE")
            add_code(8, spline.layer or self.default_layer)
            add_code(62, hex_to_aci(spline.color))
            add_code(90, len(pts))
            add_code(70, 1 if spline.closed else 0)
            add_code(43, "0.0")

            for p in pts:
                add_code(10, self._fmt(p.x))
                add_code(20, self._fmt(p.y))

        add_code(0, "ENDSEC")

        # -------------------------------------------------------------
        # 5. EOF
        # -------------------------------------------------------------
        add_code(0, "EOF")

        return "\n".join(lines) + "\n"

    def export_to_file(self, ast: GeometryAST, output_path: Union[str, Path]) -> Path:
        """Export AST to DXF file atomically."""
        dxf_content = self.export(ast)
        return atomic_write_text(output_path, dxf_content)


def export_dxf(
    ast: GeometryAST,
    file_path: Optional[Union[str, Path]] = None,
    units_mm: bool = True,
    precision: int = 6,
) -> str:
    """Convenience function to export GeometryAST to DXF string and optional file."""
    exporter = DXFExporter(precision=precision, units_mm=units_mm)
    dxf_str = exporter.export(ast)
    if file_path:
        exporter.export_to_file(ast, file_path)
    return dxf_str
