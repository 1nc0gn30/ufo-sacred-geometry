"""Merkaba (Star Tetrahedron), Torus Field, Torus Knot & Vesica Piscis Synthesizer.

Implements:
1. Merkaba (Stella Octangula / Star Tetrahedron lightbody vehicle in 3D projection)
2. Torus Energy Field (Vortex math 3-6-9 toroidal flow lattice)
3. Parametric (p, q) Torus Knots (Trefoil, Pentagrammatic & Solfeggio harmonic windings)
4. Sacred Vesica Piscis & Mandorla (Portal of creation, sqrt(2), sqrt(3), sqrt(5) proportions)
100% Python Standard Library.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Point3D, Polygon, Spline


def generate_merkaba(
    size: Optional[float] = None,
    radius: float = 120.0,
    rot_x: float = 0.45,
    rot_y: float = 0.65,
    rot_z: float = 0.0,
    perspective: bool = False,
    wireframe_axes: bool = True,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.4,
    male_tetra_color: str = "#00f0ff",
    female_tetra_color: str = "#ff007f",
    sphere_color: str = "#ffd700",
    show_spheres: bool = True,
    show_core_octahedron: bool = True,
    layer: str = "merkaba_star",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Merkaba (Star Tetrahedron / Stella Octangula) 3D light-body projection."""
    if size is not None:
        radius = size

    ast = GeometryAST(
        title="Merkaba Star Tetrahedron",
        description="The 8-pointed Stella Octangula light-spirit-body dimensional vehicle consisting of counter-rotating interpenetrating tetrahedra.",
        parameters={
            "radius": radius,
            "size": radius,
            "rot_x": rot_x,
            "rot_y": rot_y,
            "rot_z": rot_z,
            "perspective": perspective,
            "stroke_width": stroke_width,
            "show_spheres": show_spheres,
            "wireframe_axes": wireframe_axes,
        },
        tags=["sacred_geometry", "merkaba", "star_tetrahedron", "stella_octangula", "lightbody", "3d"],
        layers={
            "male_tetra": {"color": male_tetra_color, "stroke_width": stroke_width * 1.3},
            "female_tetra": {"color": female_tetra_color, "stroke_width": stroke_width * 1.3},
            "core_octa": {"color": "#ffd700", "stroke_width": stroke_width * 0.9, "opacity": 0.6},
            "energy_sphere": {"color": sphere_color, "stroke_width": stroke_width * 1.1},
            "axes": {"color": "#ffffff", "stroke_width": 0.8, "opacity": 0.5},
        },
    )

    s = radius / math.sqrt(3.0)

    # Ascending Tetrahedron (4 vertices)
    t1_verts = [
        Point3D(s, s, s),
        Point3D(s, -s, -s),
        Point3D(-s, s, -s),
        Point3D(-s, -s, s),
    ]
    t1_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    # Descending Tetrahedron (4 vertices)
    t2_verts = [
        Point3D(-s, -s, -s),
        Point3D(-s, s, s),
        Point3D(s, -s, s),
        Point3D(s, s, -s),
    ]
    t2_edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

    def project_pt(p3: Point3D) -> Point2D:
        pr = p3.rotate_euler(rot_x, rot_y, rot_z)
        if perspective:
            p2 = pr.project_2d(focal_length=450.0, camera_z=550.0)
        else:
            p2 = pr.project_2d(orthographic=True)
        return p2.translate(center_x, center_y)

    t1_pts_2d = [project_pt(p) for p in t1_verts]
    t2_pts_2d = [project_pt(p) for p in t2_verts]

    ast.points3d.extend(t1_verts)
    ast.points3d.extend(t2_verts)

    # Add 2 projected triangle polygons
    ast.add_polygon([t1_pts_2d[0], t1_pts_2d[1], t1_pts_2d[2]], stroke_width=stroke_width, color=male_tetra_color, layer="male_tetra")
    ast.add_polygon([t2_pts_2d[0], t2_pts_2d[1], t2_pts_2d[2]], stroke_width=stroke_width, color=female_tetra_color, layer="female_tetra")

    # 1. Draw Ascending Tetrahedron (Male)
    for u, v in t1_edges:
        ast.add_line(
            t1_pts_2d[u],
            t1_pts_2d[v],
            stroke_width=stroke_width * 1.3,
            color=male_tetra_color,
            layer="male_tetra",
        )

    # 2. Draw Descending Tetrahedron (Female)
    for u, v in t2_edges:
        ast.add_line(
            t2_pts_2d[u],
            t2_pts_2d[v],
            stroke_width=stroke_width * 1.3,
            color=female_tetra_color,
            layer="female_tetra",
        )

    # 3. Optional Core Octahedron
    if show_core_octahedron:
        octa_verts_3d = [
            Point3D(s, 0, 0),
            Point3D(-s, 0, 0),
            Point3D(0, s, 0),
            Point3D(0, -s, 0),
            Point3D(0, 0, s),
            Point3D(0, 0, -s),
        ]
        octa_pts_2d = [project_pt(p) for p in octa_verts_3d]
        octa_edges = [
            (0, 2),
            (2, 1),
            (1, 3),
            (3, 0),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (5, 0),
            (5, 1),
            (5, 2),
            (5, 3),
        ]
        for u, v in octa_edges:
            ast.add_line(
                octa_pts_2d[u],
                octa_pts_2d[v],
                stroke_width=stroke_width * 0.9,
                color="#ffd700",
                layer="core_octa",
                opacity=0.6,
            )

    # 4. Internal 3D Axes
    if wireframe_axes:
        c0 = Point2D(center_x, center_y)
        p_x = project_pt(Point3D(s * 1.2, 0, 0))
        p_y = project_pt(Point3D(0, s * 1.2, 0))
        p_z = project_pt(Point3D(0, 0, s * 1.2))
        ast.add_line(c0, p_x, stroke_width=0.8, color="#ffffff", layer="axes", opacity=0.5)
        ast.add_line(c0, p_y, stroke_width=0.8, color="#ffffff", layer="axes", opacity=0.5)
        ast.add_line(c0, p_z, stroke_width=0.8, color="#ffffff", layer="axes", opacity=0.5)

    # 5. Enclosing Spherical Aura Rings
    if show_spheres:
        c0 = Point2D(center_x, center_y)
        ast.add_circle(c0, radius, stroke_width=stroke_width * 1.1, color=sphere_color, layer="energy_sphere")
        ast.add_circle(c0, radius * 1.08, stroke_width=stroke_width * 0.8, color=sphere_color, layer="energy_sphere")

    return ast


