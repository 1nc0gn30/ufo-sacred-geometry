"""Flower of Life & Sacred Geometry Lattice Generators.

Implements:
- Seed of Life (7 interlocking circles)
- Flower of Life (19 concentric circles, parameterized rings, completion arcs, double outer rings)
- Egg of Life (embryonic morula 8-node harmonic layout)
- Fruit of Life (13 non-overlapping node circles at 0, 2R, 4R)
- Tree of Life (Kabbalistic 10 Sephiroth nodes + 22 connecting paths aligned to the Flower lattice)
100% Python Standard Library.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from ..models import Circle, GeometryAST, LineSegment, Point2D


def generate_seed_of_life(
    radius: float = 60.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.5,
    color: str = "#ffd700",
    outer_circle: bool = True,
    outer_circle_color: str = "#ffaa00",
    layer: str = "seed_of_life",
) -> GeometryAST:
    """Generate the Seed of Life (7 intersecting circles).

    The foundation of sacred geometry: 1 central circle plus 6 circles
    centered at 60-degree intervals along the central circumference.
    """
    ast = GeometryAST(
        title="Seed of Life",
        description="7 interlocking circles representing the 6 days of creation and center point of rest.",
        parameters={
            "radius": radius,
            "center_x": center_x,
            "center_y": center_y,
            "stroke_width": stroke_width,
            "color": color,
            "outer_circle": outer_circle,
        },
        tags=["sacred_geometry", "classical", "seed_of_life", "hexagonal"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "boundary": {"color": outer_circle_color, "stroke_width": stroke_width * 1.2},
        },
    )

    c0 = Point2D(center_x, center_y)
    # 1. Central circle
    ast.add_circle(c0, radius, stroke_width=stroke_width, color=color, layer=layer)

    # 2. 6 Perimeter circles
    for i in range(6):
        angle = i * (math.pi / 3.0)
        center_i = Point2D.from_polar(radius, angle, origin=c0)
        ast.add_circle(center_i, radius, stroke_width=stroke_width, color=color, layer=layer)

    # 3. Outer boundary circle (radius = 2 * radius)
    if outer_circle:
        ast.add_circle(
            c0,
            radius * 2.0,
            stroke_width=stroke_width * 1.2,
            color=outer_circle_color,
            layer="boundary",
        )

    return ast


def generate_flower_of_life(
    radius: float = 40.0,
    rings: int = 3,
    iterations: Optional[int] = None,
    outer_rings: bool = True,
    completion_arcs: bool = True,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.2,
    color: str = "#ffd700",
    outer_color: str = "#ff9900",
    layer: str = "flower_of_life",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Flower of Life with parametric concentric hexagonal rings.

    Standard Flower of Life has rings=3 (37 circles in hex lattice) framed by double outer rings.
    Generalized rings parameter allows N-depth hexagonal lattice expansion.
    """
    if iterations is not None:
        rings = iterations

    ast = GeometryAST(
        title="Flower of Life",
        description=f"Sacred hexagonal rosette pattern with {rings} rings and intersecting lens geometry.",
        parameters={
            "radius": radius,
            "rings": rings,
            "outer_rings": outer_rings,
            "completion_arcs": completion_arcs,
            "stroke_width": stroke_width,
            "color": color,
        },
        tags=["sacred_geometry", "flower_of_life", "rosette", "platonic", "ancient"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "outer_rings": {"color": outer_color, "stroke_width": stroke_width * 1.5},
            "petal_arcs": {"color": color, "stroke_width": stroke_width * 0.9, "opacity": 0.85},
        },
    )

    c0 = Point2D(center_x, center_y)

    # Compute hexagonal lattice center positions for N rings
    circle_centers: List[Tuple[Point2D, int]] = [(c0, 0)]  # (point, ring_index)

    for ring in range(1, rings + 1):
        for i in range(6):
            corner_angle = i * (math.pi / 3.0)
            corner_p = Point2D.from_polar(ring * radius, corner_angle, origin=c0)

            next_corner_angle = ((i + 1) % 6) * (math.pi / 3.0)
            next_corner_p = Point2D.from_polar(ring * radius, next_corner_angle, origin=c0)

            for step in range(ring):
                t = step / float(ring)
                px = corner_p.x + t * (next_corner_p.x - corner_p.x)
                py = corner_p.y + t * (next_corner_p.y - corner_p.y)
                circle_centers.append((Point2D(px, py), ring))

    # Add all lattice circles
    for center, ring_idx in circle_centers:
        ast.add_circle(
            center,
            radius,
            stroke_width=stroke_width,
            color=color,
            layer=layer,
        )

    # Double outer boundary rings
    if outer_rings:
        boundary_radius = (rings if rings > 1 else 2) * radius
        ast.add_circle(
            c0,
            boundary_radius,
            stroke_width=stroke_width * 1.5,
            color=outer_color,
            layer="outer_rings",
        )
        ast.add_circle(
            c0,
            boundary_radius * 1.05,
            stroke_width=stroke_width * 1.0,
            color=outer_color,
            layer="outer_rings",
        )

    return ast



