"""Golden Ratio, Fibonacci Spiral, Whirling Squares & Sunflower Phyllotaxis Generators.

Implements:
- Golden Ratio (Phi = 1.6180339887...) logarithmic spiral
- Fibonacci Whirling Squares and nested Golden Rectangles
- Quarter-circle continuous spiral arcs
- Sunflower Phyllotaxis disc pattern (Vogel's formula with Golden Angle 137.507764°)
- Fibonacci parastichy spiral families (connecting neighboring seeds)
- Golden Triangle Logarithmic Spiral (Kepler / Isosceles Golden Triangles)
100% Python Standard Library.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Polygon, Spline

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0  # ~1.618033988749895
GOLDEN_ANGLE_DEG: float = 137.50776405003785  # 360 * (1 - 1/phi)
GOLDEN_ANGLE_RAD: float = GOLDEN_ANGLE_DEG * (math.pi / 180.0)


def generate_fibonacci_sequence(n: int = 8, count: Optional[int] = None) -> List[int]:
    """Generate first n numbers of the Fibonacci sequence [1, 1, 2, 3, 5, 8, ...]."""
    if count is not None:
        n = count
    if n <= 0:
        return []
    if n == 1:
        return [1]
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def generate_golden_rectangles(
    iterations: int = 8,
    count: Optional[int] = None,
    initial_size: float = 12.0,
    base_size: Optional[float] = None,
    center_x: float = 0.0,
    center_y: float = 0.0,
    show_arcs: bool = True,
    show_rectangles: bool = True,
    show_diagonals: bool = True,
    stroke_width: float = 1.2,
    rect_color: str = "#39ff14",
    spiral_color: str = "#ffd700",
    diagonal_color: str = "#555577",
    layer: str = "golden_rectangles",
    **kwargs: Any,
) -> GeometryAST:
    """Generate classic Fibonacci Whirling Squares and Golden Spiral Arcs."""
    if count is not None:
        iterations = count
    if base_size is not None:
        initial_size = base_size

    ast = GeometryAST(
        title="Fibonacci Whirling Squares & Golden Spiral",
        description=f"Logarithmic growth spiral constructed from {iterations} nested Fibonacci squares and quarter-arcs.",
        parameters={
            "iterations": iterations,
            "count": iterations,
            "initial_size": initial_size,
            "base_size": initial_size,
            "show_arcs": show_arcs,
            "show_rectangles": show_rectangles,
            "show_diagonals": show_diagonals,
            "stroke_width": stroke_width,
        },
        tags=["sacred_geometry", "fibonacci", "golden_ratio", "spiral", "whirling_squares"],
        layers={
            layer: {"color": rect_color, "stroke_width": stroke_width},
            "spiral_arc": {"color": spiral_color, "stroke_width": stroke_width * 1.8},
            "diagonals": {"color": diagonal_color, "stroke_width": stroke_width * 0.8, "opacity": 0.4},
        },
    )

    fibs = generate_fibonacci_sequence(iterations)

    min_x = 0.0
    min_y = 0.0
    max_x = initial_size * fibs[0]
    max_y = initial_size * fibs[0]

    squares: List[Tuple[Point2D, Point2D, Point2D, Point2D, Point2D, float, float, float]] = []

    s0 = initial_size * fibs[0]
    p_tl = Point2D(0.0, 0.0)
    p_tr = Point2D(s0, 0.0)
    p_br = Point2D(s0, s0)
    p_bl = Point2D(0.0, s0)
    squares.append((p_tl, p_tr, p_br, p_bl, Point2D(s0, s0), s0, math.pi, 1.5 * math.pi))

    for i in range(1, iterations):
        side = initial_size * fibs[i]
        dir_idx = i % 4

        if dir_idx == 1:
            new_min_y = min_y - side
            tl = Point2D(min_x, new_min_y)
            tr = Point2D(max_x, new_min_y)
            br = Point2D(max_x, min_y)
            bl = Point2D(min_x, min_y)
            arc_c = Point2D(min_x, min_y)
            arc_r = side
            start_a = 1.5 * math.pi
            end_a = 2.0 * math.pi
            min_y = new_min_y

        elif dir_idx == 2:
            new_min_x = min_x - side
            tl = Point2D(new_min_x, min_y)
            tr = Point2D(min_x, min_y)
            br = Point2D(min_x, max_y)
            bl = Point2D(new_min_x, max_y)
            arc_c = Point2D(min_x, max_y)
            arc_r = side
            start_a = 0.0
            end_a = 0.5 * math.pi
            min_x = new_min_x

        elif dir_idx == 3:
            new_max_y = max_y + side
            tl = Point2D(min_x, max_y)
            tr = Point2D(max_x, max_y)
            br = Point2D(max_x, new_max_y)
            bl = Point2D(min_x, new_max_y)
            arc_c = Point2D(max_x, max_y)
            arc_r = side
            start_a = 0.5 * math.pi
            end_a = math.pi
            max_y = new_max_y

        else:
            new_max_x = max_x + side
            tl = Point2D(max_x, min_y)
            tr = Point2D(new_max_x, min_y)
            br = Point2D(new_max_x, max_y)
            bl = Point2D(max_x, max_y)
            arc_c = Point2D(max_x, min_y)
            arc_r = side
            start_a = math.pi
            end_a = 1.5 * math.pi
            max_x = new_max_x

        squares.append((tl, tr, br, bl, arc_c, arc_r, start_a, end_a))

    for tl, tr, br, bl, arc_c, arc_r, start_a, end_a in squares:
        if show_rectangles:
            ast.add_polygon(
                [tl, tr, br, bl],
                stroke_width=stroke_width,
                color=rect_color,
                layer=layer,
            )
        if show_arcs:
            ast.add_arc(
                arc_c,
                arc_r,
                start_a,
                end_a,
                stroke_width=stroke_width * 1.8,
                color=spiral_color,
                layer="spiral_arc",
            )

    if show_diagonals:
        ast.add_line(
            Point2D(min_x, min_y),
            Point2D(max_x, max_y),
            stroke_width=stroke_width * 0.8,
            color=diagonal_color,
            layer="diagonals",
            opacity=0.4,
        )
        ast.add_line(
            Point2D(min_x, max_y),
            Point2D(max_x, min_y),
            stroke_width=stroke_width * 0.8,
            color=diagonal_color,
            layer="diagonals",
            opacity=0.4,
        )

    ast.center_at(center_x, center_y)
    return ast


def generate_golden_spiral(
    radius: Optional[float] = None,
    turns: Optional[float] = None,
    iterations: float = 6.0,
    growth_factor: float = 0.3063489,  # ln(phi) / (pi/2)
    scale: float = 8.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    num_arms: int = 1,
    num_samples: int = 600,
    stroke_width: float = 1.5,
    color: str = "#ffd700",
    layer: str = "golden_spiral",
    **kwargs: Any,
) -> GeometryAST:
    """Generate true continuous Logarithmic Golden Spiral r(theta) = scale * exp(b * theta).

    growth_factor b = ln(phi) / (pi/2) ~ 0.3063489 for exact Golden Ratio expansion per 90 degrees.
    Supports multi-arm spirals (e.g. galaxy arms, dual vortex).
    """
    if turns is not None:
        iterations = float(turns)
    if "turns" in kwargs:
        iterations = float(kwargs["turns"])
    if radius is not None:
        scale = max(2.0, radius * 0.05)

    ast = GeometryAST(
        title="Logarithmic Golden Spiral",
        description=f"Continuous equiangular golden spiral with {num_arms} arms expanding at rate phi per quadrant.",
        parameters={
            "iterations": iterations,
            "turns": iterations,
            "radius": radius or (scale * 20.0),
            "growth_factor": growth_factor,
            "scale": scale,
            "num_arms": num_arms,
            "num_samples": num_samples,
            "stroke_width": stroke_width,
            "color": color,
        },
        tags=["sacred_geometry", "golden_spiral", "logarithmic", "vortex", "equiangular"],
        layers={layer: {"color": color, "stroke_width": stroke_width}},
    )

    max_theta = iterations * 2.0 * math.pi
    c0 = Point2D(center_x, center_y)

    for arm in range(num_arms):
        arm_offset = arm * (2.0 * math.pi / num_arms)
        pts: List[Point2D] = []

        for i in range(num_samples + 1):
            t = (i / float(num_samples)) * max_theta
            r = scale * math.exp(growth_factor * t)
            theta = t + arm_offset
            pts.append(Point2D(c0.x + r * math.cos(theta), c0.y + r * math.sin(theta)))

        for i in range(len(pts) - 1):
            ast.add_line(
                pts[i],
                pts[i + 1],
                stroke_width=stroke_width,
                color=color,
                layer=layer,
            )

        # Also add as a Spline / Polyline
        if len(pts) > 2:
            sampled_spline = pts[::max(1, len(pts) // 40)]
            ast.add_spline(sampled_spline, stroke_width=stroke_width, color=color, layer=layer)

    return ast


def generate_phyllotaxis(
    count: Optional[int] = None,
    num_points: int = 350,
    scaling: Optional[float] = None,
    spread: float = 4.5,
    divergence_angle_deg: Optional[float] = None,
    divergence_angle: Optional[float] = None,
    marker_radius: Optional[float] = None,
    dot_radius: Optional[float] = None,
    point_radius: float = 2.8,
    connect_spirals: bool = True,
    parastichy_p: int = 21,
    parastichy_q: int = 34,
    center_x: float = 0.0,
    center_y: float = 0.0,
    seed_color: str = "#ffd700",
    color: Optional[str] = None,
    spiral_color_1: str = "#00f0ff",
    spiral_color_2: str = "#ff007f",
    stroke_width: float = 1.0,
    layer: str = "sunflower_phyllotaxis",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the sunflower phyllotaxis disc pattern using Vogel's mathematical model."""
    if count is not None:
        num_points = count
    if scaling is not None:
        spread = scaling
    if dot_radius is not None:
        point_radius = dot_radius
    if marker_radius is not None:
        point_radius = marker_radius
    if color is not None:
        seed_color = color

    eff_div_angle_deg = divergence_angle_deg if divergence_angle_deg is not None else (divergence_angle if divergence_angle is not None else GOLDEN_ANGLE_DEG)
    eff_div_rad = math.radians(eff_div_angle_deg)

    ast = GeometryAST(
        title="Sunflower Phyllotaxis Disc",
        description=f"Vogel's golden angle phyllotaxis with {num_points} seeds and ({parastichy_p}, {parastichy_q}) parastichy spirals.",
        parameters={
            "num_points": num_points,
            "count": num_points,
            "spread": spread,
            "scaling": spread,
            "point_radius": point_radius,
            "dot_radius": point_radius,
            "divergence_angle_deg": eff_div_angle_deg,
            "connect_spirals": connect_spirals,
            "parastichy_p": parastichy_p,
            "parastichy_q": parastichy_q,
        },
        tags=["sacred_geometry", "phyllotaxis", "vogel", "sunflower", "golden_angle", "nature"],
        layers={
            layer: {"color": seed_color, "stroke_width": stroke_width},
            "spiral_family_p": {"color": spiral_color_1, "stroke_width": 0.9, "opacity": 0.6},
            "spiral_family_q": {"color": spiral_color_2, "stroke_width": 0.9, "opacity": 0.6},
        },
    )

    c0 = Point2D(center_x, center_y)
    seeds: List[Point2D] = []

    for n in range(num_points):
        theta = n * eff_div_rad
        r = spread * math.sqrt(n)
        seeds.append(Point2D.from_polar(r, theta, origin=c0))

    if connect_spirals and num_points > parastichy_q:
        for n in range(num_points - parastichy_p):
            ast.add_line(
                seeds[n],
                seeds[n + parastichy_p],
                stroke_width=0.8,
                color=spiral_color_1,
                layer="spiral_family_p",
                opacity=0.6,
            )

        for n in range(num_points - parastichy_q):
            ast.add_line(
                seeds[n],
                seeds[n + parastichy_q],
                stroke_width=0.8,
                color=spiral_color_2,
                layer="spiral_family_q",
                opacity=0.6,
            )

    for i, pt in enumerate(seeds):
        r_node = max(1.2, point_radius * (0.6 + 0.4 * math.sqrt(i / float(max(1, num_points)))))
        ast.add_circle(
            pt,
            r_node,
            stroke_width=stroke_width * 0.8,
            color=seed_color,
            fill="#ffd700",
            layer=layer,
        )

    return ast