def generate_torus(
    major_radius: float = 120.0,
    minor_radius: float = 45.0,
    strands: Optional[int] = None,
    flow_strands: int = 24,
    u_steps: int = 32,
    v_steps: int = 16,
    rot_x: float = 0.85,
    rot_y: float = 0.35,
    rot_z: float = 0.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 0.8,
    color_ring: str = "#00f0ff",
    color_spoke: str = "#ff007f",
    layer: str = "torus_field",
    **kwargs: Any,
) -> GeometryAST:
    """Generate a 3D Torus Vortex Mesh & Energy Field projection."""
    eff_strands = strands if strands is not None else flow_strands

    ast = GeometryAST(
        title="Toroidal Vortex Energy Field",
        description="Continuous 3D doughnut vortex harmonic torus field exhibiting self-sustaining zero-point energy dynamics.",
        parameters={
            "major_radius": major_radius,
            "minor_radius": minor_radius,
            "strands": eff_strands,
            "flow_strands": eff_strands,
            "u_steps": u_steps,
            "v_steps": v_steps,
            "rot_x": rot_x,
            "rot_y": rot_y,
            "stroke_width": stroke_width,
        },
        tags=["sacred_geometry", "torus", "vortex", "zero_point", "energy_field", "rodin_coil", "3d"],
        layers={
            layer: {"color": color_ring, "stroke_width": stroke_width},
            "poloidal_ribs": {"color": color_spoke, "stroke_width": stroke_width * 0.85, "opacity": 0.7},
            "strand_circles": {"color": color_ring, "stroke_width": stroke_width * 0.9, "opacity": 0.5},
        },
    )

    c0 = Point2D(center_x, center_y)

    # Add concentric strands circles
    for i in range(eff_strands):
        r_c = major_radius - minor_radius + (2.0 * minor_radius * (i / float(max(1, eff_strands - 1))))
        if r_c > 0:
            ast.add_circle(c0, r_c, stroke_width=stroke_width * 0.9, color=color_ring, layer="strand_circles")

    # Generate 3D grid
    grid_3d: List[List[Point3D]] = []
    for i in range(u_steps):
        u = i * (2.0 * math.pi / u_steps)
        row: List[Point3D] = []
        for j in range(v_steps):
            v = j * (2.0 * math.pi / v_steps)
            x = (major_radius + minor_radius * math.cos(v)) * math.cos(u)
            y = (major_radius + minor_radius * math.cos(v)) * math.sin(u)
            z = minor_radius * math.sin(v)
            row.append(Point3D(x, y, z))
        grid_3d.append(row)

    def project_pt(p3: Point3D) -> Point2D:
        pr = p3.rotate_euler(rot_x, rot_y, rot_z)
        p2 = pr.project_2d(orthographic=True)
        return p2.translate(center_x, center_y)

    grid_2d: List[List[Point2D]] = [[project_pt(p) for p in row] for row in grid_3d]

    # Draw longitudinal rings
    for j in range(v_steps):
        ring_pts = [grid_2d[i][j] for i in range(u_steps)]
        ring_pts.append(grid_2d[0][j])
        for k in range(len(ring_pts) - 1):
            ast.add_line(
                ring_pts[k],
                ring_pts[k + 1],
                stroke_width=stroke_width,
                color=color_ring,
                layer=layer,
            )

    # Draw poloidal ribs
    for i in range(u_steps):
        spoke_pts = [grid_2d[i][j] for j in range(v_steps)]
        spoke_pts.append(grid_2d[i][0])
        for k in range(len(spoke_pts) - 1):
            ast.add_line(
                spoke_pts[k],
                spoke_pts[k + 1],
                stroke_width=stroke_width * 0.85,
                color=color_spoke,
                layer="poloidal_ribs",
                opacity=0.7,
            )

    return ast


