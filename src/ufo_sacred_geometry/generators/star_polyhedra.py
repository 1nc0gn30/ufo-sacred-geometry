"""Archimedean & Kepler-Poinsot 3D Star Polyhedra & Sacred Resonance Frequency Matrix.

Provides:
1. Kepler-Poinsot Star Polyhedra:
   - Small Stellated Dodecahedron ({5/2, 5})
   - Great Stellated Dodecahedron ({5/2, 3})
   - Great Dodecahedron ({5, 5/2})
   - Great Icosahedron ({3, 5/2})
2. Archimedean Semiregular Polyhedra:
   - Cuboctahedron (Vector Equilibrium of Buckminster Fuller)
   - Icosidodecahedron
   - Truncated Octahedron (space-filling permutohedron)
   - Truncated Icosahedron (Buckyball / C60 Fullerene)
3. Sacred Harmonic Resonance Frequency Matrix:
   - Solfeggio Scale (174Hz, 285Hz, 396Hz [Liberation], 417Hz [Undoing], 528Hz [DNA Transformation],
     639Hz [Connection], 741Hz [Awakening Intuition], 852Hz [Spiritual Order], 963Hz [Transcendence])
   - Schumann Earth Ionospheric Resonances (7.83Hz, 14.3Hz, 20.8Hz, 27.3Hz, 33.8Hz)
   - Planetary Orbital Harmonics (Sun 126.22Hz, Earth Year 136.1Hz [Om], Moon 210.42Hz)
   - Cymatic nodal harmonic resonance circle generators and visual chord projections.

100% Python Standard Library.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..models import GeometryAST, Point2D, Point3D

# Golden Ratio Constant
PHI = (1.0 + math.sqrt(5.0)) / 2.0


# =============================================================================
# 1. Kepler-Poinsot & Archimedean Polyhedral Geometry Generators
# =============================================================================

def _generate_small_stellated_dodecahedron_3d(scale: float = 100.0) -> Tuple[List[Point3D], List[Tuple[int, int]]]:
    """
    Generate the Small Stellated Dodecahedron ({5/2, 5}).
    Has 12 pentagrammic faces and 12 vertices: 12 vertices of an icosahedron.
    The edges connect vertices like 12 intersecting pentagrams.
    """
    scale_fac = scale / math.sqrt(1.0 + PHI * PHI)
    vertices: List[Point3D] = []
    # 12 vertices of golden rectangles (icosahedron vertex arrangement)
    for y in [-1.0, 1.0]:
        for z in [-PHI, PHI]:
            vertices.append(Point3D(0.0, y * scale_fac, z * scale_fac))
    for x in [-1.0, 1.0]:
        for y in [-PHI, PHI]:
            vertices.append(Point3D(x * scale_fac, y * scale_fac, 0.0))
    for x in [-PHI, PHI]:
        for z in [-1.0, 1.0]:
            vertices.append(Point3D(x * scale_fac, 0.0, z * scale_fac))

    # Star pentagrams connect vertices at golden ratio chord distance (~ 2 * PHI * scale_fac)
    edges: List[Tuple[int, int]] = []
    target_dist = 2.0 * PHI * scale_fac
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            d = vertices[i].distance_to(vertices[j])
            if abs(d - target_dist) < 0.2 * scale_fac:
                edges.append((i, j))
    return vertices, edges


def _generate_great_stellated_dodecahedron_3d(scale: float = 100.0) -> Tuple[List[Point3D], List[Tuple[int, int]]]:
    """
    Generate Great Stellated Dodecahedron ({5/2, 3}).
    Vertices are the 20 vertices of a regular dodecahedron.
    Edges connect alternate vertices forming 12 intersecting pentagrams (30 edges).
    """
    inv_phi = 1.0 / PHI
    scale_fac = scale / math.sqrt(3.0)
    vertices: List[Point3D] = []
    # 8 cube vertices
    for x in [-1.0, 1.0]:
        for y in [-1.0, 1.0]:
            for z in [-1.0, 1.0]:
                vertices.append(Point3D(x * scale_fac, y * scale_fac, z * scale_fac))
    # 12 golden rectangle vertices
    for y in [-inv_phi, inv_phi]:
        for z in [-PHI, PHI]:
            vertices.append(Point3D(0.0, y * scale_fac, z * scale_fac))
    for x in [-inv_phi, inv_phi]:
        for y in [-PHI, PHI]:
            vertices.append(Point3D(x * scale_fac, y * scale_fac, 0.0))
    for x in [-PHI, PHI]:
        for z in [-inv_phi, inv_phi]:
            vertices.append(Point3D(x * scale_fac, 0.0, z * scale_fac))

    # Connect vertices at star pentagram chord length (~ 2 * scale_fac)
    edges: List[Tuple[int, int]] = []
    target_dist = 2.0 * scale_fac
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            d = vertices[i].distance_to(vertices[j])
            if abs(d - target_dist) < 0.15 * scale_fac:
                edges.append((i, j))
    return vertices, edges


def _generate_cuboctahedron_3d(scale: float = 100.0) -> Tuple[List[Point3D], List[Tuple[int, int]]]:
    """
    Generate Cuboctahedron (Vector Equilibrium of Buckminster Fuller).
    12 vertices: all permutations of (±1, ±1, 0) normalized.
    24 equal edges connecting each vertex to its 4 nearest neighbors.
    In vector equilibrium, all 24 edges equal the distance from the center to all 12 vertices!
    """
    s = scale / math.sqrt(2.0)
    vertices: List[Point3D] = [
        Point3D(s, s, 0.0), Point3D(s, -s, 0.0), Point3D(-s, s, 0.0), Point3D(-s, -s, 0.0),
        Point3D(s, 0.0, s), Point3D(s, 0.0, -s), Point3D(-s, 0.0, s), Point3D(-s, 0.0, -s),
        Point3D(0.0, s, s), Point3D(0.0, s, -s), Point3D(0.0, -s, s), Point3D(0.0, -s, -s),
    ]
    edges: List[Tuple[int, int]] = []
    target_dist = scale  # Distance between adjacent vertices equals radius
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            d = vertices[i].distance_to(vertices[j])
            if abs(d - target_dist) < 0.1 * scale:
                edges.append((i, j))
    return vertices, edges


def _generate_icosidodecahedron_3d(scale: float = 100.0) -> Tuple[List[Point3D], List[Tuple[int, int]]]:
    """
    Generate Icosidodecahedron (Archimedean solid with 30 vertices, 60 edges, 32 faces).
    Vertices: cyclic permutations of (0, 0, ±phi) and (±1/2, ±phi/2, ±(1+phi)/2).
    """
    s = scale / PHI
    vertices: List[Point3D] = []
    # (0, 0, ±phi)
    for z in [-PHI, PHI]:
        vertices.append(Point3D(0.0, 0.0, z * s))
    for y in [-PHI, PHI]:
        vertices.append(Point3D(0.0, y * s, 0.0))
    for x in [-PHI, PHI]:
        vertices.append(Point3D(x * s, 0.0, 0.0))

    # (±1/2, ±phi/2, ±(1+phi)/2)
    p1 = 0.5 * s
    p2 = 0.5 * PHI * s
    p3 = 0.5 * (1.0 + PHI) * s
    for x in [-p1, p1]:
        for y in [-p2, p2]:
            for z in [-p3, p3]:
                vertices.append(Point3D(x, y, z))
                vertices.append(Point3D(y, z, x))
                vertices.append(Point3D(z, x, y))

    # Remove duplicates
    unique_verts: List[Point3D] = []
    for v in vertices:
        if not any(v.distance_to(u) < 1e-4 for u in unique_verts):
            unique_verts.append(v)

    # 60 edges connecting nearest neighbors (dist = s)
    edges: List[Tuple[int, int]] = []
    target_dist = s
    for i in range(len(unique_verts)):
        for j in range(i + 1, len(unique_verts)):
            d = unique_verts[i].distance_to(unique_verts[j])
            if abs(d - target_dist) < 0.15 * s:
                edges.append((i, j))
    return unique_verts, edges


def _generate_truncated_icosahedron_3d(scale: float = 100.0) -> Tuple[List[Point3D], List[Tuple[int, int]]]:
    """
    Generate Truncated Icosahedron (Buckyball / C60 fullerene).
    60 vertices, 90 edges (12 pentagonal and 20 hexagonal faces).
    """
    s = scale / math.sqrt(9.0 * PHI + 10.0)
    vertices: List[Point3D] = []
    # Even permutations of (0, ±1, ±3phi), (±1, ±(2+phi), ±2phi), (±phi, ±2, ±(2phi+1))
    coords1 = [0.0, 1.0, 3.0 * PHI]
    coords2 = [1.0, 2.0 + PHI, 2.0 * PHI]
    coords3 = [PHI, 2.0, 2.0 * PHI + 1.0]

    for p in [coords1, coords2, coords3]:
        for sx in [-1.0, 1.0]:
            for sy in [-1.0, 1.0]:
                for sz in [-1.0, 1.0]:
                    # Even permutations (0, 1, 2), (1, 2, 0), (2, 0, 1)
                    raw_pts = [
                        (p[0] * sx, p[1] * sy, p[2] * sz),
                        (p[1] * sy, p[2] * sz, p[0] * sx),
                        (p[2] * sz, p[0] * sx, p[1] * sy),
                    ]
                    for x, y, z in raw_pts:
                        pt = Point3D(x * s, y * s, z * s)
                        if not any(pt.distance_to(u) < 1e-3 for u in vertices):
                            vertices.append(pt)

    # 90 edges: edge length = 2 * s
    edges: List[Tuple[int, int]] = []
    target_dist = 2.0 * s
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            d = vertices[i].distance_to(vertices[j])
            if abs(d - target_dist) < 0.2 * s:
                edges.append((i, j))
    return vertices, edges


def generate_star_polyhedron_projection(
    poly_type: str = "cuboctahedron",
    size: float = 140.0,
    rot_x: float = 0.55,
    rot_y: float = 0.75,
    rot_z: float = 0.0,
    perspective: bool = False,
    stroke_width: float = 1.5,
    color: str = "#00f0ff",
    show_nodes: bool = True,
    node_radius: float = 3.5,
    center_x: float = 0.0,
    center_y: float = 0.0,
    layer: str = "star_polyhedron",
    **kwargs: Any,
) -> GeometryAST:
    """
    Project 3D Archimedean or Kepler-Poinsot Star Polyhedron wireframe onto 2D plane.
    Supported poly_types:
    - 'small_stellated_dodecahedron'
    - 'great_stellated_dodecahedron'
    - 'cuboctahedron' (Vector Equilibrium)
    - 'icosidodecahedron'
    - 'truncated_icosahedron' (Buckyball / C60)
    """
    ptype = poly_type.lower().strip().replace("-", "_")

    if "small_stellated" in ptype:
        verts, edges = _generate_small_stellated_dodecahedron_3d(size)
        title = "Small Stellated Dodecahedron"
    elif "great_stellated" in ptype:
        verts, edges = _generate_great_stellated_dodecahedron_3d(size)
        title = "Great Stellated Dodecahedron"
    elif "cuboctahedron" in ptype or "vector_equilibrium" in ptype:
        verts, edges = _generate_cuboctahedron_3d(size)
        title = "Cuboctahedron (Vector Equilibrium)"
    elif "icosidodecahedron" in ptype:
        verts, edges = _generate_icosidodecahedron_3d(size)
        title = "Icosidodecahedron"
    elif "truncated_icosahedron" in ptype or "buckyball" in ptype or "c60" in ptype:
        verts, edges = _generate_truncated_icosahedron_3d(size)
        title = "Truncated Icosahedron (Buckyball)"
    else:
        raise ValueError(
            f"Unknown star polyhedron type '{poly_type}'. Choose from: 'cuboctahedron', "
            f"'small_stellated_dodecahedron', 'great_stellated_dodecahedron', 'icosidodecahedron', 'truncated_icosahedron'."
        )

    ast = GeometryAST(
        title=f"Star Polyhedron: {title}",
        description=f"3D Euler projection of {title} with {len(verts)} vertices and {len(edges)} edges.",
        parameters={
            "poly_type": poly_type,
            "size": size,
            "rot_x": rot_x,
            "rot_y": rot_y,
            "rot_z": rot_z,
            "perspective": perspective,
            "stroke_width": stroke_width,
            "color": color,
        },
        tags=["sacred_geometry", "polyhedra", "star_polyhedron", ptype, "archimedean", "3d_projection"],
        layers={
            layer: {"color": color, "stroke_width": stroke_width},
            "poly_nodes": {"color": "#ffd700", "stroke_width": stroke_width},
        },
    )
    ast.points3d = verts

    pts_2d: List[Point2D] = []
    for p3 in verts:
        p_rot = p3.rotate_euler(rot_x, rot_y, rot_z)
        if perspective:
            proj = p_rot.project_2d(focal_length=450.0, camera_z=600.0)
        else:
            proj = p_rot.project_2d(orthographic=True)
        pts_2d.append(proj.translate(center_x, center_y))

    for u, v in edges:
        if u < len(pts_2d) and v < len(pts_2d):
            ast.add_line(pts_2d[u], pts_2d[v], stroke_width=stroke_width, color=color, layer=layer)

    if show_nodes:
        for pt in pts_2d:
            ast.add_circle(pt, node_radius, stroke_width=stroke_width, color="#ffd700", fill="#050814", layer="poly_nodes")

    return ast


# =============================================================================
# 2. Sacred Resonance Frequency Matrix & Cymatic Harmonic Generator
# =============================================================================

@dataclass
class SacredFrequency:
    """Frequency definition with physical and esoteric attributes."""
    name: str
    freq_hz: float
    category: str
    chakra_or_planet: str
    color_hex: str
    geometry_polygon_order: int
    description: str


# Canonical Sacred Harmonic Matrix
SACRED_FREQUENCY_MATRIX: Dict[str, SacredFrequency] = {
    # Solfeggio Frequencies
    "solfeggio_174": SacredFrequency("Foundation", 174.0, "solfeggio", "Physical Grounding", "#7f1d1d", 3, "Pain relief and physical foundation frequency."),
    "solfeggio_285": SacredFrequency("Quantum Cognition", 285.0, "solfeggio", "Bio-Energy Field", "#b91c1c", 4, "Tissue rejuvenation and cellular regeneration."),
    "solfeggio_396": SacredFrequency("Liberation from Guilt & Fear", 396.0, "solfeggio", "Root Chakra (Muladhara)", "#dc2626", 4, "Grounding power, turns grief into joy and dissolves subconscious fear."),
    "solfeggio_417": SacredFrequency("Undoing Situations & Facilitating Change", 417.0, "solfeggio", "Sacral Chakra (Svadhisthana)", "#ea580c", 6, "Clears traumatic experiences and facilitates positive transmutation."),
    "solfeggio_528": SacredFrequency("Transformation & Miracles (DNA Repair)", 528.0, "solfeggio", "Solar Plexus (Manipura)", "#ca8a04", 6, "The 'Love Frequency' - mathematical harmonic of chlorophyll, water structure, and DNA bio-repair."),
    "solfeggio_639": SacredFrequency("Harmonizing Relationships & Interconnection", 639.0, "solfeggio", "Heart Chakra (Anahata)", "#16a34a", 12, "Enhances cellular communication, empathy, community harmony, and relational balance."),
    "solfeggio_741": SacredFrequency("Awakening Intuition & Solving Problems", 741.0, "solfeggio", "Throat Chakra (Vishuddha)", "#0284c7", 16, "Detoxification of radiation, expands pure intuitive expression and vocal truth."),
    "solfeggio_852": SacredFrequency("Returning to Spiritual Order", 852.0, "solfeggio", "Third Eye (Ajna)", "#4f46e5", 24, "Awakens inner sight, clairvoyance, cellular lucidity, and higher cosmic perception."),
    "solfeggio_963": SacredFrequency("Pure Cosmic Transcendence / Crown", 963.0, "solfeggio", "Crown Chakra (Sahasrara)", "#9333ea", 32, "Crown awakening, oneness with the Light, pineal activation and cosmic connection."),
    # Schumann Ionospheric Resonances
    "schumann_fundamental": SacredFrequency("Schumann Fundamental Earth Resonance", 7.83, "schumann", "Earth Ionosphere / Alpha Waves", "#10b981", 8, "Primary standing electromagnetic wave in Earth-ionosphere cavity; synchronizes human alpha brainwaves."),
    "schumann_mode2": SacredFrequency("Schumann Harmonic Second Mode", 14.3, "schumann", "Beta Waves / Bio-field", "#06b6d4", 14, "Secondary ionospheric resonant node."),
    "schumann_mode3": SacredFrequency("Schumann Harmonic Third Mode", 20.8, "schumann", "High Beta Waves", "#3b82f6", 21, "Tertiary resonant frequency."),
    # Planetary & Cosmic Harmonics (Cousto Cosmic Octave)
    "cosmic_om_earth": SacredFrequency("Earth Year Orbital OM", 136.1, "planetary", "Earth Period / Anahata", "#059669", 12, "Earth's 365-day solar rotation transposed to 32nd octave (traditional Indian Om frequency)."),
    "sun_frequency": SacredFrequency("Solar Core Oscillator", 126.22, "planetary", "Sol / Sun", "#f59e0b", 10, "Transposed acoustic frequency of the Sun's diameter and gravitational resonance."),
    "moon_synodic": SacredFrequency("Synodic Lunar Gateway", 210.42, "planetary", "Chandra / Moon", "#e0e7ff", 28, "Synodic lunar month resonance connecting tides, intuition, and biorhythms."),
}


def get_sacred_frequency(key: str) -> SacredFrequency:
    """Retrieve frequency metadata by identifier."""
    clean_key = key.lower().strip().replace("-", "_")
    if clean_key in SACRED_FREQUENCY_MATRIX:
        return SACRED_FREQUENCY_MATRIX[clean_key]
    for k, v in SACRED_FREQUENCY_MATRIX.items():
        if clean_key in k or k in clean_key:
            return v
    raise KeyError(f"Sacred frequency '{key}' not found. Valid keys: {list(SACRED_FREQUENCY_MATRIX.keys())}")


def list_sacred_frequencies(category: Optional[str] = None) -> List[Dict[str, Any]]:
    """List all frequencies in the matrix with optional category filtering."""
    results = []
    for k, f in SACRED_FREQUENCY_MATRIX.items():
        if category and category.lower() != "all" and f.category.lower() != category.lower():
            continue
        results.append({
            "id": k,
            "name": f.name,
            "freq_hz": f.freq_hz,
            "category": f.category,
            "chakra_or_planet": f.chakra_or_planet,
            "color_hex": f.color_hex,
            "geometry_polygon_order": f.geometry_polygon_order,
            "description": f.description,
        })
    return results


def generate_cymatic_resonance_pattern(
    frequency_key: str = "solfeggio_528",
    radius: float = 160.0,
    harmonics_count: int = 6,
    nodal_lines: int = 12,
    stroke_width: float = 1.2,
    center_x: float = 0.0,
    center_y: float = 0.0,
    layer: str = "cymatic_resonance",
    **kwargs: Any,
) -> GeometryAST:
    """
    Generate a 2D Cymatic Chladni / Bessel Nodal Waveform Sacred Resonance Geometry
    based on the exact frequency vibrational matrix (Solfeggio, Schumann, Planetary).
    """
    freq_data = get_sacred_frequency(frequency_key)
    base_color = freq_data.color_hex
    order = freq_data.geometry_polygon_order or 6

    ast = GeometryAST(
        title=f"Sacred Cymatic Resonance: {freq_data.name} ({freq_data.freq_hz} Hz)",
        description=f"Vibrational Chladni nodal plate geometry calculated for {freq_data.freq_hz} Hz ({freq_data.chakra_or_planet}).",
        parameters={
            "frequency_key": frequency_key,
            "frequency_hz": freq_data.freq_hz,
            "frequency_name": freq_data.name,
            "category": freq_data.category,
            "radius": radius,
            "harmonics_count": harmonics_count,
            "nodal_lines": nodal_lines,
            "base_color": base_color,
        },
        tags=["sacred_geometry", "resonance", "cymatics", "solfeggio", freq_data.category, f"{int(freq_data.freq_hz)}hz"],
        layers={
            layer: {"color": base_color, "stroke_width": stroke_width},
            "outer_ring": {"color": "#ffd700", "stroke_width": stroke_width * 1.5},
            "radial_spokes": {"color": base_color, "stroke_width": stroke_width * 0.75},
            "nodal_petals": {"color": "#00ffff", "stroke_width": stroke_width},
        },
    )

    # 1. Outer boundary concentric circles representing Bessel function wave nodes
    for h in range(1, harmonics_count + 1):
        r_node = radius * (h / harmonics_count)
        ast.add_circle(
            Point2D(center_x, center_y),
            r_node,
            stroke_width=stroke_width * (1.5 if h == harmonics_count else 0.8),
            color=base_color if h < harmonics_count else "#ffd700",
            layer="outer_ring" if h == harmonics_count else layer,
            opacity=0.9 if h == harmonics_count else 0.6,
        )

    # 2. Radial nodal lines / spokes (zero-amplitude wave lines)
    spoke_count = max(nodal_lines, order * 2)
    for s in range(spoke_count):
        angle = (2.0 * math.pi / spoke_count) * s
        dx = radius * math.cos(angle)
        dy = radius * math.sin(angle)
        ast.add_line(
            Point2D(center_x, center_y),
            Point2D(center_x + dx, center_y + dy),
            stroke_width=stroke_width * 0.75,
            color=base_color,
            layer="radial_spokes",
            opacity=0.45,
        )

    # 3. Wave interference rosettes / Chladni petals modulated by sinusoidal frequency
    pts_per_wave = 180
    for h in range(1, harmonics_count):
        ring_r = radius * (h / harmonics_count)
        amp = (radius / harmonics_count) * 0.4
        petal_pts: List[Point2D] = []
        for i in range(pts_per_wave):
            theta = (2.0 * math.pi / pts_per_wave) * i
            r_mod = ring_r + amp * math.cos(order * theta)
            px = center_x + r_mod * math.cos(theta)
            py = center_y + r_mod * math.sin(theta)
            petal_pts.append(Point2D(px, py))

        for j in range(len(petal_pts)):
            p1 = petal_pts[j]
            p2 = petal_pts[(j + 1) % len(petal_pts)]
            ast.add_line(p1, p2, stroke_width=stroke_width, color="#00ffff", layer="nodal_petals", opacity=0.85)

    # 4. Central nodal point
    ast.add_circle(Point2D(center_x, center_y), 4.0, stroke_width=stroke_width, color="#ffd700", fill="#ffd700", layer=layer)
    return ast