def generate_golden_triangle_spiral(
    iterations: int = 9,
    depth: Optional[int] = None,
    initial_size: float = 240.0,
    base_length: Optional[float] = None,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.2,
    triangle_color: str = "#00f0ff",
    spiral_color: str = "#ffd700",
    layer: str = "golden_triangle",
    **kwargs: Any,
) -> GeometryAST:
    """Generate recursive Golden Triangles (isosceles 72-72-36 triangles) and nested spiral."""
    if depth is not None:
        iterations = depth
    if base_length is not None:
        initial_size = base_length

    ast = GeometryAST(
        title="Golden Triangle Spiral (Sublime Triangle)",
        description=f"Recursive self-similar Golden Triangle subdivision of order {iterations}.",
        parameters={
            "iterations": iterations,
            "depth": iterations,
            "initial_size": initial_size,
            "base_length": initial_size,
            "stroke_width": stroke_width,
        },
        tags=["sacred_geometry", "golden_triangle", "sublime_triangle", "pentagram", "fractal"],
        layers={
            layer: {"color": triangle_color, "stroke_width": stroke_width},
            "spiral": {"color": spiral_color, "stroke_width": stroke_width * 1.8},
        },
    )

    side = initial_size
    base = side / PHI
    height = math.sqrt(side * side - (base / 2.0) ** 2)

    A = Point2D(center_x, center_y - height * 0.6)
    B = Point2D(center_x - base / 2.0, center_y + height * 0.4)
    C = Point2D(center_x + base / 2.0, center_y + height * 0.4)

    cur_A, cur_B, cur_C = A, B, C
    spiral_pts: List[Point2D] = [cur_B]

    for _ in range(iterations):
        ast.add_polygon(
            [cur_A, cur_B, cur_C],
            stroke_width=stroke_width,
            color=triangle_color,
            layer=layer,
        )
        Dx = cur_A.x + (cur_C.x - cur_A.x) / PHI
        Dy = cur_A.y + (cur_C.y - cur_A.y) / PHI
        D = Point2D(Dx, Dy)

        ast.add_line(cur_B, D, stroke_width=stroke_width, color=triangle_color, layer=layer)
        spiral_pts.append(D)

        cur_A, cur_B, cur_C = cur_C, D, cur_B

    if len(spiral_pts) >= 3:
        ast.add_spline(
            spiral_pts,
            stroke_width=stroke_width * 1.8,
            color=spiral_color,
            layer="spiral",
        )

    return ast