def generate_torus_knot(
    p: int = 2,
    q: int = 3,
    r_major: Optional[float] = None,
    r_minor: Optional[float] = None,
    major_radius: float = 110.0,
    minor_radius: float = 40.0,
    num_points: int = 480,
    rot_x: float = 0.5,
    rot_y: float = 0.4,
    rot_z: float = 0.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
    stroke_width: float = 1.6,
    knot_color: str = "#39ff14",
    layer: str = "torus_knot",
    **kwargs: Any,
) -> GeometryAST:
    """Generate a Parametric (p, q) Torus Knot in 3D projection."""
    if r_major is not None:
        major_radius = r_major
    if r_minor is not None:
        minor_radius = r_minor

    ast = GeometryAST(
        title=f"Torus Knot ({p}, {q})",
        description=f"Parametric ({p},{q}) continuous topological torus knot wrapping {p} longitudinal and {q} meridian cycles.",
        parameters={
            "p": p,
            "q": q,
            "major_radius": major_radius,
            "minor_radius": minor_radius,
            "r_major": major_radius,
            "r_minor": minor_radius,
            "num_points": num_points,
            "stroke_width": stroke_width,
            "knot_color": knot_color,
        },
        tags=["sacred_geometry", "torus_knot", "trefoil", "topology", "harmonics", "3d"],
        layers={layer: {"color": knot_color, "stroke_width": stroke_width}},
    )

    pts_3d: List[Point3D] = []
    for i in range(num_points):
        theta = (i / float(num_points)) * 2.0 * math.pi
        r_curr = major_radius + minor_radius * math.cos(q * theta)
        x = r_curr * math.cos(p * theta)
        y = r_curr * math.sin(p * theta)
        z = -minor_radius * math.sin(q * theta)
        pts_3d.append(Point3D(x, y, z))

    ast.points3d = pts_3d

    def project_pt(p3: Point3D) -> Point2D:
        pr = p3.rotate_euler(rot_x, rot_y, rot_z)
        p2 = pr.project_2d(orthographic=True)
        return p2.translate(center_x, center_y)

    pts_2d = [project_pt(p3) for p3 in pts_3d]
    pts_2d.append(pts_2d[0])

    for i in range(len(pts_2d) - 1):
        ast.add_line(
            pts_2d[i],
            pts_2d[i + 1],
            stroke_width=stroke_width,
            color=knot_color,
            layer=layer,
        )

    # Add sampled spline
    sampled = pts_2d[::max(1, len(pts_2d) // 32)]
    ast.add_spline(sampled, stroke_width=stroke_width, color=knot_color, layer=layer, closed=True)

    return ast


def generate_vesica_piscis(
    radius: float = 80.0,
    draw_axes: bool = True,
    draw_mandorla_axes: bool = True,
    center_x: float = 0.0,
    center_y: float = 0.0,
    num_rays: int = 24,
    nested_depth: int = 3,
    stroke_width: float = 1.3,
    circle_color: str = "#ffd700",
    ray_color: str = "#00f0ff",
    mandorla_fill: bool = False,
    layer: str = "vesica_piscis",
    **kwargs: Any,
) -> GeometryAST:
    """Generate the Sacred Vesica Piscis (The Vessel of the Fish / Mandorla Portal)."""
    ast = GeometryAST(
        title="Vesica Piscis & Mandorla Portal",
        description="The primal geometric womb of creation where unity divides into polarity, encoding sqrt(3) harmonic proportions.",
        parameters={
            "radius": radius,
            "center_x": center_x,
            "center_y": center_y,
            "num_rays": num_rays,
            "nested_depth": nested_depth,
            "stroke_width": stroke_width,
        },
        tags=["sacred_geometry", "vesica_piscis", "mandorla", "creation", "womb", "sqrt3"],
        layers={
            layer: {"color": circle_color, "stroke_width": stroke_width * 1.3},
            "mandorla_rays": {"color": ray_color, "stroke_width": stroke_width * 0.8, "opacity": 0.65},
            "nested_vesica": {"color": "#ff007f", "stroke_width": stroke_width * 1.0},
        },
    )

    c0 = Point2D(center_x, center_y)

    for depth in range(nested_depth):
        scale_fac = 1.0 / (depth * 0.5 + 1.0)
        curr_r = radius * scale_fac
        curr_layer = layer if depth == 0 else "nested_vesica"

        c_left = Point2D(c0.x - curr_r / 2.0, c0.y)
        c_right = Point2D(c0.x + curr_r / 2.0, c0.y)

        ast.add_circle(c_left, curr_r, stroke_width=stroke_width, color=circle_color, layer=curr_layer)
        ast.add_circle(c_right, curr_r, stroke_width=stroke_width, color=circle_color, layer=curr_layer)

        if draw_axes or draw_mandorla_axes:
            h_half = curr_r * math.sqrt(3.0) / 2.0
            p_top = Point2D(c0.x, c0.y - h_half)
            p_bot = Point2D(c0.x, c0.y + h_half)
            ast.add_line(p_top, p_bot, stroke_width=stroke_width * 0.9, color=circle_color, layer=curr_layer)
            ast.add_line(c_left, c_right, stroke_width=stroke_width * 0.9, color=circle_color, layer=curr_layer)

    if num_rays > 0:
        outer_r = radius * 1.6
        for i in range(num_rays):
            angle = i * (2.0 * math.pi / num_rays)
            p_end = Point2D.from_polar(outer_r, angle, origin=c0)
            ast.add_line(
                c0,
                p_end,
                stroke_width=stroke_width * 0.75,
                color=ray_color,
                layer="mandorla_rays",
                opacity=0.6,
            )

    ast.add_circle(c0, radius * 1.732, stroke_width=stroke_width * 1.2, color=circle_color, layer=layer)

    return ast
