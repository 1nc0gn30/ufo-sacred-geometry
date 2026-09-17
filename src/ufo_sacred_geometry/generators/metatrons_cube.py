"""Metatron's Cube & Platonic Solids Geometric Synthesizer.

Implements:
- Metatron's Cube (13 Fruit of Life nodal centers + all 78 sacred connecting lines)
- 5 Platonic Solids 2D orthographic/isometric wireframe projections:
  1. Tetrahedron (Fire / 4 vertices) & Star Tetrahedron / Merkaba
  2. Hexahedron / Cube (Earth / 8 vertices)
  3. Octahedron (Air / 6 vertices)
  4. Icosahedron (Water / 12 vertices)
  5. Dodecahedron (Ether / 20 vertices)
100% Python Standard Library.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from ..models import Circle, GeometryAST, LineSegment, Point2D, Point3D

PHI = (1.0 + math.sqrt(5.0)) / 2.0  # Golden Ratio (~1.6180339887)


def get_metatrons_13_centers(
    radius: float = 40.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
) -> List[Point2D]:
    """Calculate the 13 canonical nodal center coordinates of Metatron's Cube.

    Index 0: Origin Center (0, 0)
    Indices 1..6: Inner Hexagon Centers at distance 2 * radius
    Indices 7..12: Outer Hexagon Centers at distance 4 * radius
    """
    c0 = Point2D(center_x, center_y)
    centers: List[Point2D] = [c0]

    # 6 Inner centers
    for i in range(6):
        angle = i * (math.pi / 3.0)
        centers.append(Point2D.from_polar(2.0 * radius, angle, origin=c0))

    # 6 Outer centers
    for i in range(6):
        angle = i * (math.pi / 3.0)
        centers.append(Point2D.from_polar(4.0 * radius, angle, origin=c0))

    return centers


def generate_metatrons_cube(
    radius: float = 35.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    include_circles: bool = True,
    include_lines: bool = True,
    include_outer_bounds: bool = True,
    circle_style: str = "fruit_of_life",  # "fruit_of_life" or "nodes_only"
    stroke_width: float = 1.0,
    line_color: str = "#00ffff",
    circle_color: str = "#ffd700",
    outer_boundary: Optional[bool] = None,
    highlight_cube: bool = False,
    layer: str = "metatrons_cube",
    **kwargs: Any,
) -> GeometryAST:
    """Generate Metatron's Cube with all 78 connecting line segments and 13 nodal circles.

    Total lines = 13 * 12 / 2 = 78 unique segments.
    """
    has_outer = include_outer_bounds if outer_boundary is None else outer_boundary

    ast = GeometryAST(
        title="Metatron's Cube",
        description="The 13 information systems of the Fruit of Life connected by 78 lines encoding the 5 Platonic Solids.",
        parameters={
            "radius": radius,
            "center_x": center_x,
            "center_y": center_y,
            "include_circles": include_circles,
            "include_lines": include_lines,
            "circle_style": circle_style,
            "stroke_width": stroke_width,
            "line_color": line_color,
            "circle_color": circle_color,
            "highlight_cube": highlight_cube,
        },
        tags=["sacred_geometry", "metatron", "archangel", "platonic_solids", "creation"],
        layers={
            layer: {"color": line_color, "stroke_width": stroke_width},
            "fruit_circles": {"color": circle_color, "stroke_width": stroke_width * 1.2},
            "cube_highlight": {"color": "#ff007f", "stroke_width": stroke_width * 1.6},
            "outer_rings": {"color": circle_color, "stroke_width": stroke_width * 1.5},
        },
    )

    centers = get_metatrons_13_centers(radius, center_x, center_y)
    c0 = centers[0]

    # 1. Add all 78 Connecting Lines (Combinations of 13 taken 2 at a time)
    if include_lines:
        line_count = 0
        for i in range(len(centers)):
            for j in range(i + 1, len(centers)):
                p1, p2 = centers[i], centers[j]
                ast.add_line(
                    p1,
                    p2,
                    stroke_width=stroke_width,
                    color=line_color,
                    layer=layer,
                    opacity=0.75,
                )
                line_count += 1

    # 2. Add 13 Circles
    if include_circles:
        node_r = radius if circle_style == "fruit_of_life" else radius * 0.25
        for i, pt in enumerate(centers):
            ast.add_circle(
                pt,
                node_r,
                stroke_width=stroke_width * 1.2,
                color=circle_color,
                layer="fruit_circles",
                opacity=0.9,
            )

    # 3. Highlight the isometric Cube / Hexahedron edges inside Metatron's Cube
    if highlight_cube:
        outer_indices = [7, 8, 9, 10, 11, 12]
        for k in range(6):
            p_a = centers[outer_indices[k]]
            p_b = centers[outer_indices[(k + 1) % 6]]
            ast.add_line(
                p_a,
                p_b,
                stroke_width=stroke_width * 1.8,
                color="#ff00ff",
                layer="cube_highlight",
            )

        for k in [7, 9, 11]:
            ast.add_line(
                c0,
                centers[k],
                stroke_width=stroke_width * 1.8,
                color="#ff00ff",
                layer="cube_highlight",
            )

    # 4. Outer framing boundary ring
    if has_outer:
        max_dist = 4.0 * radius + (radius if circle_style == "fruit_of_life" else radius * 0.5)
        ast.add_circle(
            c0,
            max_dist,
            stroke_width=stroke_width * 1.4,
            color=circle_color,
            layer="outer_rings",
        )

    return ast



def _get_platonic_3d_geometry(
    solid_type: str,
    size: float = 100.0,
) -> Tuple[List[Point3D], List[Tuple[int, int]]]:
    """Generate canonical 3D vertices and edge tuples for the 5 Platonic Solids."""
    st = solid_type.lower().strip()
    s = size / 2.0

    if st in ("tetrahedron", "fire"):
        # 4 vertices: (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)
        k = s / math.sqrt(3.0)
        vertices = [
            Point3D(k, k, k),
            Point3D(k, -k, -k),
            Point3D(-k, k, -k),
            Point3D(-k, -k, k),
        ]
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    elif st in ("cube", "hexahedron", "earth"):
        # 8 vertices: (±s, ±s, ±s)
        vertices = []
        for x in [-s, s]:
            for y in [-s, s]:
                for z in [-s, s]:
                    vertices.append(Point3D(x, y, z))
        # 12 edges
        edges = [
            (0, 1),
            (1, 3),
            (3, 2),
            (2, 0),  # bottom square
            (4, 5),
            (5, 7),
            (7, 6),
            (6, 4),  # top square
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),  # vertical pillars
        ]

    elif st in ("octahedron", "air"):
        # 6 vertices: (±s, 0, 0), (0, ±s, 0), (0, 0, ±s)
        vertices = [
            Point3D(s, 0, 0),
            Point3D(-s, 0, 0),
            Point3D(0, s, 0),
            Point3D(0, -s, 0),
            Point3D(0, 0, s),
            Point3D(0, 0, -s),
        ]
        # 12 edges
        edges = [
            (0, 2),
            (2, 1),
            (1, 3),
            (3, 0),  # XY equator
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),  # top pyramid
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),  # bottom pyramid
        ]

    elif st in ("icosahedron", "water"):
        # 12 vertices: Golden ratio rectangles (0, ±1, ±PHI), (±1, ±PHI, 0), (±PHI, 0, ±1)
        scale_fac = s / math.sqrt(1.0 + PHI * PHI)
        vertices = []
        # (0, ±1, ±phi)
        for y in [-1.0, 1.0]:
            for z in [-PHI, PHI]:
                vertices.append(Point3D(0.0, y * scale_fac, z * scale_fac))
        # (±1, ±phi, 0)
        for x in [-1.0, 1.0]:
            for y in [-PHI, PHI]:
                vertices.append(Point3D(x * scale_fac, y * scale_fac, 0.0))
        # (±phi, 0, ±1)
        for x in [-PHI, PHI]:
            for z in [-1.0, 1.0]:
                vertices.append(Point3D(x * scale_fac, 0.0, z * scale_fac))

        # Connect all pairs with distance ~ 2 * scale_fac (30 edges)
        edges = []
        target_dist = 2.0 * scale_fac
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                d = vertices[i].distance_to(vertices[j])
                if abs(d - target_dist) < 0.1 * scale_fac:
                    edges.append((i, j))

    elif st in ("dodecahedron", "ether", "aether", "universe"):
        # 20 vertices: (±1, ±1, ±1), (0, ±1/phi, ±phi), (±1/phi, ±phi, 0), (±phi, 0, ±1/phi)
        inv_phi = 1.0 / PHI
        scale_fac = s / math.sqrt(3.0)
        vertices = []
        # 8 cube vertices (±1, ±1, ±1)
        for x in [-1.0, 1.0]:
            for y in [-1.0, 1.0]:
                for z in [-1.0, 1.0]:
                    vertices.append(Point3D(x * scale_fac, y * scale_fac, z * scale_fac))
        # (0, ±1/phi, ±phi)
        for y in [-inv_phi, inv_phi]:
            for z in [-PHI, PHI]:
                vertices.append(Point3D(0.0, y * scale_fac, z * scale_fac))
        # (±1/phi, ±phi, 0)
        for x in [-inv_phi, inv_phi]:
            for y in [-PHI, PHI]:
                vertices.append(Point3D(x * scale_fac, y * scale_fac, 0.0))
        # (±phi, 0, ±1/phi)
        for x in [-PHI, PHI]:
            for z in [-inv_phi, inv_phi]:
                vertices.append(Point3D(x * scale_fac, 0.0, z * scale_fac))

        # Connect pairs with nearest edge distance (30 edges)
        edges = []
        target_dist = 2.0 * inv_phi * scale_fac
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                d = vertices[i].distance_to(vertices[j])
                if abs(d - target_dist) < 0.15 * scale_fac:
                    edges.append((i, j))

    else:
        raise ValueError(
            f"Unknown Platonic Solid: {solid_type}. Choose from 'tetrahedron', 'cube', 'octahedron', 'icosahedron', 'dodecahedron'."
        )

    return vertices, edges


def generate_platonic_solid_projection(
    solid_type: str = "cube",
    solid_name: Optional[str] = None,
    size: float = 120.0,
    radius: Optional[float] = None,
    rot_x: float = 0.55,
    rot_y: float = 0.75,
    rot_z: float = 0.0,
    perspective: bool = False,
    stroke_width: float = 1.5,
    color: str = "#00f0ff",
    show_nodes: bool = True,
    node_radius: float = 4.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    layer: str = "platonic_solid",
    **kwargs: Any,
) -> GeometryAST:
    """Generate a 2D projection of any of the 5 Platonic Solids with 3D Euler rotations."""
    if solid_name is not None:
        solid_type = solid_name
    if radius is not None:
        size = radius * 2.0

    vertices_3d, edges = _get_platonic_3d_geometry(solid_type, size)

    title_name = solid_type.capitalize()
    ast = GeometryAST(
        title=f"Platonic Solid: {title_name}",
        description=f"3D projection of the sacred {title_name} polyhedral wireframe geometry.",
        parameters={
            "solid_type": solid_type,
            "solid_name": solid_type,
            "size": size,
            "rot_x": rot_x,
            "rot_y": rot_y,
            "rot_z": rot_z,
            "perspective": perspective,
            "stroke_width": stroke_width,
            "color": color,
        },
        tags=["sacred_geometry", "platonic_solid", solid_type.lower(), "3d_projection", "polyhedra"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "solid_nodes": {"color": "#ffd700", "stroke_width": stroke_width},
        },
    )


    # Store 3D vertices in AST
    ast.points3d = vertices_3d

    # Rotate in 3D and project to 2D
    pts_2d: List[Point2D] = []
    for p3 in vertices_3d:
        p_rot = p3.rotate_euler(rot_x, rot_y, rot_z)
        if perspective:
            proj = p_rot.project_2d(focal_length=400.0, camera_z=500.0)
        else:
            proj = p_rot.project_2d(orthographic=True)
        pts_2d.append(proj.translate(center_x, center_y))

    # Add all edges
    for u, v in edges:
        ast.add_line(
            pts_2d[u],
            pts_2d[v],
            stroke_width=stroke_width,
            color=color,
            layer=layer,
        )

    # Add vertex nodes
    if show_nodes:
        for pt in pts_2d:
            ast.add_circle(
                pt,
                node_radius,
                stroke_width=stroke_width,
                color="#ffd700",
                fill="#050814",
                layer="solid_nodes",
            )

    return ast
