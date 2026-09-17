"""Sacred Geometry Pattern Catalog & Generator Registry.

Contains 20+ authentic curated sacred geometry presets across 5 distinct domains:
1. Classical Sacred Geometry (Seed, Flower, Fruit, Egg, Tree of Life)
2. Hermetic & Polyhedral (Metatron's Cube, 5 Platonic Solids, Merkaba)
3. Golden Ratio & Natural Harmonics (Golden Spiral, Whirling Squares, Phyllotaxis, Sublime Triangle)
4. Vedic & Mystical Yantras (Sri Yantra, Vesica Piscis)
5. Extraterrestrial Agro-Glyphs & Vortex Dynamics (Milk Hill, Julia Set, Barbury Castle, Chilbolton, Torus)
100% Python Standard Library.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from .generators.crop_circle import (
    generate_barbury_castle_glyph,
    generate_chilbolton_binary_glyph,
    generate_crop_circle,
    generate_julia_set_glyph,
    generate_milk_hill_glyph,
    generate_triskele_glyph,
)
from .generators.fibonacci_spiral import (
    generate_golden_rectangles,
    generate_golden_spiral,
    generate_golden_triangle_spiral,
    generate_phyllotaxis,
)
from .generators.flower_of_life import (
    generate_egg_of_life,
    generate_flower_of_life,
    generate_fruit_of_life,
    generate_seed_of_life,
    generate_tree_of_life,
)
from .generators.merkaba_torus import (
    generate_merkaba,
    generate_torus,
    generate_torus_knot,
    generate_vesica_piscis,
)
from .generators.metatrons_cube import (
    generate_metatrons_cube,
    generate_platonic_solid_projection,
)
from .generators.sri_yantra import generate_sri_yantra
from .models import GeometryAST, PatternPreset

# Complete Preset Registry
_PRESETS_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------
    # 1. CLASSICAL SACRED GEOMETRY
    # -------------------------------------------------------------
    {
        "id": "seed_of_life",
        "title": "Seed of Life",
        "category": "Classical Sacred Geometry",
        "description": "7 intersecting circles representing the genesis vortex and the primary hexagonal template of creation.",
        "difficulty": "beginner",
        "historical_context": "Found in ancient Egyptian temples (Abydos Osirion), Assyrian palaces, and Kabbalistic manuscripts.",
        "tags": ["seed_of_life", "creation", "hexagonal", "classical", "circles"],
        "default_parameters": {
            "radius": 60.0,
            "stroke_width": 1.5,
            "color": "#ffd700",
            "outer_circle": True,
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 300},
    },
    {
        "id": "flower_of_life",
        "title": "Flower of Life",
        "category": "Classical Sacred Geometry",
        "description": "19 concentric interlocking circles forming 90 overlapping flower petals framed by double outer rings.",
        "difficulty": "medium",
        "historical_context": "Carved into the granite pillars of the Temple of Osiris at Abydos, Egypt (circa 4000 BCE) and studied extensively by Leonardo da Vinci.",
        "tags": ["flower_of_life", "rosette", "platonic_matrix", "egyptian", "ancient"],
        "default_parameters": {
            "radius": 45.0,
            "rings": 3,
            "outer_rings": True,
            "completion_arcs": True,
            "stroke_width": 1.2,
            "color": "#ffd700",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 400},
    },
    {
        "id": "fruit_of_life",
        "title": "Fruit of Life",
        "category": "Classical Sacred Geometry",
        "description": "13 isolated circles derived from completing the outer rings of the Flower of Life, forming the blueprint of Metatron's Cube.",
        "difficulty": "medium",
        "historical_context": "The hidden octave of creation containing 13 informational systems governing all dimensional planes.",
        "tags": ["fruit_of_life", "metatron", "octave", "blueprint"],
        "default_parameters": {
            "radius": 32.0,
            "stroke_width": 1.5,
            "color": "#ff007f",
            "connecting_lines": True,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 380},
    },
    {
        "id": "egg_of_life",
        "title": "Egg of Life",
        "category": "Classical Sacred Geometry",
        "description": "8-cell embryonic morula formation describing the morphogenetic field of all cellular biological life.",
        "difficulty": "beginner",
        "historical_context": "Reflects the third stage of embryonic division (morula) where 8 cells form a star-tetrahedral cluster.",
        "tags": ["egg_of_life", "embryo", "biology", "morphogenesis"],
        "default_parameters": {
            "radius": 55.0,
            "stroke_width": 1.5,
            "color": "#00f0ff",
        },
        "preview_hints": {"recommended_theme": "cosmic_purple", "viewbox_size": 350},
    },
    {
        "id": "tree_of_life",
        "title": "Tree of Life (Etz Chaim)",
        "category": "Classical Sacred Geometry",
        "description": "10 Divine Sephiroth emanations connected by 22 sacred paths, perfectly overlaid on the Flower of Life grid.",
        "difficulty": "advanced",
        "historical_context": "Central glyph of Kabbalistic cosmology and Hermetic Qabalah, modeling the descent of the divine spark into material existence.",
        "tags": ["tree_of_life", "kabbalah", "sephiroth", "paths", "hermetic"],
        "default_parameters": {
            "scale": 110.0,
            "node_radius": 14.0,
            "overlay_flower": True,
            "stroke_width": 1.4,
            "path_color": "#00f0ff",
            "node_color": "#ffd700",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 500},
    },
    # -------------------------------------------------------------
    # 2. HERMETIC & POLYHEDRAL
    # -------------------------------------------------------------
    {
        "id": "metatrons_cube",
        "title": "Metatron's Cube",
        "category": "Hermetic & Polyhedral",
        "description": "13 Fruit of Life nodal centers connected by 78 line segments, unlocking all 5 3D Platonic Solids.",
        "difficulty": "advanced",
        "historical_context": "Named after the Archangel Metatron; described in early Jewish mysticism and Renaissance sacred geometry texts as the master geometric key.",
        "tags": ["metatron", "archangel", "platonic_solids", "cuboctahedron", "78_lines"],
        "default_parameters": {
            "radius": 35.0,
            "include_circles": True,
            "stroke_width": 1.1,
            "line_color": "#00ffff",
            "circle_color": "#ffd700",
            "highlight_cube": True,
            "outer_boundary": True,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 450},
    },
    {
        "id": "platonic_tetrahedron",
        "title": "Platonic Solid: Tetrahedron",
        "category": "Hermetic & Polyhedral",
        "description": "Regular 4-sided polyhedron representing the Element of Fire, solar energy, and spontaneous creation.",
        "difficulty": "beginner",
        "historical_context": "Plato's Timaeus (360 BCE): Associated with Fire due to its sharpest points and smallest volume-to-surface ratio.",
        "tags": ["platonic_solid", "tetrahedron", "fire", "polyhedra", "3d"],
        "default_parameters": {
            "size": 130.0,
            "rot_x": 0.55,
            "rot_y": 0.75,
            "rot_z": 0.0,
            "stroke_width": 1.6,
            "color": "#ff3b30",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 300},
    },
    {
        "id": "platonic_cube",
        "title": "Platonic Solid: Hexahedron (Cube)",
        "category": "Hermetic & Polyhedral",
        "description": "Regular 6-sided hexahedron representing the Element of Earth, stability, crystalline matter, and physical manifestation.",
        "difficulty": "beginner",
        "historical_context": "Plato's Timaeus: Associated with Earth due to its stability and square faces.",
        "tags": ["platonic_solid", "cube", "hexahedron", "earth", "polyhedra", "3d"],
        "default_parameters": {
            "size": 120.0,
            "rot_x": 0.55,
            "rot_y": 0.75,
            "rot_z": 0.0,
            "stroke_width": 1.6,
            "color": "#34c759",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 300},
    },
    {
        "id": "platonic_octahedron",
        "title": "Platonic Solid: Octahedron",
        "category": "Hermetic & Polyhedral",
        "description": "Regular 8-sided dual of the cube representing the Element of Air, mental clarity, and communication.",
        "difficulty": "medium",
        "historical_context": "Plato's Timaeus: Associated with Air due to its frictionless rotatability and balance.",
        "tags": ["platonic_solid", "octahedron", "air", "polyhedra", "3d"],
        "default_parameters": {
            "size": 130.0,
            "rot_x": 0.55,
            "rot_y": 0.75,
            "rot_z": 0.0,
            "stroke_width": 1.6,
            "color": "#ffd700",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 300},
    },
    {
        "id": "platonic_icosahedron",
        "title": "Platonic Solid: Icosahedron",
        "category": "Hermetic & Polyhedral",
        "description": "Regular 20-sided polyhedron constructed from Golden Ratio rectangles representing the Element of Water and fluidity.",
        "difficulty": "advanced",
        "historical_context": "Plato's Timaeus: Associated with Water due to its smooth spherical approximation and 20 triangular faces.",
        "tags": ["platonic_solid", "icosahedron", "water", "golden_ratio", "polyhedra", "3d"],
        "default_parameters": {
            "size": 140.0,
            "rot_x": 0.55,
            "rot_y": 0.75,
            "rot_z": 0.0,
            "stroke_width": 1.5,
            "color": "#00f0ff",
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 320},
    },
    {
        "id": "platonic_dodecahedron",
        "title": "Platonic Solid: Dodecahedron",
        "category": "Hermetic & Polyhedral",
        "description": "Regular 12-sided pentagonal polyhedron representing Ether, Quintessence, the Cosmos, and universal consciousness.",
        "difficulty": "master",
        "historical_context": "Plato's Timaeus: 'There remained a fifth construction, which God used for embroidering the constellations on the whole heaven.'",
        "tags": ["platonic_solid", "dodecahedron", "ether", "quintessence", "cosmos", "pentagon", "3d"],
        "default_parameters": {
            "size": 140.0,
            "rot_x": 0.55,
            "rot_y": 0.75,
            "rot_z": 0.0,
            "stroke_width": 1.5,
            "color": "#af52de",
        },
        "preview_hints": {"recommended_theme": "cosmic_purple", "viewbox_size": 320},
    },
    {
        "id": "merkaba_star",
        "title": "Merkaba Lightbody (Stella Octangula)",
        "category": "Hermetic & Polyhedral",
        "description": "3D Star Tetrahedron composed of two interpenetrating counter-rotating tetrahedra creating a multidimensional light vehicle.",
        "difficulty": "advanced",
        "historical_context": "Ancient Egyptian 'Mer-Ka-Ba' (Light-Spirit-Body); studied by Johannes Kepler in 1619 as the Stella Octangula.",
        "tags": ["merkaba", "star_tetrahedron", "stella_octangula", "lightbody", "3d"],
        "default_parameters": {
            "radius": 120.0,
            "rot_x": 0.45,
            "rot_y": 0.65,
            "rot_z": 0.0,
            "stroke_width": 1.4,
            "male_tetra_color": "#00f0ff",
            "female_tetra_color": "#ff007f",
            "show_spheres": True,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 350},
    },
    # -------------------------------------------------------------
    # 3. GOLDEN RATIO & NATURAL HARMONICS
    # -------------------------------------------------------------
    {
        "id": "golden_rectangles",
        "title": "Fibonacci Whirling Squares",
        "category": "Golden Ratio & Natural Harmonics",
        "description": "Decomposition of the Golden Rectangle into nested Fibonacci squares [1,1,2,3,5,8,13,21] with continuous quarter-circle arcs.",
        "difficulty": "beginner",
        "historical_context": "Discovered by Leonardo Fibonacci of Pisa in Liber Abaci (1202) and foundational to Euclidean geometry.",
        "tags": ["fibonacci", "golden_ratio", "whirling_squares", "spiral", "phi"],
        "default_parameters": {
            "iterations": 8,
            "initial_size": 12.0,
            "show_arcs": True,
            "show_rectangles": True,
            "show_diagonals": True,
            "stroke_width": 1.2,
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 420},
    },
    {
        "id": "golden_spiral",
        "title": "Logarithmic Golden Spiral",
        "category": "Golden Ratio & Natural Harmonics",
        "description": "Continuous equiangular logarithmic spiral expanding at the precise Golden Ratio factor phi per quadrant.",
        "difficulty": "medium",
        "historical_context": "Described by René Descartes (1638) and praised by Jakob Bernoulli as 'Spira Mirabilis' ('the marvelous spiral').",
        "tags": ["golden_spiral", "logarithmic", "equiangular", "vortex", "phi"],
        "default_parameters": {
            "iterations": 6.0,
            "scale": 8.0,
            "num_arms": 1,
            "stroke_width": 1.6,
            "color": "#ffd700",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 450},
    },
    {
        "id": "sunflower_phyllotaxis",
        "title": "Sunflower Vogel Phyllotaxis",
        "category": "Golden Ratio & Natural Harmonics",
        "description": "Vogel's mathematical disc model with Golden Angle 137.507764° generating clockwise and counter-clockwise parastichy spirals.",
        "difficulty": "advanced",
        "historical_context": "Formulated by Helmut Vogel in 1979 to model the optimal mathematical packing of sunflower seeds and botanical seed heads.",
        "tags": ["phyllotaxis", "vogel", "sunflower", "golden_angle", "parastichy", "botany"],
        "default_parameters": {
            "num_points": 350,
            "spread": 4.5,
            "point_radius": 2.8,
            "connect_spirals": True,
            "parastichy_p": 21,
            "parastichy_q": 34,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 450},
    },
    {
        "id": "golden_triangle_spiral",
        "title": "Golden Triangle Spiral (Sublime Triangle)",
        "category": "Golden Ratio & Natural Harmonics",
        "description": "Recursive self-similar Golden Triangle (72°-72°-36°) subdivision generating logarithmic spiral vertices.",
        "difficulty": "medium",
        "historical_context": "Known to Pythagorean mathematicians as the basis of the Pentagram and Kepler's sublime triangle.",
        "tags": ["golden_triangle", "sublime_triangle", "pentagram", "pythagorean"],
        "default_parameters": {
            "iterations": 9,
            "initial_size": 240.0,
            "stroke_width": 1.2,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 400},
    },
    # -------------------------------------------------------------
    # 4. VEDIC & MYSTICAL YANTRAS
    # -------------------------------------------------------------
    {
        "id": "sri_yantra",
        "title": "Sri Yantra (Sri Chakra)",
        "category": "Vedic & Mystical Yantras",
        "description": "Master Vedic cosmogram: 9 interlocking Shiva/Shakti triangles, 43 sub-triangles, 24 lotus petals, and 4-gate Bhupura.",
        "difficulty": "master",
        "historical_context": "Vedic sacred geometry described in the Saundarya Lahari and Tantraraja Tantra (over 2500 years old).",
        "tags": ["sri_yantra", "vedic", "tantra", "mandala", "chakra", "sacred_cosmology"],
        "default_parameters": {
            "size": 180.0,
            "show_petals": True,
            "show_bhupura": True,
            "show_bindu": True,
            "stroke_width": 1.0,
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 460},
    },
    {
        "id": "vesica_piscis",
        "title": "Vesica Piscis & Mandorla Portal",
        "category": "Vedic & Mystical Yantras",
        "description": "Intersection of two identical circles encoding the square root of 3, with nested harmonic mandorlas and radiating sunburst rays.",
        "difficulty": "beginner",
        "historical_context": "Appears in Sacred Christian art, Gothic cathedral portals (Chartres), and ancient Pythagorean sacred arithmetic.",
        "tags": ["vesica_piscis", "mandorla", "sqrt3", "portal", "creation"],
        "default_parameters": {
            "radius": 80.0,
            "num_rays": 24,
            "nested_depth": 3,
            "stroke_width": 1.3,
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 380},
    },
    # -------------------------------------------------------------
    # 5. EXTRATERRESTRIAL AGRO-GLYPHS & VORTEX DYNAMICS
    # -------------------------------------------------------------
    {
        "id": "crop_circle_milk_hill",
        "title": "Milk Hill 409-Circle Crop Circle (2001)",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "Colossal 6-arm triple logarithmic spiral formation discovered at Milk Hill, Wiltshire (2001) comprising 409 circles.",
        "difficulty": "master",
        "historical_context": "Discovered on August 12, 2001 in Wiltshire, UK during heavy mist; spanning over 800 feet across.",
        "tags": ["crop_circle", "milk_hill", "409_circles", "ufo", "alien", "agro_glyph"],
        "default_parameters": {
            "scale": 220.0,
            "stroke_width": 0.8,
            "glyph_color": "#39ff14",
            "fill_circles": True,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 520},
    },
    {
        "id": "crop_circle_julia_set",
        "title": "Stonehenge Julia Set Crop Circle (1996)",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "151-circle Julia Set fractal agro-glyph that materialized opposite Stonehenge in broad daylight in July 1996.",
        "difficulty": "advanced",
        "historical_context": "Formed on July 7, 1996 within a 45-minute window verified by pilots flying over Stonehenge.",
        "tags": ["crop_circle", "julia_set", "stonehenge", "fractal", "spiral"],
        "default_parameters": {
            "scale": 200.0,
            "num_circles": 151,
            "stroke_width": 1.0,
            "color": "#00f0ff",
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 480},
    },
    {
        "id": "crop_circle_barbury_castle",
        "title": "Barbury Castle Tetrahedron Glyph (1991)",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "Historic 3D tetrahedron flattened glyph with 3 multi-ring corner spheres and ratcheted sunburst center.",
        "difficulty": "advanced",
        "historical_context": "Discovered near Wroughton, Wiltshire on July 17, 1991; decoded by physicists as a 3D tetrahedral projection.",
        "tags": ["crop_circle", "barbury_castle", "tetrahedron", "sunburst", "agro_glyph"],
        "default_parameters": {
            "scale": 180.0,
            "stroke_width": 1.2,
            "color": "#ffd700",
        },
        "preview_hints": {"recommended_theme": "dark_gold", "viewbox_size": 440},
    },
    {
        "id": "crop_circle_chilbolton",
        "title": "Chilbolton Alien Binary Telemetry (2001)",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "The binary response to Carl Sagan's 1974 Arecibo message discovered in wheat fields next to Chilbolton Radio Observatory.",
        "difficulty": "master",
        "historical_context": "Appeared in August 2001 featuring modified DNA nucleotides, alien physiology, and crop-circle transmitter antenna.",
        "tags": ["crop_circle", "chilbolton", "arecibo", "binary", "alien_contact", "seti"],
        "default_parameters": {
            "scale": 200.0,
            "stroke_width": 1.0,
            "color": "#39ff14",
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 480},
    },
    {
        "id": "crop_circle_triskele",
        "title": "Windmill Hill Triskele Vortex Glyph",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "Triple-spiral swirling vortex formation with graduating harmonic satellite circles.",
        "difficulty": "medium",
        "historical_context": "Discovered at Windmill Hill, Wiltshire in 1996; connects Celtic triskele sacred art with agro-glyph vortex science.",
        "tags": ["crop_circle", "triskele", "triple_spiral", "vortex", "celtic"],
        "default_parameters": {
            "scale": 190.0,
            "stroke_width": 1.2,
            "color": "#00f0ff",
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 440},
    },
    {
        "id": "torus_vortex",
        "title": "Toroidal Vortex Energy Field",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "Continuous 3D doughnut vortex harmonic torus field demonstrating self-sustaining zero-point energy dynamics.",
        "difficulty": "advanced",
        "historical_context": "Fundamental energy structure in Walter Russell's cosmology, Marko Rodin's vortex math, and Arthur Young's reflexology.",
        "tags": ["torus", "vortex", "zero_point", "energy_field", "rodin_coil", "3d"],
        "default_parameters": {
            "major_radius": 120.0,
            "minor_radius": 45.0,
            "u_steps": 32,
            "v_steps": 16,
            "rot_x": 0.85,
            "rot_y": 0.35,
        },
        "preview_hints": {"recommended_theme": "cosmic_purple", "viewbox_size": 420},
    },
    {
        "id": "torus_knot_trefoil",
        "title": "Parametric Torus Knot (2, 3) Trefoil",
        "category": "Extraterrestrial Agro-Glyphs",
        "description": "Parametric (2,3) topological trefoil torus knot weaving through toroidal coordinates.",
        "difficulty": "medium",
        "historical_context": "Oldest non-trivial mathematical knot; sacred triquetra in Celtic knotwork and modern string theory compactifications.",
        "tags": ["torus_knot", "trefoil", "topology", "harmonics", "3d"],
        "default_parameters": {
            "p": 2,
            "q": 3,
            "major_radius": 110.0,
            "minor_radius": 40.0,
            "num_points": 480,
            "rot_x": 0.5,
            "rot_y": 0.4,
            "stroke_width": 1.6,
        },
        "preview_hints": {"recommended_theme": "neon_ufo", "viewbox_size": 380},
    },
]

# Instantiate PatternPreset Objects
PRESETS: Dict[str, PatternPreset] = {
    p["id"]: PatternPreset.from_dict(p) for p in _PRESETS_DATA
}


# Generator Dispatcher Mapping
_GENERATOR_MAP: Dict[str, Callable[..., GeometryAST]] = {
    "seed_of_life": generate_seed_of_life,
    "flower_of_life": generate_flower_of_life,
    "fruit_of_life": generate_fruit_of_life,
    "egg_of_life": generate_egg_of_life,
    "tree_of_life": generate_tree_of_life,
    "metatrons_cube": generate_metatrons_cube,
    "platonic_tetrahedron": lambda **kw: generate_platonic_solid_projection(solid_type="tetrahedron", **kw),
    "platonic_cube": lambda **kw: generate_platonic_solid_projection(solid_type="cube", **kw),
    "platonic_octahedron": lambda **kw: generate_platonic_solid_projection(solid_type="octahedron", **kw),
    "platonic_icosahedron": lambda **kw: generate_platonic_solid_projection(solid_type="icosahedron", **kw),
    "platonic_dodecahedron": lambda **kw: generate_platonic_solid_projection(solid_type="dodecahedron", **kw),
    "merkaba_star": generate_merkaba,
    "golden_rectangles": generate_golden_rectangles,
    "golden_spiral": generate_golden_spiral,
    "sunflower_phyllotaxis": generate_phyllotaxis,
    "golden_triangle_spiral": generate_golden_triangle_spiral,
    "sri_yantra": generate_sri_yantra,
    "vesica_piscis": generate_vesica_piscis,
    "crop_circle_milk_hill": generate_milk_hill_glyph,
    "crop_circle_julia_set": generate_julia_set_glyph,
    "crop_circle_barbury_castle": generate_barbury_castle_glyph,
    "crop_circle_chilbolton": generate_chilbolton_binary_glyph,
    "crop_circle_triskele": generate_triskele_glyph,
    "torus_vortex": generate_torus,
    "torus_knot_trefoil": generate_torus_knot,
}


def get_preset(preset_id: str) -> Optional[PatternPreset]:
    """Retrieve a preset definition by its unique identifier."""
    return PRESETS.get(preset_id)


def list_presets(
    category: Optional[str] = None,
    tag: Optional[str] = None,
    difficulty: Optional[str] = None,
) -> List[PatternPreset]:
    """Query presets with optional filtering by category, tag, or difficulty."""
    results = list(PRESETS.values())
    if category and category.lower() != "all":
        cat_lower = category.lower()
        results = [p for p in results if cat_lower in p.category.lower()]
    if tag:
        tag_lower = tag.lower()
        results = [p for p in results if any(tag_lower in t.lower() for t in p.tags)]
    if difficulty:
        diff_lower = difficulty.lower()
        results = [p for p in results if p.difficulty.lower() == diff_lower]
    return results


def list_categories() -> List[str]:
    """List all unique preset categories."""
    cats = {p.category for p in PRESETS.values()}
    return sorted(cats)


def list_tags() -> List[str]:
    """List all unique tags across all presets."""
    tags = set()
    for p in PRESETS.values():
        tags.update(p.tags)
    return sorted(tags)


def generate_pattern(
    pattern_id: str,
    custom_params: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> GeometryAST:
    """Generate a Sacred Geometry AST given a preset ID and optional custom parameter overrides."""
    import inspect

    pid = pattern_id.lower().strip().replace("-", "_")
    if pid not in _GENERATOR_MAP:
        found = False
        for k in _GENERATOR_MAP.keys():
            if k == pid or pid in k or k in pid:
                pid = k
                found = True
                break
        if not found:
            raise ValueError(
                f"Unknown pattern preset ID: '{pattern_id}'. Available presets: {sorted(_GENERATOR_MAP.keys())}"
            )

    preset = PRESETS.get(pid)
    params = dict(preset.default_parameters if preset else {})
    if custom_params:
        params.update(custom_params)
    if kwargs:
        params.update(kwargs)

    generator_fn = _GENERATOR_MAP[pid]
    sig = inspect.signature(generator_fn)
    valid_params = sig.parameters

    if "radius" in params and "scale" in valid_params and "radius" not in valid_params:
        params["scale"] = params["radius"]
    if "radius" in params and "size" in valid_params and "radius" not in valid_params:
        params["size"] = params["radius"]
    if "count" in params and "num_points" in valid_params and "count" not in valid_params:
        params["num_points"] = params["count"]

    filtered_params = {k: v for k, v in params.items() if k in valid_params}
    return generator_fn(**filtered_params)


def get_catalog_summary() -> Dict[str, Any]:
    """Return high-level summary of the entire Sacred Geometry catalog."""
    return {
        "total_presets": len(PRESETS),
        "categories": {
            cat: len(list_presets(category=cat)) for cat in list_categories()
        },
        "difficulties": {
            d: len([p for p in PRESETS.values() if p.difficulty == d])
            for d in ["beginner", "medium", "advanced", "master"]
        },
        "all_preset_ids": list(PRESETS.keys()),
    }
