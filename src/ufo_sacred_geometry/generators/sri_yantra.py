"""Sri Yantra (Sri Chakra) Sacred Vedic Cosmogram Generator.

Implements:
- 9 Interlocking Isosceles Triangles (4 Shiva upward, 5 Shakti downward) forming 43 secondary triangles
- Central Bindu point (Supreme Consciousness)
- 8-Petal Inner Lotus (Sarva Samkshobhana)
- 16-Petal Outer Lotus (Sarva Vidravana)
- 3 Concentric Girdle Rings (Mekhala-traya)
- Triple-tiered Bhupura (Earth Citadel) with 4 Cardinal T-Portico Gateways
100% Python Standard Library.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Polygon, Spline


def _create_lotus_petal(
    center: Point2D,
    inner_radius: float,
    outer_radius: float,
    angle_rad: float,
    petal_span_rad: float,
    color: str,
    stroke_width: float,
    layer: str,
) -> Polygon:
    """Create a curved lotus petal vertex path."""
    tip = Point2D.from_polar(outer_radius, angle_rad, origin=center)
    base_left = Point2D.from_polar(inner_radius, angle_rad - petal_span_rad / 2.0, origin=center)
    base_right = Point2D.from_polar(inner_radius, angle_rad + petal_span_rad / 2.0, origin=center)

    # Midpoint control bulges for petal curvature
    mid_r = (inner_radius + outer_radius) * 0.58
    mid_left = Point2D.from_polar(mid_r, angle_rad - petal_span_rad * 0.45, origin=center)
    mid_right = Point2D.from_polar(mid_r, angle_rad + petal_span_rad * 0.45, origin=center)

    points = [base_left, mid_left, tip, mid_right, base_right]
    return Polygon(
        points=points,
        stroke_width=stroke_width,
        color=color,
        layer=layer,
        closed=False,
    )


def generate_sri_yantra(
    size: float = 180.0,
    scale: Optional[float] = None,
    lotus_petals: Optional[int] = None,
    include_bhupura: Optional[bool] = None,
    center_x: float = 0.0,
    center_y: float = 0.0,
    show_petals: bool = True,
    show_bhupura: bool = True,
    show_bindu: bool = True,
    stroke_width: float = 1.0,
    triangle_color: str = "#ffd700",
    petals_color: str = "#00f0ff",
    bhupura_color: str = "#ff007f",
    bindu_color: str = "#ffffff",
    layer: str = "sri_yantra_core",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the complete Sri Yantra with 9 interlocking triangles, lotuses, and Bhupura."""
    if scale is not None:
        size = scale
    if include_bhupura is not None:
        show_bhupura = include_bhupura

    ast = GeometryAST(
        title="Sri Yantra (Sri Chakra)",
        description="The Master Cosmogram of Vedic sacred geometry with 9 interlocking Shiva/Shakti triangles, 43 sub-triangles, 24 lotus petals, and 4-gate Bhupura.",
        parameters={
            "size": size,
            "scale": size,
            "center_x": center_x,
            "center_y": center_y,
            "show_petals": show_petals,
            "show_bhupura": show_bhupura,
            "show_bindu": show_bindu,
            "stroke_width": stroke_width,
        },
        tags=["sacred_geometry", "sri_yantra", "vedic", "tantra", "mandala", "yantra", "chakra"],
        layers={
            layer: {"color": triangle_color, "stroke_width": stroke_width * 1.2},
            "lotus_petals": {"color": petals_color, "stroke_width": stroke_width},
            "bhupura": {"color": bhupura_color, "stroke_width": stroke_width * 1.5},
            "bindu": {"color": bindu_color, "stroke_width": stroke_width * 2.0},
        },
    )


    c0 = Point2D(center_x, center_y)
    r_core = size * 0.45  # Enclosing radius of 9 central triangles

    # 1. Authentic 9 Triangles Normalized Geometry
    # Triangle definitions: (y_apex_factor, y_base_factor, base_width_factor, is_upward)
    # y coordinates normalized to r_core
    triangle_specs: List[Tuple[float, float, float, bool]] = [
        # Upward Shiva 1 (Largest base top, apex bottom)
        (-0.92, 0.78, 0.88, True),
        # Downward Shakti 1 (Largest base bottom, apex top)
        (0.92, -0.78, 0.88, False),
        # Upward Shiva 2
        (-0.70, 0.54, 0.76, True),
        # Downward Shakti 2
        (0.70, -0.54, 0.76, False),
        # Upward Shiva 3
        (-0.48, 0.32, 0.62, True),
        # Downward Shakti 3
        (0.48, -0.32, 0.62, False),
        # Upward Shiva 4
        (-0.28, 0.14, 0.46, True),
        # Downward Shakti 4
        (0.28, -0.14, 0.46, False),
        # Downward Shakti 5 (Central innermost triangle)
        (-0.16, 0.08, 0.28, False),
    ]

    for y_apex_f, y_base_f, w_base_f, is_up in triangle_specs:
        apex_y = c0.y - (y_apex_f * r_core)  # Inverted Y for screen coords
        base_y = c0.y - (y_base_f * r_core)
        half_w = (w_base_f * r_core)

        apex = Point2D(c0.x, apex_y)
        base_left = Point2D(c0.x - half_w, base_y)
        base_right = Point2D(c0.x + half_w, base_y)

        ast.add_polygon(
            [apex, base_left, base_right],
            stroke_width=stroke_width * 1.1,
            color=triangle_color,
            layer=layer,
            closed=True,
        )

    # 2. Central Bindu Point
    if show_bindu:
        ast.add_circle(
            c0,
            r_core * 0.035,
            stroke_width=stroke_width * 1.5,
            color=bindu_color,
            fill=bindu_color,
            layer="bindu",
        )

    # Inner core boundary ring
    ast.add_circle(
        c0,
        r_core,
        stroke_width=stroke_width,
        color=triangle_color,
        layer=layer,
    )

    # 3. 8-Petal and 16-Petal Lotuses
    if show_petals:
        # Inner 8-Petal Lotus
        r_lotus1_in = r_core
        r_lotus1_out = size * 0.58
        ast.add_circle(c0, r_lotus1_out, stroke_width=stroke_width * 0.8, color=petals_color, layer="lotus_petals")
        for i in range(8):
            ang = i * (math.pi / 4.0)
            petal = _create_lotus_petal(
                c0,
                r_lotus1_in,
                r_lotus1_out,
                ang,
                math.pi / 4.0,
                petals_color,
                stroke_width,
                "lotus_petals",
            )
            ast.polygons.append(petal)

        # Outer 16-Petal Lotus
        r_lotus2_in = r_lotus1_out
        r_lotus2_out = size * 0.72
        ast.add_circle(c0, r_lotus2_out, stroke_width=stroke_width * 0.8, color=petals_color, layer="lotus_petals")
        for i in range(16):
            ang = i * (math.pi / 8.0)
            petal = _create_lotus_petal(
                c0,
                r_lotus2_in,
                r_lotus2_out,
                ang,
                math.pi / 8.0,
                petals_color,
                stroke_width,
                "lotus_petals",
            )
            ast.polygons.append(petal)

        # 3 Concentric Girdle Rings (Mekhala-traya)
        ast.add_circle(c0, size * 0.76, stroke_width=stroke_width, color=petals_color, layer="lotus_petals")
        ast.add_circle(c0, size * 0.79, stroke_width=stroke_width * 1.2, color=petals_color, layer="lotus_petals")
        ast.add_circle(c0, size * 0.82, stroke_width=stroke_width, color=petals_color, layer="lotus_petals")

    # 4. Triple-tiered Bhupura (Earth Citadel with 4 Cardinal T-Gates)
    if show_bhupura:
        base_s = size * 0.88
        for tier, tier_scale in enumerate([1.0, 1.05, 1.10]):
            s = base_s * tier_scale
            # Build 4-gated square with T-shaped portals on N, E, S, W
            gate_w = s * 0.28
            gate_d = s * 0.08

            # Perimeter polyline segments with stepped gate recesses
            # Top (North)
            p_tl = Point2D(c0.x - s, c0.y - s)
            p_tr = Point2D(c0.x + s, c0.y - s)
            p_br = Point2D(c0.x + s, c0.y + s)
            p_bl = Point2D(c0.x - s, c0.y + s)

            # North Gate
            g_n1 = Point2D(c0.x - gate_w / 2.0, c0.y - s)
            g_n2 = Point2D(c0.x - gate_w / 2.0, c0.y - s - gate_d)
            g_n3 = Point2D(c0.x + gate_w / 2.0, c0.y - s - gate_d)
            g_n4 = Point2D(c0.x + gate_w / 2.0, c0.y - s)

            # East Gate
            g_e1 = Point2D(c0.x + s, c0.y - gate_w / 2.0)
            g_e2 = Point2D(c0.x + s + gate_d, c0.y - gate_w / 2.0)
            g_e3 = Point2D(c0.x + s + gate_d, c0.y + gate_w / 2.0)
            g_e4 = Point2D(c0.x + s, c0.y + gate_w / 2.0)

            # South Gate
            g_s1 = Point2D(c0.x + gate_w / 2.0, c0.y + s)
            g_s2 = Point2D(c0.x + gate_w / 2.0, c0.y + s + gate_d)
            g_s3 = Point2D(c0.x - gate_w / 2.0, c0.y + s + gate_d)
            g_s4 = Point2D(c0.x - gate_w / 2.0, c0.y + s)

            # West Gate
            g_w1 = Point2D(c0.x - s, c0.y + gate_w / 2.0)
            g_w2 = Point2D(c0.x - s - gate_d, c0.y + gate_w / 2.0)
            g_w3 = Point2D(c0.x - s - gate_d, c0.y - gate_w / 2.0)
            g_w4 = Point2D(c0.x - s, c0.y - gate_w / 2.0)

            gate_outline = [
                p_tl,
                g_n1,
                g_n2,
                g_n3,
                g_n4,
                p_tr,
                g_e1,
                g_e2,
                g_e3,
                g_e4,
                p_br,
                g_s1,
                g_s2,
                g_s3,
                g_s4,
                p_bl,
                g_w1,
                g_w2,
                g_w3,
                g_w4,
            ]

            ast.add_polygon(
                gate_outline,
                stroke_width=stroke_width * (1.3 if tier == 0 else 1.0),
                color=bhupura_color,
                layer="bhupura",
                closed=True,
            )

    return ast
