"""Unit tests for SVG, DXF, and OBJ multi-format geometry exporters."""

import os
from pathlib import Path
import pytest

import ufo_sacred_geometry
from ufo_sacred_geometry.exporters import (
    DXFExporter,
    OBJExporter,
    SVG_THEMES,
    SVGExporter,
    export_dxf,
    export_obj,
    export_svg,
    hex_to_aci,
)
from ufo_sacred_geometry.generators import (
    generate_flower_of_life,
    generate_merkaba,
    generate_metatrons_cube,
    generate_seed_of_life,
    generate_sri_yantra,
)
from ufo_sacred_geometry.models import (
    Arc,
    Circle,
    GeometryAST,
    LineSegment,
    Point2D,
    Point3D,
    Polygon,
    Spline,
)


def test_hex_to_aci_color_mapping():
    """Verify Hex CSS colors map accurately to AutoCAD Color Index (ACI 1-7)."""
    assert hex_to_aci("#ff0000") == 1  # Red
    assert hex_to_aci("#ffd700") == 2  # Yellow / Gold
    assert hex_to_aci("#00ff00") == 3  # Green
    assert hex_to_aci("#00ffff") == 4  # Cyan
    assert hex_to_aci("#0000ff") == 5  # Blue
    assert hex_to_aci("#ff00ff") == 6  # Magenta
    assert hex_to_aci("#ffffff") == 7  # White
    assert hex_to_aci("invalid") == 7  # Fallback


def test_svg_exporter_generation_and_themes(sample_ast, tmp_path):
    """Verify SVGExporter renders complete XML vector output across color themes."""
    exporter = SVGExporter(theme="dark_gold", width=1000.0, height=1000.0, glow=True)
    svg_str = exporter.export(sample_ast)

    assert svg_str.startswith('<?xml version="1.0" encoding="UTF-8"')
    assert '<svg xmlns="http://www.w3.org/2000/svg"' in svg_str
    assert 'viewBox="' in svg_str
    assert '<circle' in svg_str
    assert '<line' in svg_str
    assert '<polygon' in svg_str or '<polyline' in svg_str
    assert 'id="sacred_glow"' in svg_str
    assert '</svg>' in svg_str

    # Test all predefined themes
    for theme_name in SVG_THEMES.keys():
        theme_svg = export_svg(sample_ast, theme=theme_name)
        assert '</svg>' in theme_svg

    # Test export to file
    out_file = tmp_path / "test_output.svg"
    export_svg(sample_ast, file_path=out_file)
    assert out_file.exists()
    assert out_file.stat().st_size > 100


def test_svg_arc_and_spline_rendering():
    """Verify Arc and Spline vector elements in SVG."""
    ast = GeometryAST(title="Arc and Spline Test")
    ast.add_arc(Point2D(0.0, 0.0), 50.0, 0.0, 1.570796)
    ast.add_spline([Point2D(0.0, 0.0), Point2D(20.0, 40.0), Point2D(40.0, 0.0)])

    svg = export_svg(ast)
    assert '<path d="M ' in svg
    assert '<polyline points="' in svg


def test_dxf_exporter_structure(sample_ast, tmp_path):
    """Verify DXFExporter creates standard AutoCAD R12/2000 compliant sections and entities."""
    exporter = DXFExporter(precision=6, units_mm=True)
    dxf_str = exporter.export(sample_ast)

    # Check structural sections
    assert "SECTION" in dxf_str
    assert "HEADER" in dxf_str
    assert "$ACADVER" in dxf_str
    assert "TABLES" in dxf_str
    assert "LAYER" in dxf_str
    assert "ENTITIES" in dxf_str
    assert "EOF" in dxf_str

    # Check entity tokens
    assert "CIRCLE" in dxf_str
    assert "LINE" in dxf_str
    assert "LWPOLYLINE" in dxf_str or "POLYLINE" in dxf_str

    # Test export to file
    out_dxf = tmp_path / "test_output.dxf"
    export_dxf(sample_ast, file_path=out_dxf)
    assert out_dxf.exists()
    assert out_dxf.stat().st_size > 100


def test_dxf_arc_and_spline_entities():
    """Verify ARC and sampled spline LWPOLYLINE in DXF."""
    ast = GeometryAST(title="DXF Primitives")
    ast.add_arc(Point2D(10.0, 10.0), 30.0, 0.0, 3.14159)
    ast.add_spline([Point2D(0.0, 0.0), Point2D(10.0, 20.0), Point2D(20.0, 0.0)])

    dxf = export_dxf(ast)
    assert "ARC" in dxf
    assert "LWPOLYLINE" in dxf


def test_obj_exporter_mesh_and_mtl(sample_ast, tmp_path):
    """Verify OBJExporter generates 3D vertices, normals, faces, and companion MTL material."""
    exporter = OBJExporter(
        base_type="cylinder",
        base_thickness=5.0,
        relief_height=2.0,
        stroke_width_3d=1.0,
    )
    obj_str = exporter.export(sample_ast)

    # Validate OBJ structure
    assert "# UFO Sacred Geometry 3D Mesh Exporter" in obj_str or "o SacredGeometry" in obj_str
    assert "v " in obj_str  # Vertices
    assert "vn " in obj_str  # Normals
    assert "f " in obj_str  # Faces
    assert "usemtl " in obj_str

    # Validate MTL structure
    mtl_str = exporter.export_mtl()
    assert "newmtl " in mtl_str
    assert "Kd " in mtl_str

    # Test file write with companion MTL
    out_obj = tmp_path / "medallion.obj"
    exporter.export_to_file(sample_ast, out_obj)
    assert out_obj.exists()
    assert out_obj.with_suffix(".mtl").exists()
    assert out_obj.stat().st_size > 500


def test_obj_base_types(sample_ast):
    """Verify 'box', 'cylinder', and 'none' base types in 3D OBJ export."""
    for base in ["cylinder", "box", "none"]:
        exporter = OBJExporter(base_type=base)
        obj_text = exporter.export(sample_ast)
        assert "v " in obj_text
        assert "f " in obj_text


def test_top_level_exporters_on_complex_generators(tmp_path):
    """Verify top-level package export functions work on complex sacred geometry patterns."""
    metatron = generate_metatrons_cube(radius=60.0)
    sri_yantra = generate_sri_yantra(size=100.0)
    merkaba = generate_merkaba(radius=80.0)

    # SVG export
    svg_meta = ufo_sacred_geometry.export_svg(metatron, theme="neon_matrix")
    assert '</svg>' in svg_meta

    # DXF export
    dxf_sri = ufo_sacred_geometry.export_dxf(sri_yantra)
    assert "EOF" in dxf_sri

    # OBJ export
    obj_merk = ufo_sacred_geometry.export_obj(merkaba)
    assert "v " in obj_merk
