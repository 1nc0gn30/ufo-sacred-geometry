"""Comprehensive Test Suite for ufo_sacred_geometry Core Engine, Generators, Exporters, and Catalog."""

from __future__ import annotations

import json
import math
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ufo_sacred_geometry import (
    PRESETS,
    Arc,
    BoundingBox,
    Circle,
    DXFExporter,
    GeometryAST,
    LineSegment,
    OBJExporter,
    PatternPreset,
    Point2D,
    Point3D,
    Polygon,
    Spline,
    SVGExporter,
    atomic_write_bytes,
    atomic_write_text,
    export_dxf,
    export_obj,
    export_svg,
    generate_barbury_castle_glyph,
    generate_chilbolton_binary_glyph,
    generate_crop_circle,
    generate_egg_of_life,
    generate_fibonacci_sequence,
    generate_flower_of_life,
    generate_fruit_of_life,
    generate_golden_rectangles,
    generate_golden_spiral,
    generate_golden_triangle_spiral,
    generate_julia_set_glyph,
    generate_merkaba,
    generate_metatrons_cube,
    generate_milk_hill_glyph,
    generate_pattern,
    generate_phyllotaxis,
    generate_platonic_solid_projection,
    generate_seed_of_life,
    generate_sri_yantra,
    generate_torus,
    generate_torus_knot,
    generate_tree_of_life,
    generate_triskele_glyph,
    generate_vesica_piscis,
    get_catalog_summary,
    get_platform_info,
    get_preset,
    list_categories,
    list_presets,
    list_tags,
    normalize_path,
    read_json_safe,
    read_text_safe,
    safe_delete,
    write_json_safe,
)


