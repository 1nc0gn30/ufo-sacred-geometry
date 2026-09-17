"""Unit tests for models.py geometric AST data structures and primitives."""

import math
import pytest

from ufo_sacred_geometry.models import (
    Point2D,
    Point3D,
    LineSegment,
    Circle,
    Arc,
    Polygon,
    Spline,
    BoundingBox,
    GeometryAST,
    PatternPreset,
)


def test_point_2d_operations():
    """Verify Point2D transformations and math calculations."""
    p1 = Point2D(0.0, 0.0)
    p2 = Point2D(3.0, 4.0)

    # Distance and angle
    assert math.isclose(p1.distance_to(p2), 5.0)
    assert math.isclose(p1.angle_to(Point2D(1.0, 0.0)), 0.0)

    # Translation
    p_trans = p2.translate(2.0, -1.0)
    assert p_trans.x == 5.0 and p_trans.y == 3.0

    # Scaling
    p_scaled = p2.scale(2.0)
    assert p_scaled.x == 6.0 and p_scaled.y == 8.0

    # Rotation (90 deg counter-clockwise)
    p_rot = Point2D(1.0, 0.0).rotate(math.pi / 2.0)
    assert math.isclose(p_rot.x, 0.0, abs_tol=1e-6)
    assert math.isclose(p_rot.y, 1.0, abs_tol=1e-6)

    # Polar creation
    p_polar = Point2D.from_polar(10.0, math.pi / 4.0)
    assert math.isclose(p_polar.x, 10.0 * math.cos(math.pi / 4.0))
    assert math.isclose(p_polar.y, 10.0 * math.sin(math.pi / 4.0))

    # Serialization
    d = p2.to_dict()
    assert d == {"x": 3.0, "y": 4.0}
    p_restored = Point2D.from_dict(d)
    assert p_restored == p2


def test_point_3d_operations():
    """Verify Point3D 3D transformations and 2D projections."""
    p3 = Point3D(10.0, 20.0, 30.0)

    assert math.isclose(p3.distance_to(Point3D(10.0, 20.0, 30.0)), 0.0)
    assert math.isclose(p3.distance_to(Point3D(13.0, 24.0, 30.0)), 5.0)

    # Rotations
    p_rx = p3.rotate_x(math.pi / 2.0)
    assert math.isclose(p_rx.x, 10.0)
    assert math.isclose(p_rx.y, -30.0, abs_tol=1e-6)
    assert math.isclose(p_rx.z, 20.0, abs_tol=1e-6)

    # 2D projection
    p2_proj = p3.project_2d(orthographic=True)
    assert p2_proj.x == 10.0 and p2_proj.y == 20.0

    p2_persp = p3.project_2d(focal_length=500.0, camera_z=600.0)
    assert isinstance(p2_persp, Point2D)

    # Dict roundtrip
    d = p3.to_dict()
    assert Point3D.from_dict(d) == p3


def test_line_segment():
    """Verify LineSegment properties and transformations."""
    line = LineSegment(start=Point2D(0.0, 0.0), end=Point2D(6.0, 8.0), stroke_width=2.0)
    assert math.isclose(line.length, 10.0)
    assert line.midpoint.x == 3.0 and line.midpoint.y == 4.0

    line_t = line.translate(2.0, 3.0)
    assert line_t.start.x == 2.0 and line_t.end.x == 8.0

    line_s = line.scale(2.0)
    assert math.isclose(line_s.length, 20.0)

    # Dict serialization
    d = line.to_dict()
    restored = LineSegment.from_dict(d)
    assert restored.start == line.start and restored.end == line.end


def test_circle_geometry():
    """Verify Circle properties, point on circumference, and scaling."""
    c = Circle(center=Point2D(0.0, 0.0), radius=10.0)
    assert math.isclose(c.area, math.pi * 100.0)
    assert math.isclose(c.circumference, 2.0 * math.pi * 10.0)

    p_circ = c.point_at_angle(0.0)
    assert p_circ.x == 10.0 and p_circ.y == 0.0

    c_scaled = c.scale(3.0)
    assert c_scaled.radius == 30.0

    d = c.to_dict()
    restored = Circle.from_dict(d)
    assert restored.radius == c.radius and restored.center == c.center


