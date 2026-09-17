"""Pytest configuration and shared fixtures for ufo-sacred-geometry test suite."""

import os
import sys
from pathlib import Path
import pytest

# Ensure src/ directory is first in sys.path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import ufo_sacred_geometry
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


@pytest.fixture
def sample_point_2d() -> Point2D:
    return Point2D(x=10.0, y=20.0)


@pytest.fixture
def sample_point_3d() -> Point3D:
    return Point3D(x=10.0, y=20.0, z=30.0)


@pytest.fixture
def sample_line_segment() -> LineSegment:
    return LineSegment(
        start=Point2D(0.0, 0.0),
        end=Point2D(100.0, 100.0),
        stroke_width=1.5,
        color="#ffd700",
    )


@pytest.fixture
def sample_circle() -> Circle:
    return Circle(
        center=Point2D(0.0, 0.0),
        radius=50.0,
        stroke_width=1.2,
        color="#4285f4",
    )


@pytest.fixture
def sample_polygon() -> Polygon:
    return Polygon(
        points=[Point2D(0.0, 0.0), Point2D(50.0, 0.0), Point2D(25.0, 43.3)],
        stroke_width=1.0,
        color="#00ff66",
        closed=True,
    )


@pytest.fixture
def sample_ast(sample_circle, sample_line_segment, sample_polygon) -> GeometryAST:
    ast = GeometryAST(
        title="Test Geometry AST",
        description="Geometry AST created for test fixtures",
        parameters={"radius": 50.0, "iterations": 3},
        tags=["test", "sacred_geometry"],
    )
    ast.circles.append(sample_circle)
    ast.lines.append(sample_line_segment)
    ast.polygons.append(sample_polygon)
    return ast


@pytest.fixture
def temp_output_dir(tmp_path) -> Path:
    out = tmp_path / "sacred_geometry_out"
    out.mkdir(parents=True, exist_ok=True)
    return out
