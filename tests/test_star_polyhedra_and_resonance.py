"""Tests for Archimedean & Kepler-Poinsot Star Polyhedra and Sacred Resonance Frequency Matrix."""

from __future__ import annotations

import json
from ufo_sacred_geometry.generators.star_polyhedra import (
    SACRED_FREQUENCY_MATRIX,
    SacredFrequency,
    generate_cymatic_resonance_pattern,
    generate_star_polyhedron_projection,
    get_sacred_frequency,
    list_sacred_frequencies,
)
from ufo_sacred_geometry.catalog import generate_pattern, get_preset, list_presets
from ufo_sacred_geometry.mcp_server import MCPServer
from ufo_sacred_geometry.ui_server import generate_pattern_ast


def test_star_polyhedron_projection_cuboctahedron() -> None:
    ast = generate_star_polyhedron_projection(poly_type="cuboctahedron", size=120.0)
    assert ast.title == "Star Polyhedron: Cuboctahedron (Vector Equilibrium)"
    assert len(ast.points3d) == 12
    assert len(ast.lines) == 24  # 24 edges of cuboctahedron
    assert len(ast.circles) == 12  # 12 vertex nodes
    assert ast.bounds().width > 0


def test_star_polyhedron_projection_small_stellated_dodecahedron() -> None:
    ast = generate_star_polyhedron_projection(poly_type="small_stellated_dodecahedron", size=130.0)
    assert "Small Stellated Dodecahedron" in ast.title
    assert len(ast.points3d) == 12
    assert len(ast.lines) > 0
    assert ast.bounds().height > 0


def test_star_polyhedron_projection_great_stellated_and_buckyball() -> None:
    ast_great = generate_star_polyhedron_projection(poly_type="great_stellated_dodecahedron", size=100.0)
    assert len(ast_great.points3d) == 20
    assert len(ast_great.lines) > 0

    ast_bucky = generate_star_polyhedron_projection(poly_type="truncated_icosahedron", size=100.0)
    assert len(ast_bucky.points3d) == 60
    assert len(ast_bucky.lines) == 90


def test_sacred_resonance_frequency_matrix_metadata() -> None:
    freq_528 = get_sacred_frequency("solfeggio_528")
    assert freq_528.freq_hz == 528.0
    assert "DNA" in freq_528.name or "Transformation" in freq_528.name
    assert freq_528.category == "solfeggio"

    freq_schumann = get_sacred_frequency("schumann_fundamental")
    assert freq_schumann.freq_hz == 7.83

    all_freqs = list_sacred_frequencies()
    assert len(all_freqs) >= 12
    solfeggios = list_sacred_frequencies(category="solfeggio")
    assert len(solfeggios) == 9


def test_generate_cymatic_resonance_pattern() -> None:
    ast = generate_cymatic_resonance_pattern(frequency_key="solfeggio_528", radius=150.0, harmonics_count=5)
    assert "528" in ast.title
    assert len(ast.circles) >= 5  # Outer Bessel nodal rings + center point
    assert len(ast.lines) > 20  # Rosettes and radial spoke lines
    assert ast.bounds().width > 0


def test_catalog_new_presets() -> None:
    p_ve = get_preset("cuboctahedron_vector_equilibrium")
    assert p_ve is not None
    assert p_ve.category == "Archimedean & Star Polyhedra"

    ast_ve = generate_pattern("cuboctahedron_vector_equilibrium")
    assert len(ast_ve.lines) == 24

    p_528 = get_preset("sacred_resonance_solfeggio_528")
    assert p_528 is not None
    ast_528 = generate_pattern("sacred_resonance_solfeggio_528")
    assert len(ast_528.circles) >= 5


def test_mcp_star_polyhedron_and_resonance_tools() -> None:
    server = MCPServer()
    # Star Polyhedron tool
    req_poly = {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/call",
        "params": {
            "name": "geometry_star_polyhedron",
            "arguments": {"poly_type": "cuboctahedron", "size": 100.0},
        },
    }
    res_poly = server.handle_request(req_poly)
    assert res_poly is not None
    assert "result" in res_poly
    data_poly = json.loads(res_poly["result"]["content"][0]["text"])
    assert data_poly["poly_type"] == "cuboctahedron"
    assert data_poly["vertices_3d_count"] == 12
    assert "<svg" in data_poly["svg_xml"]

    # Resonance tool
    req_res = {
        "jsonrpc": "2.0",
        "id": 102,
        "method": "tools/call",
        "params": {
            "name": "geometry_sacred_resonance",
            "arguments": {"frequency_key": "solfeggio_528"},
        },
    }
    res_res = server.handle_request(req_res)
    assert res_res is not None
    assert "result" in res_res
    data_res = json.loads(res_res["result"]["content"][0]["text"])
    assert data_res["frequency_hz"] == 528.0
    assert "<svg" in data_res["svg_xml"]


def test_ui_server_pattern_generation() -> None:
    ast_cubo = generate_pattern_ast("cuboctahedron_vector_equilibrium")
    assert len(ast_cubo.lines) == 24

    ast_res = generate_pattern_ast("sacred_resonance_solfeggio_528")
    assert len(ast_res.circles) >= 5