class TestCompat(unittest.TestCase):
    """Test cross-platform compatibility helper functions."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmppath = Path(self.tmpdir.name)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_platform_info(self) -> None:
        info = get_platform_info()
        self.assertIn("python_version", info)
        self.assertIn("system", info)
        self.assertIn("is_linux", info)
        self.assertIn("is_windows", info)

    def test_atomic_write_text_and_read(self) -> None:
        target = self.tmppath / "sub" / "test.txt"
        content = "✨ Sacred Geometry Nexus 🛸"
        written = atomic_write_text(target, content)
        self.assertTrue(written.exists())
        read_back = read_text_safe(target)
        self.assertEqual(read_back, content)

    def test_atomic_write_bytes(self) -> None:
        target = self.tmppath / "binary.bin"
        data = b"\x00\xff\xfe\x42"
        written = atomic_write_bytes(target, data)
        self.assertTrue(written.exists())
        with open(written, "rb") as f:
            self.assertEqual(f.read(), data)

    def test_json_safe_read_write(self) -> None:
        target = self.tmppath / "data.json"
        data = {"preset": "flower_of_life", "rings": 3, "radius": 45.5}
        write_json_safe(target, data)
        loaded = read_json_safe(target)
        self.assertEqual(loaded, data)

    def test_safe_delete(self) -> None:
        target = self.tmppath / "to_delete.txt"
        target.write_text("temporary")
        self.assertTrue(safe_delete(target))
        self.assertFalse(target.exists())
        # Safe delete on non-existent file should return False without raising
        self.assertFalse(safe_delete(target))


class TestGeometryModels(unittest.TestCase):
    """Test AST primitives and transformations."""

    def test_point2d_math(self) -> None:
        p1 = Point2D(0.0, 0.0)
        p2 = Point2D(3.0, 4.0)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0)

        p_rot = Point2D(1.0, 0.0).rotate(math.pi / 2.0)
        self.assertAlmostEqual(p_rot.x, 0.0, places=5)
        self.assertAlmostEqual(p_rot.y, 1.0, places=5)

        p_trans = p1.translate(10.0, -5.0)
        self.assertEqual((p_trans.x, p_trans.y), (10.0, -5.0))

    def test_point3d_rotations_and_projection(self) -> None:
        p3 = Point3D(0.0, 10.0, 0.0)
        p3_rot = p3.rotate_x(math.pi / 2.0)
        self.assertAlmostEqual(p3_rot.y, 0.0, places=5)
        self.assertAlmostEqual(p3_rot.z, 10.0, places=5)

        p2_proj = p3.project_2d(orthographic=True)
        self.assertEqual((p2_proj.x, p2_proj.y), (0.0, 10.0))

    def test_geometry_ast_operations(self) -> None:
        ast = GeometryAST(title="Test AST")
        ast.add_circle(Point2D(0.0, 0.0), 50.0)
        ast.add_line(Point2D(-50.0, 0.0), Point2D(50.0, 0.0))
        ast.add_arc(Point2D(0.0, 0.0), 30.0, 0.0, math.pi)
        ast.add_polygon([Point2D(-10, -10), Point2D(10, -10), Point2D(0, 10)])

        bb = ast.bounds()
        self.assertAlmostEqual(bb.min_x, -50.0, places=3)
        self.assertAlmostEqual(bb.max_x, 50.0, places=3)
        self.assertAlmostEqual(bb.min_y, -50.0, places=3)
        self.assertAlmostEqual(bb.max_y, 50.0, places=3)
        self.assertAlmostEqual(bb.width, 100.0, places=3)
        self.assertAlmostEqual(bb.height, 100.0, places=3)

        # Test Serialization
        serialized = ast.to_dict()
        restored = GeometryAST.from_dict(serialized)
        self.assertEqual(len(restored.circles), 1)
        self.assertEqual(len(restored.lines), 1)
        self.assertEqual(len(restored.arcs), 1)
        self.assertEqual(len(restored.polygons), 1)

        # Test Fit to Box
        ast.fit_to_box(target_width=500.0, target_height=500.0, padding=50.0)
        new_bb = ast.bounds()
        self.assertAlmostEqual(new_bb.center.x, 250.0, places=2)
        self.assertAlmostEqual(new_bb.center.y, 250.0, places=2)


class TestGenerators(unittest.TestCase):
    """Test all parametric sacred geometry and crop circle generators."""

    def test_flower_of_life_family(self) -> None:
        seed = generate_seed_of_life(radius=50.0)
        self.assertEqual(len(seed.circles), 8)  # 1 center + 6 petals + 1 outer

        flower = generate_flower_of_life(radius=40.0, rings=3, outer_rings=True)
        self.assertGreater(len(flower.circles), 19)

        egg = generate_egg_of_life(radius=50.0)
        self.assertEqual(len(egg.circles), 8)

        fruit = generate_fruit_of_life(radius=30.0)
        self.assertEqual(len(fruit.circles), 13)

        tree = generate_tree_of_life(scale=100.0, overlay_flower=False)
        self.assertEqual(len(tree.lines), 22)  # 22 connecting paths
        self.assertEqual(len(tree.circles), 20)  # 10 double-ring Sephiroth nodes

    def test_metatrons_cube_and_platonic_solids(self) -> None:
        metatron = generate_metatrons_cube(radius=35.0)
        # 78 lines + 6 hexagon highlight lines + 3 Y-spokes = 87 lines
        self.assertGreaterEqual(len(metatron.lines), 78)
        self.assertEqual(len(metatron.circles), 14)  # 13 nodal centers + 1 outer ring Sephiroth nodes

        for solid in ["tetrahedron", "cube", "octahedron", "icosahedron", "dodecahedron"]:
            ast_solid = generate_platonic_solid_projection(solid_type=solid, size=100.0)
            self.assertGreater(len(ast_solid.lines), 0)
            self.assertGreater(len(ast_solid.points3d), 0)

    def test_fibonacci_and_golden_ratio(self) -> None:
        fibs = generate_fibonacci_sequence(8)
        self.assertEqual(fibs, [1, 1, 2, 3, 5, 8, 13, 21])

        rects = generate_golden_rectangles(iterations=7)
        self.assertEqual(len(rects.polygons), 7)
        self.assertEqual(len(rects.arcs), 7)

        spiral = generate_golden_spiral(iterations=5.0)
        self.assertGreater(len(spiral.lines), 100)

        phyllotaxis = generate_phyllotaxis(num_points=100, connect_spirals=True)
        self.assertEqual(len(phyllotaxis.circles), 100)
        self.assertGreater(len(phyllotaxis.lines), 50)

        tri_spiral = generate_golden_triangle_spiral(iterations=6)
        self.assertEqual(len(tri_spiral.polygons), 6)

    def test_sri_yantra(self) -> None:
        sri = generate_sri_yantra(size=200.0, show_petals=True, show_bhupura=True)
        self.assertGreaterEqual(len(sri.polygons), 9 + 8 + 16 + 3)  # 9 triangles + 24 petals + 3 bhupura
        self.assertGreater(len(sri.circles), 0)

    def test_crop_circles(self) -> None:
        milk_hill = generate_milk_hill_glyph(scale=200.0)
        self.assertEqual(len(milk_hill.circles), 409)  # 1 + 6 * 68 = 409 circles

        julia = generate_julia_set_glyph(scale=200.0, num_circles=151)
        self.assertEqual(len(julia.circles), 151)

        barbury = generate_barbury_castle_glyph(scale=180.0)
        self.assertGreater(len(barbury.lines), 10)
        self.assertGreater(len(barbury.circles), 5)

        chilbolton = generate_chilbolton_binary_glyph(scale=200.0)
        self.assertGreater(len(chilbolton.polygons), 50)

        triskele = generate_triskele_glyph(scale=190.0)
        self.assertGreater(len(triskele.lines), 50)

    def test_merkaba_and_torus(self) -> None:
        merkaba = generate_merkaba(radius=100.0)
        self.assertEqual(len(merkaba.lines), 27)  # 6 + 6 tetra + 12 core octahedron + 3 axes

        torus = generate_torus(major_radius=100.0, minor_radius=40.0, u_steps=16, v_steps=8)
        self.assertGreater(len(torus.lines), 100)

        trefoil = generate_torus_knot(p=2, q=3, major_radius=100.0, minor_radius=40.0, num_points=100)
        self.assertEqual(len(trefoil.lines), 100)

        vesica = generate_vesica_piscis(radius=80.0, num_rays=12)
        self.assertEqual(len(vesica.circles), 7)  # 2 * 3 nested + 1 boundary


class TestExporters(unittest.TestCase):
    """Test multi-format export to SVG, DXF, and OBJ."""

    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tmppath = Path(self.tmpdir.name)
        self.ast = generate_flower_of_life(radius=40.0, rings=3)

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def test_svg_export(self) -> None:
        svg_file = self.tmppath / "flower.svg"
        svg_str = export_svg(self.ast, file_path=svg_file, theme="dark_gold", glow=True)
        self.assertTrue(svg_file.exists())
        self.assertIn("<svg", svg_str)
        self.assertIn("sacred_glow", svg_str)
        self.assertIn("</svg>", svg_str)

    def test_dxf_export(self) -> None:
        dxf_file = self.tmppath / "flower.dxf"
        dxf_str = export_dxf(self.ast, file_path=dxf_file)
        self.assertTrue(dxf_file.exists())
        self.assertIn("SECTION", dxf_str)
        self.assertIn("HEADER", dxf_str)
        self.assertIn("TABLES", dxf_str)
        self.assertIn("ENTITIES", dxf_str)
        self.assertIn("CIRCLE", dxf_str)
        self.assertIn("EOF", dxf_str)

    def test_obj_export(self) -> None:
        obj_file = self.tmppath / "flower.obj"
        obj_str = export_obj(self.ast, file_path=obj_file, base_type="cylinder")
        self.assertTrue(obj_file.exists())
        mtl_file = self.tmppath / "flower.mtl"
        self.assertTrue(mtl_file.exists())
        self.assertIn("v ", obj_str)
        self.assertIn("vn ", obj_str)
        self.assertIn("f ", obj_str)


class TestCatalog(unittest.TestCase):
    """Test Preset Registry and Dispatcher."""

    def test_catalog_presets_count(self) -> None:
        self.assertGreaterEqual(len(PRESETS), 20)
        summary = get_catalog_summary()
        self.assertGreaterEqual(summary["total_presets"], 20)
        self.assertIn("Classical Sacred Geometry", summary["categories"])
        self.assertIn("Hermetic & Polyhedral", summary["categories"])
        self.assertIn("Extraterrestrial Agro-Glyphs", summary["categories"])

    def test_generate_all_presets(self) -> None:
        for preset_id in PRESETS:
            ast = generate_pattern(preset_id)
            self.assertIsInstance(ast, GeometryAST)
            stats = ast.stats()
            self.assertGreater(stats["total_primitives"], 0, f"Preset '{preset_id}' generated 0 primitives!")


if __name__ == "__main__":
    unittest.main()
