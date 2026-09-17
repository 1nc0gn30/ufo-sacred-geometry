"""Unit tests for sacred geometry, platonic solids, and crop circle pattern generators."""

import math
import pytest

import ufo_sacred_geometry
from ufo_sacred_geometry.generators import (
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
    generate_phyllotaxis,
    generate_platonic_solid_projection,
    generate_seed_of_life,
    generate_sri_yantra,
    generate_torus,
    generate_torus_knot,
    generate_tree_of_life,
    generate_triskele_glyph,
    generate_vesica_piscis,
    get_metatrons_13_centers,
)


def test_seed_of_life_generator():
    """Verify Seed of Life creates 7 circles + optional boundary."""
    ast = generate_seed_of_life(radius=50.0, outer_circle=True)
    assert len(ast.circles) == 8  # 1 center + 6 perimeter + 1 outer boundary
    assert ast.title == "Seed of Life"
    assert "seed_of_life" in ast.tags


def test_flower_of_life_rings():
    """Verify parametric expansion of Flower of Life rings."""
    ast_1 = generate_flower_of_life(radius=30.0, rings=1, outer_rings=False)
    assert len(ast_1.circles) == 7  # 1 + 6 = 7

    ast_2 = generate_flower_of_life(radius=30.0, rings=2, outer_rings=False)
    assert len(ast_2.circles) == 19  # 1 + 6 + 12 = 19 (Classical 19 circles)

    ast_3 = generate_flower_of_life(radius=30.0, rings=3, outer_rings=True)
    assert len(ast_3.circles) >= 37  # 1 + 6 + 12 + 18 = 37 + 2 outer boundary rings


def test_egg_of_life():
    """Verify Egg of Life generates central and 6 intersecting circles."""
    ast = generate_egg_of_life(radius=40.0)
    assert len(ast.circles) >= 7
    assert ast.title == "Egg of Life"


def test_fruit_of_life():
    """Verify Fruit of Life creates 13 nodes (0, 2R, 4R)."""
    ast = generate_fruit_of_life(radius=25.0, connecting_lines=True)
    assert len(ast.circles) == 13
    assert len(ast.lines) == 6


def test_tree_of_life():
    """Verify Kabbalistic Tree of Life generates 10 Sephiroth nodes and 22 connecting paths."""
    ast = generate_tree_of_life(scale=100.0, overlay_flower=False)
    assert len(ast.lines) == 22  # 22 Paths of Wisdom
    assert len(ast.circles) == 20  # 10 Sephiroth nodes (each with inner/outer circle)


def test_metatrons_cube():
    """Verify Metatron's Cube 13 centers, 78 connecting lines, and Platonic solid projections."""
    centers = get_metatrons_13_centers(radius=50.0)
    assert len(centers) == 13

    ast = generate_metatrons_cube(radius=50.0, include_circles=True, outer_boundary=True)
    assert len(ast.lines) == 78  # 13 * 12 / 2 = 78 complete graph connections
    assert len(ast.circles) >= 13

    # Test individual Platonic solid projections
    for solid in ["tetrahedron", "cube", "octahedron", "dodecahedron", "icosahedron"]:
        ast_solid = generate_platonic_solid_projection(solid_type=solid, size=60.0)
        assert len(ast_solid.lines) > 0
        assert solid in ast_solid.tags


def test_fibonacci_sequence_and_spiral():
    """Verify Fibonacci sequence generator and logarithmic golden spiral."""
    seq = generate_fibonacci_sequence(10)
    assert seq == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    ast_spiral = generate_golden_spiral(scale=8.0, iterations=4.0)
    assert len(ast_spiral.lines) >= 1 or len(ast_spiral.splines) >= 1

    ast_rects = generate_golden_rectangles(initial_size=10.0, iterations=7)
    assert len(ast_rects.polygons) == 7

    ast_tri = generate_golden_triangle_spiral(initial_size=150.0, iterations=6)
    assert len(ast_tri.polygons) == 6


def test_sunflower_phyllotaxis():
    """Verify Vogel sunflower disc packing with Golden Angle."""
    ast = generate_phyllotaxis(num_points=200, spread=5.0)
    assert len(ast.circles) == 200
    bb = ast.bounds()
    assert bb.width > 0.0 and bb.height > 0.0


def test_sri_yantra():
    """Verify Sri Yantra 9 interlocking triangles and lotus petals."""
    ast = generate_sri_yantra(size=150.0, show_petals=True, show_bhupura=True)
    assert len(ast.polygons) >= 9  # 9 Shiva/Shakti triangles + lotus petals + Bhupura
    assert len(ast.circles) >= 1  # Center Bindu point


def test_crop_circles():
    """Verify crop circle agro-glyph generators."""
    ast_milk = generate_milk_hill_glyph(scale=150.0)
    assert len(ast_milk.circles) == 409

    ast_julia = generate_julia_set_glyph(scale=120.0, num_circles=80)
    assert len(ast_julia.circles) == 80

    ast_barbury = generate_barbury_castle_glyph(scale=100.0)
    assert len(ast_barbury.circles) >= 3
    assert len(ast_barbury.polygons) >= 1

    ast_chilbolton = generate_chilbolton_binary_glyph(scale=100.0)
    assert len(ast_chilbolton.circles) > 0

    ast_triskele = generate_triskele_glyph(scale=100.0)
    assert len(ast_triskele.circles) >= 3

    # Generic crop circle dispatcher
    ast_generic = generate_crop_circle(glyph_type="milk_hill", scale=100.0)
    assert len(ast_generic.circles) > 0


def test_merkaba_and_torus():
    """Verify Merkaba Star Tetrahedron and Torus Vortex dynamics."""
    ast_merkaba = generate_merkaba(radius=120.0)
    assert len(ast_merkaba.lines) >= 6

    ast_torus = generate_torus(major_radius=150.0, minor_radius=60.0, u_steps=24)
    assert len(ast_torus.lines) >= 24 or len(ast_torus.circles) >= 24

    ast_knot = generate_torus_knot(p=2, q=3, major_radius=100.0, minor_radius=40.0)
    assert len(ast_knot.lines) >= 1

    ast_vesica = generate_vesica_piscis(radius=100.0)
    assert len(ast_vesica.circles) >= 2


def test_top_level_generate_pattern():
    """Verify top-level package generate_pattern works for all core presets."""
    presets_to_test = [
        "flower_of_life",
        "seed_of_life",
        "metatrons_cube",
        "golden_spiral",
        "sri_yantra",
        "merkaba_star",
        "torus_vortex",
        "sunflower_phyllotaxis",
    ]
    for p in presets_to_test:
        ast = ufo_sacred_geometry.generate_pattern(p, radius=80.0)
        assert ast is not None
        assert len(ast.circles) + len(ast.lines) + len(ast.polygons) > 0