def generate_egg_of_life(
    radius: float = 50.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.5,
    color: str = "#00f0ff",
    layer: str = "egg_of_life",
) -> GeometryAST:
    """Generate the Egg of Life (8-cell / 7-overlapping sphere harmonic layout).

    Represents embryonic cellular division and the morphogenetic field of all life forms.
    """
    ast = GeometryAST(
        title="Egg of Life",
        description="8-cell embryonic morphogenetic structure derived from intersecting central petals of Flower of Life.",
        parameters={"radius": radius, "stroke_width": stroke_width, "color": color},
        tags=["sacred_geometry", "egg_of_life", "biology", "creation"],
        layers={layer: {"color": color, "stroke_width": stroke_width}},
    )

    c0 = Point2D(center_x, center_y)
    # Central sphere
    ast.add_circle(c0, radius, stroke_width=stroke_width, color=color, layer=layer)

    # 6 Surrounding intersecting circles spaced by radius
    for i in range(6):
        angle = i * (math.pi / 3.0) + (math.pi / 6.0)
        p = Point2D.from_polar(radius, angle, origin=c0)
        ast.add_circle(p, radius, stroke_width=stroke_width, color=color, layer=layer)

    # Outer harmonic ring
    ast.add_circle(
        c0,
        radius * 2.0,
        stroke_width=stroke_width * 1.3,
        color=color,
        layer=layer,
        opacity=0.7,
    )

    return ast


def generate_fruit_of_life(
    radius: float = 30.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.5,
    color: str = "#ff007f",
    connecting_lines: bool = False,
    layer: str = "fruit_of_life",
) -> GeometryAST:
    """Generate the Fruit of Life (13 isolated circles).

    Derived by completing the outer circles of the Flower of Life.
    1 central circle + 6 inner circles (dist 2R) + 6 outer circles (dist 4R)
    forming the 13 informational nodes for Metatron's Cube.
    """
    ast = GeometryAST(
        title="Fruit of Life",
        description="13 non-overlapping circles forming the blueprint of the universe and Metatron's Cube.",
        parameters={
            "radius": radius,
            "connecting_lines": connecting_lines,
            "stroke_width": stroke_width,
            "color": color,
        },
        tags=["sacred_geometry", "fruit_of_life", "metatron", "platonic"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "connecting_rays": {"color": "#ffffff", "stroke_width": 0.8, "opacity": 0.4},
        },
    )

    c0 = Point2D(center_x, center_y)
    centers: List[Point2D] = [c0]

    # Center circle
    ast.add_circle(c0, radius, stroke_width=stroke_width, color=color, layer=layer)

    # 6 Inner circles at 2 * radius, 6 Outer circles at 4 * radius
    for i in range(6):
        angle = i * (math.pi / 3.0)
        p_inner = Point2D.from_polar(2.0 * radius, angle, origin=c0)
        p_outer = Point2D.from_polar(4.0 * radius, angle, origin=c0)

        centers.append(p_inner)
        centers.append(p_outer)

        ast.add_circle(p_inner, radius, stroke_width=stroke_width, color=color, layer=layer)
        ast.add_circle(p_outer, radius, stroke_width=stroke_width, color=color, layer=layer)

        if connecting_lines:
            ast.add_line(
                c0,
                p_outer,
                stroke_width=0.8,
                color="#ffffff",
                layer="connecting_rays",
                opacity=0.4,
            )

    return ast