def test_arc_geometry():
    """Verify Arc start, end, span angles, and serialization."""
    arc = Arc(
        center=Point2D(0.0, 0.0),
        radius=20.0,
        start_angle=0.0,
        end_angle=math.pi / 2.0,
    )
    assert math.isclose(arc.start_point.x, 20.0)
    assert math.isclose(arc.start_point.y, 0.0)
    assert math.isclose(arc.end_point.x, 0.0, abs_tol=1e-6)
    assert math.isclose(arc.end_point.y, 20.0)
    assert math.isclose(arc.span_angle, math.pi / 2.0)

    d = arc.to_dict()
    restored = Arc.from_dict(d)
    assert restored.radius == arc.radius


def test_polygon_geometry():
    """Verify Polygon centroid, scaling, and dictionary roundtrip."""
    pts = [Point2D(0.0, 0.0), Point2D(10.0, 0.0), Point2D(10.0, 10.0), Point2D(0.0, 10.0)]
    poly = Polygon(points=pts, closed=True)

    assert poly.centroid.x == 5.0 and poly.centroid.y == 5.0

    poly_t = poly.translate(5.0, 5.0)
    assert poly_t.centroid.x == 10.0 and poly_t.centroid.y == 10.0

    d = poly.to_dict()
    restored = Polygon.from_dict(d)
    assert len(restored.points) == 4
    assert restored.closed is True


def test_spline_sampling():
    """Verify Spline sample points via Catmull-Rom interpolation."""
    ctrl_pts = [Point2D(0.0, 0.0), Point2D(20.0, 50.0), Point2D(40.0, 0.0), Point2D(60.0, 50.0)]
    spline = Spline(control_points=ctrl_pts, closed=False)

    sampled = spline.sample_points(samples_per_segment=8)
    assert len(sampled) > len(ctrl_pts)
    assert isinstance(sampled[0], Point2D)

    d = spline.to_dict()
    restored = Spline.from_dict(d)
    assert len(restored.control_points) == 4


def test_bounding_box():
    """Verify BoundingBox calculations."""
    bb = BoundingBox(min_x=-50.0, min_y=-100.0, max_x=50.0, max_y=100.0)
    assert bb.width == 100.0
    assert bb.height == 200.0
    assert bb.center.x == 0.0 and bb.center.y == 0.0
    assert bb.to_tuple() == (-50.0, -100.0, 50.0, 100.0, 100.0, 200.0)


def test_geometry_ast_full_lifecycle():
    """Verify GeometryAST primitive addition, bounding computation, transformations, and serialization."""
    ast = GeometryAST(title="Metatron Test")

    c = ast.add_circle(Point2D(0.0, 0.0), 50.0)
    l = ast.add_line(Point2D(-50.0, 0.0), Point2D(50.0, 0.0))
    p = ast.add_polygon([Point2D(0.0, 50.0), Point2D(-43.3, -25.0), Point2D(43.3, -25.0)])

    # Check bounds
    bb = ast.bounds()
    assert bb.min_x <= -50.0
    assert bb.max_x >= 50.0
    assert bb.min_y <= -50.0
    assert bb.max_y >= 50.0

    # Transformations
    ast.translate(10.0, 20.0)
    bb_trans = ast.bounds()
    assert bb_trans.center.x == 10.0
    assert bb_trans.center.y == 20.0

    # Fit to box
    ast.fit_to_box(target_width=500.0, target_height=500.0, padding=25.0)
    bb_fitted = ast.bounds()
    assert bb_fitted.width <= 450.0
    assert bb_fitted.height <= 450.0

    # Stats
    st = ast.stats()
    assert st["circles"] == 1
    assert st["lines"] == 1
    assert st["polygons"] == 1
    assert st["total_primitives"] == 3

    # JSON Roundtrip
    json_str = ast.to_json()
    assert isinstance(json_str, str)
    restored_ast = GeometryAST.from_json(json_str)
    assert len(restored_ast.circles) == 1
    assert len(restored_ast.lines) == 1
    assert len(restored_ast.polygons) == 1
    assert restored_ast.title == "Metatron Test"


def test_pattern_preset_dataclass():
    """Verify PatternPreset serialization and deserialization."""
    preset = PatternPreset(
        id="sri_yantra_master",
        title="Sri Yantra Master Diagram",
        category="sacred",
        description="9 interlocking triangles creating 43 sub-triangles.",
        default_parameters={"scale": 150.0, "petals": 16},
        tags=["sri_yantra", "vedic"],
        difficulty="master",
    )

    d = preset.to_dict()
    assert d["id"] == "sri_yantra_master"
    assert d["difficulty"] == "master"

    restored = PatternPreset.from_dict(d)
    assert restored.id == preset.id
    assert restored.default_parameters == preset.default_parameters
