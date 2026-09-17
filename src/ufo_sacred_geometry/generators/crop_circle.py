"""Authentic Extraterrestrial Agro-Glyph & Crop Circle Synthesizer.

Implements:
1. Milk Hill 2001 (Colossal 409-Circle 6-Arm Logarithmic Spiral Glyph)
2. Julia Set Spiral 1996 (Stonehenge 151-Circle Fractal Spiral)
3. Barbury Castle 1991 (Triangular Tetrahedron & Ratcheted Sunburst Glyph)
4. Chilbolton 2001 (Binary Telemetry Matrix & Arecibo Reply Glyph)
5. Windmill Hill Triskele (Triple Vortex Harmonic Agro-Glyph)
100% Python Standard Library.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Polygon


def generate_milk_hill_glyph(
    radius: Optional[float] = None,
    scale: float = 220.0,
    arms: int = 6,
    circles_per_arm: int = 68,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 0.8,
    glyph_color: str = "#39ff14",
    fill_circles: bool = True,
    layer: str = "milk_hill_glyph",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the famous Milk Hill 2001 crop circle (409 circles in 6 logarithmic spiral arms)."""
    if radius is not None:
        scale = radius

    ast = GeometryAST(
        title="Milk Hill 409-Circle Crop Circle Glyph",
        description="The colossal 6-arm triple logarithmic spiral formation discovered at Milk Hill, Wiltshire (2001) comprising exactly 409 circles.",
        parameters={"scale": scale, "radius": scale, "arms": arms, "circles_per_arm": circles_per_arm, "stroke_width": stroke_width, "glyph_color": glyph_color},
        tags=["sacred_geometry", "crop_circle", "milk_hill", "ufo", "alien", "agro_glyph", "spiral"],
        layers={
            layer: {"color": glyph_color, "stroke_width": stroke_width},
            "guide_spirals": {"color": "#00f0ff", "stroke_width": 0.6, "opacity": 0.3},
        },
    )

    c0 = Point2D(center_x, center_y)

    # 1. Central origin circle
    r_center = scale * 0.035
    ast.add_circle(
        c0,
        r_center,
        stroke_width=stroke_width * 1.5,
        color=glyph_color,
        fill=glyph_color if fill_circles else None,
        layer=layer,
    )

    # 2. 6 Primary Spiral Arms (68 circles per arm = 408 circles)
    num_arms = arms
    spiral_b = 0.18  # Logarithmic growth parameter

    for arm in range(num_arms):
        arm_angle_base = arm * (2.0 * math.pi / num_arms)

        for i in range(1, circles_per_arm + 1):
            t = (i / float(circles_per_arm)) * 1.8 * math.pi
            dist = scale * 0.04 * math.exp(spiral_b * t)
            if dist > scale:
                dist = scale * (i / float(circles_per_arm))

            angle = arm_angle_base + t
            center_i = Point2D.from_polar(dist, angle, origin=c0)

            circle_r = max(0.8, scale * 0.008 * math.pow(i, 0.72))

            ast.add_circle(
                center_i,
                circle_r,
                stroke_width=stroke_width,
                color=glyph_color,
                fill=glyph_color if fill_circles else None,
                layer=layer,
                opacity=0.85,
            )

    return ast