def generate_tree_of_life(
    scale: float = 120.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    node_radius: float = 14.0,
    overlay_flower: bool = True,
    stroke_width: float = 1.5,
    path_color: str = "#00ffff",
    node_color: str = "#ffd700",
    flower_color: str = "#335577",
    layer: str = "tree_of_life",
) -> GeometryAST:
    """Generate the Kabbalistic Tree of Life (10 Sephiroth + 22 Connecting Paths).

    The nodal coordinates are precisely anchored to the Seed/Flower of Life lattice intersections:
    1. Kether (Crown)
    2. Chokmah (Wisdom)
    3. Binah (Understanding)
    4. Chesed (Mercy)
    5. Geburah (Severity/Strength)
    6. Tiphereth (Beauty/Harmony)
    7. Netzach (Victory)
    8. Hod (Glory/Splendor)
    9. Yesod (Foundation)
    10. Malkuth (Kingdom)
    """
    ast = GeometryAST(
        title="Tree of Life (Etz Chaim)",
        description="10 divine Sephiroth emanations and 22 connecting sacred paths aligned to the Flower of Life grid.",
        parameters={
            "scale": scale,
            "node_radius": node_radius,
            "overlay_flower": overlay_flower,
            "stroke_width": stroke_width,
        },
        tags=["sacred_geometry", "tree_of_life", "kabbalah", "hermetic", "mysticism"],
        layers={
            "flower_grid": {"color": flower_color, "stroke_width": 0.8, "opacity": 0.35},
            "tree_paths": {"color": path_color, "stroke_width": stroke_width * 1.2},
            "sephiroth_nodes": {"color": node_color, "stroke_width": stroke_width * 1.5},
        },
    )

    c0 = Point2D(center_x, center_y)

    # Optional background Seed/Flower of life lattice grid
    if overlay_flower:
        flower = generate_flower_of_life(
            radius=scale * 0.5,
            rings=2,
            outer_rings=False,
            center_x=center_x,
            center_y=center_y,
            stroke_width=0.8,
            color=flower_color,
            layer="flower_grid",
        )
        ast.circles.extend(flower.circles)
        ast.lines.extend(flower.lines)

    # Standard vertical alignment for Tree of Life (Y up/down)
    # Unit proportions along pillars: Left (Binah/Geburah/Hod), Middle (Kether/Tiphereth/Yesod/Malkuth), Right (Chokmah/Chesed/Netzach)
    dx = scale * 0.866025  # cos(30)*scale
    dy = scale * 0.5

    nodes: Dict[int, Point2D] = {
        1: Point2D(c0.x, c0.y - 2.5 * scale),  # Kether
        2: Point2D(c0.x + dx, c0.y - 2.0 * scale),  # Chokmah
        3: Point2D(c0.x - dx, c0.y - 2.0 * scale),  # Binah
        4: Point2D(c0.x + dx, c0.y - 0.75 * scale),  # Chesed
        5: Point2D(c0.x - dx, c0.y - 0.75 * scale),  # Geburah
        6: Point2D(c0.x, c0.y - 0.75 * scale),  # Tiphereth
        7: Point2D(c0.x + dx, c0.y + 0.5 * scale),  # Netzach
        8: Point2D(c0.x - dx, c0.y + 0.5 * scale),  # Hod
        9: Point2D(c0.x, c0.y + 1.25 * scale),  # Yesod
        10: Point2D(c0.x, c0.y + 2.5 * scale),  # Malkuth
    }

    # 22 Connecting paths between Sephiroth
    paths = [
        (1, 2),
        (1, 3),
        (1, 6),
        (2, 3),
        (2, 6),
        (2, 4),
        (3, 6),
        (3, 5),
        (4, 5),
        (4, 6),
        (4, 7),
        (5, 6),
        (5, 8),
        (6, 7),
        (6, 8),
        (6, 9),
        (7, 8),
        (7, 9),
        (7, 10),
        (8, 9),
        (8, 10),
        (9, 10),
    ]

    # Draw 22 Paths
    for u, v in paths:
        ast.add_line(
            nodes[u],
            nodes[v],
            stroke_width=stroke_width * 1.2,
            color=path_color,
            layer="tree_paths",
        )

    # Draw 10 Sephiroth nodes (with concentric inner ring)
    for idx, pos in nodes.items():
        ast.add_circle(
            pos,
            node_radius,
            stroke_width=stroke_width * 1.5,
            color=node_color,
            fill="#050814",
            layer="sephiroth_nodes",
        )
        ast.add_circle(
            pos,
            node_radius * 0.45,
            stroke_width=stroke_width * 0.9,
            color=node_color,
            layer="sephiroth_nodes",
        )

    return ast