def generate_julia_set_glyph(
    radius: Optional[float] = None,
    scale: float = 200.0,
    circles_count: Optional[int] = None,
    num_circles: int = 151,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.0,
    color: str = "#00f0ff",
    glyph_color: Optional[str] = None,
    fill_circles: bool = True,
    layer: str = "julia_set_glyph",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Stonehenge 1996 Julia Set Spiral Crop Circle."""
    if radius is not None:
        scale = radius
    if circles_count is not None:
        num_circles = circles_count
    if glyph_color is not None:
        color = glyph_color

    ast = GeometryAST(
        title="Stonehenge Julia Set Spiral Glyph",
        description="The legendary 151-circle Julia Set fractal agro-glyph that materialized opposite Stonehenge in July 1996.",
        parameters={"scale": scale, "radius": scale, "num_circles": num_circles, "circles_count": num_circles, "stroke_width": stroke_width, "color": color},
        tags=["sacred_geometry", "crop_circle", "julia_set", "stonehenge", "fractal", "spiral"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "spiral_axis": {"color": "#ff007f", "stroke_width": 0.8, "opacity": 0.35},
        },
    )

    c0 = Point2D(center_x, center_y)
    spiral_pts: List[Point2D] = []

    max_t = 3.2 * math.pi
    growth_rate = 0.22

    for i in range(num_circles):
        t = (i / float(max(1, num_circles - 1))) * max_t
        r_dist = scale * 0.05 * math.exp(growth_rate * t)
        pos = Point2D.from_polar(r_dist, t, origin=c0)
        spiral_pts.append(pos)

        c_radius = max(1.2, scale * 0.012 + (scale * 0.065) * math.pow(i / float(max(1, num_circles)), 1.6))

        ast.add_circle(
            pos,
            c_radius,
            stroke_width=stroke_width,
            color=color,
            fill=color if fill_circles else None,
            layer=layer,
            opacity=0.9,
        )

    for k in range(len(spiral_pts) - 1):
        ast.add_line(
            spiral_pts[k],
            spiral_pts[k + 1],
            stroke_width=0.8,
            color="#ff007f",
            layer="spiral_axis",
            opacity=0.35,
        )

    return ast


def generate_barbury_castle_glyph(
    radius: Optional[float] = None,
    scale: float = 180.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.2,
    color: str = "#ffd700",
    glyph_color: Optional[str] = None,
    layer: str = "barbury_castle",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Barbury Castle 1991 Triangular Tetrahedron & Sunburst Glyph."""
    if radius is not None:
        scale = radius
    if glyph_color is not None:
        color = glyph_color

    ast = GeometryAST(
        title="Barbury Castle Tetrahedron Glyph (1991)",
        description="The historic sacred triangular tetrahedron agro-glyph discovered at Barbury Castle encoding 3D polyhedral harmony and solar ratchets.",
        parameters={"scale": scale, "radius": scale, "stroke_width": stroke_width, "color": color},
        tags=["sacred_geometry", "crop_circle", "barbury_castle", "tetrahedron", "trinity", "sunburst"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "sunburst": {"color": "#ff007f", "stroke_width": stroke_width * 1.1},
            "corner_nodes": {"color": "#00f0ff", "stroke_width": stroke_width * 1.3},
        },
    )

    c0 = Point2D(center_x, center_y)

    corners: List[Point2D] = []
    for i in range(3):
        ang = (i * 2.0 * math.pi / 3.0) - (math.pi / 2.0)
        p = Point2D.from_polar(scale * 0.85, ang, origin=c0)
        corners.append(p)

    ast.add_polygon(corners, stroke_width=stroke_width * 1.4, color=color, layer=layer, closed=True)

    for corner in corners:
        ast.add_circle(corner, scale * 0.16, stroke_width=stroke_width, color="#00f0ff", layer="corner_nodes")
        ast.add_circle(corner, scale * 0.10, stroke_width=stroke_width * 1.2, color="#00f0ff", layer="corner_nodes")
        ast.add_circle(corner, scale * 0.04, stroke_width=stroke_width, color="#00f0ff", fill="#00f0ff", layer="corner_nodes")

    r_sun = scale * 0.28
    ast.add_circle(c0, r_sun, stroke_width=stroke_width * 1.3, color=color, layer=layer)
    ast.add_circle(c0, r_sun * 0.55, stroke_width=stroke_width, color=color, layer=layer)

    num_rays = 12
    for i in range(num_rays):
        ang = i * (2.0 * math.pi / num_rays)
        p_in = Point2D.from_polar(r_sun * 0.55, ang, origin=c0)
        p_out = Point2D.from_polar(r_sun, ang + (math.pi / 12.0), origin=c0)
        ast.add_line(p_in, p_out, stroke_width=stroke_width, color="#ff007f", layer="sunburst")

    for corner in corners:
        ast.add_line(c0, corner, stroke_width=stroke_width * 0.9, color=color, layer=layer, opacity=0.7)

    return ast


def generate_chilbolton_binary_glyph(
    width: Optional[float] = None,
    height: Optional[float] = None,
    scale: float = 200.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.0,
    color: str = "#39ff14",
    glyph_color: Optional[str] = None,
    layer: str = "chilbolton_binary",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Chilbolton 2001 Binary Reply & Telemetry Glyph."""
    if width is not None:
        scale = width * 2.0
    if glyph_color is not None:
        color = glyph_color

    ast = GeometryAST(
        title="Chilbolton Binary Message Glyph (2001)",
        description="The direct extraterrestrial binary reply to the 1974 Arecibo message discovered in the wheat fields of Chilbolton Observatory.",
        parameters={"scale": scale, "width": scale * 0.5, "height": scale, "stroke_width": stroke_width, "color": color},
        tags=["sacred_geometry", "crop_circle", "chilbolton", "arecibo", "binary", "alien_contact", "seti"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "matrix_border": {"color": "#00f0ff", "stroke_width": stroke_width * 1.5},
            "emitter_dish": {"color": "#ffd700", "stroke_width": stroke_width * 1.2},
        },
    )

    c0 = Point2D(center_x, center_y)

    cols = 23
    rows = 73
    cell_w = (scale * 0.8) / float(cols)
    cell_h = (scale * 1.8) / float(rows)

    start_x = c0.x - (cols * cell_w) / 2.0
    start_y = c0.y - (rows * cell_h) / 2.0

    ast.add_polygon(
        [
            Point2D(start_x - cell_w, start_y - cell_h),
            Point2D(start_x + cols * cell_w + cell_w, start_y - cell_h),
            Point2D(start_x + cols * cell_w + cell_w, start_y + rows * cell_h + cell_h),
            Point2D(start_x - cell_w, start_y + rows * cell_h + cell_h),
        ],
        stroke_width=stroke_width * 1.5,
        color="#00f0ff",
        layer="matrix_border",
    )

    for r in range(rows):
        for c in range(cols):
            bit_active = False

            if r < 7:
                bit_active = ((c + r * 3) % 2 == 1) and (c % 2 == 1)
            elif 7 <= r < 15:
                bit_active = (c in [2, 6, 10, 14, 18, 20]) and ((r - 7) % 3 != 0)
            elif 15 <= r < 33:
                phase = (r - 15) * 0.4
                x1 = int(11 + 6 * math.sin(phase))
                x2 = int(11 + 6 * math.sin(phase + 2.1))
                x3 = int(11 + 6 * math.sin(phase + 4.2))
                bit_active = (c in [x1, x2, x3]) or (c == 11 and r % 2 == 0)
            elif 33 <= r < 53:
                if 33 <= r < 40:
                    bit_active = abs(c - 11) <= (6 - (r - 33) // 2)
                elif 40 <= r < 48:
                    bit_active = (c == 11) or (abs(c - 11) == (r - 40))
                else:
                    bit_active = c in [9, 13]
            elif 53 <= r < 61:
                if r == 56:
                    bit_active = (c in [1, 3, 5, 7, 9, 11, 13, 15, 17, 19])
                elif r == 55:
                    bit_active = (c in [7, 9, 11])
            else:
                dish_y = r - 61
                bit_active = abs(c - 11) == dish_y

            if bit_active:
                px = start_x + c * cell_w
                py = start_y + r * cell_h
                ast.add_polygon(
                    [
                        Point2D(px, py),
                        Point2D(px + cell_w * 0.85, py),
                        Point2D(px + cell_w * 0.85, py + cell_h * 0.85),
                        Point2D(px, py + cell_h * 0.85),
                    ],
                    stroke_width=stroke_width * 0.7,
                    color=color,
                    fill=color,
                    layer=layer,
                )

    ast.add_circle(
        Point2D(c0.x, start_y + rows * cell_h + cell_h * 4),
        scale * 0.12,
        stroke_width=stroke_width * 1.3,
        color="#ffd700",
        layer="emitter_dish",
    )

    return ast


def generate_triskele_glyph(
    radius: Optional[float] = None,
    scale: float = 190.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.2,
    color: str = "#00f0ff",
    glyph_color: Optional[str] = None,
    layer: str = "triskele_vortex",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Windmill Hill Triskele Triple Vortex Crop Circle."""
    if radius is not None:
        scale = radius
    if glyph_color is not None:
        color = glyph_color

    ast = GeometryAST(
        title="Windmill Hill Triskele Vortex Glyph",
        description="Triple-spiral swirling vortex sacred formation with nested harmonic satellites.",
        parameters={"scale": scale, "radius": scale, "stroke_width": stroke_width, "color": color},
        tags=["sacred_geometry", "crop_circle", "triskele", "celtic", "vortex", "triple_spiral"],
        layers={layer: {"color": color, "stroke_width": stroke_width}},
    )

    c0 = Point2D(center_x, center_y)

    ast.add_circle(c0, scale * 0.15, stroke_width=stroke_width * 1.5, color=color, layer=layer)

    for arm in range(3):
        base_angle = arm * (2.0 * math.pi / 3.0)
        pts: List[Point2D] = []
        for i in range(40):
            t = (i / 39.0) * 1.5 * math.pi
            r = (scale * 0.15) + (scale * 0.7) * (i / 39.0)
            ang = base_angle + t
            p = Point2D.from_polar(r, ang, origin=c0)
            pts.append(p)

            if i % 8 == 0 and i > 0:
                sat_r = max(2.0, scale * 0.02 * (i / 10.0))
                ast.add_circle(p, sat_r, stroke_width=stroke_width, color=color, fill=color, layer=layer)

        for k in range(len(pts) - 1):
            ast.add_line(pts[k], pts[k + 1], stroke_width=stroke_width * 1.3, color=color, layer=layer)

    ast.add_circle(c0, scale * 0.95, stroke_width=stroke_width, color=color, layer=layer)
    ast.add_circle(c0, scale, stroke_width=stroke_width * 1.4, color=color, layer=layer)

    return ast


def generate_crop_circle(
    glyph_type: str = "milk_hill",
    style: Optional[str] = None,
    radius: Optional[float] = None,
    scale: float = 200.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.0,
    color: str = "#39ff14",
    **kwargs: Any,
) -> GeometryAST:
    """Master factory function for authentic extraterrestrial agro-glyph crop circles."""
    if style is not None:
        glyph_type = style
    if radius is not None:
        scale = radius

    s = glyph_type.lower().strip()
    if s in ("milk_hill", "409_circles", "milkhill", "crop_circle_milk_hill"):
        return generate_milk_hill_glyph(scale=scale, center_x=center_x, center_y=center_y, stroke_width=stroke_width, glyph_color=color, **kwargs)
    elif s in ("julia_set", "stonehenge", "julia", "crop_circle_julia_set"):
        return generate_julia_set_glyph(scale=scale, center_x=center_x, center_y=center_y, stroke_width=stroke_width, color=color, **kwargs)
    elif s in ("barbury_castle", "tetrahedron_glyph", "barbury", "crop_circle_barbury_castle"):
        return generate_barbury_castle_glyph(scale=scale, center_x=center_x, center_y=center_y, stroke_width=stroke_width, color=color, **kwargs)
    elif s in ("chilbolton", "arecibo_reply", "binary_glyph", "crop_circle_chilbolton"):
        return generate_chilbolton_binary_glyph(scale=scale, center_x=center_x, center_y=center_y, stroke_width=stroke_width, color=color, **kwargs)
    elif s in ("triskele", "windmill_hill", "triple_vortex", "crop_circle_triskele"):
        return generate_triskele_glyph(scale=scale, center_x=center_x, center_y=center_y, stroke_width=stroke_width, color=color, **kwargs)
    else:
        return generate_milk_hill_glyph(scale=scale, center_x=center_x, center_y=center_y, stroke_width=stroke_width, glyph_color=color, **kwargs)
