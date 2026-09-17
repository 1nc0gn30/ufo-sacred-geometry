"""Unified Geometric Abstract Syntax Tree (AST) & Primitives for Sacred Geometry.

Defines 2D/3D points, line segments, circles, arcs, polygons, splines,
the overarching GeometryAST container, transformations, and PatternPreset definitions.
100% Python Standard Library.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


@dataclass
class Point2D:
    """2D Cartesian Coordinate (x, y)."""

    x: float
    y: float

    def distance_to(self, other: Point2D) -> float:
        """Euclidean distance between this point and another."""
        return math.hypot(self.x - other.x, self.y - other.y)

    def angle_to(self, other: Point2D) -> float:
        """Angle in radians from this point to another point."""
        return math.atan2(other.y - self.y, other.x - self.x)

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> Point2D:
        """Rotate point around an origin (default: 0, 0) by angle in radians."""
        ox = origin.x if origin else 0.0
        oy = origin.y if origin else 0.0
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        dx = self.x - ox
        dy = self.y - oy
        return Point2D(
            x=ox + (dx * cos_a - dy * sin_a),
            y=oy + (dx * sin_a + dy * cos_a),
        )

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> Point2D:
        """Scale point relative to an origin (default: 0, 0)."""
        ox = origin.x if origin else 0.0
        oy = origin.y if origin else 0.0
        return Point2D(
            x=ox + (self.x - ox) * factor,
            y=oy + (self.y - oy) * factor,
        )

    def translate(self, dx: float, dy: float) -> Point2D:
        """Translate point by (dx, dy)."""
        return Point2D(x=self.x + dx, y=self.y + dy)

    def to_tuple(self) -> Tuple[float, float]:
        """Convert point to (x, y) tuple."""
        return (self.x, self.y)

    def to_dict(self) -> Dict[str, float]:
        """Serialize point to dictionary."""
        return {"x": round(self.x, 6), "y": round(self.y, 6)}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Point2D:
        """Deserialize point from dictionary."""
        return cls(x=float(data["x"]), y=float(data["y"]))

    @classmethod
    def from_polar(cls, r: float, theta_rad: float, origin: Optional[Point2D] = None) -> Point2D:
        """Create point from polar coordinates (r, theta) relative to origin."""
        ox = origin.x if origin else 0.0
        oy = origin.y if origin else 0.0
        return cls(x=ox + r * math.cos(theta_rad), y=oy + r * math.sin(theta_rad))


@dataclass
class Point3D:
    """3D Cartesian Coordinate (x, y, z)."""

    x: float
    y: float
    z: float

    def distance_to(self, other: Point3D) -> float:
        """3D Euclidean distance."""
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def rotate_x(self, angle_rad: float) -> Point3D:
        """Rotate around X-axis."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Point3D(self.x, self.y * c - self.z * s, self.y * s + self.z * c)

    def rotate_y(self, angle_rad: float) -> Point3D:
        """Rotate around Y-axis."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Point3D(self.x * c + self.z * s, self.y, -self.x * s + self.z * c)

    def rotate_z(self, angle_rad: float) -> Point3D:
        """Rotate around Z-axis."""
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Point3D(self.x * c - self.y * s, self.x * s + self.y * c, self.z)

    def rotate_euler(self, rx: float, ry: float, rz: float) -> Point3D:
        """Rotate by Euler angles in order X -> Y -> Z."""
        return self.rotate_x(rx).rotate_y(ry).rotate_z(rz)

    def project_2d(
        self,
        focal_length: float = 500.0,
        camera_z: float = 600.0,
        orthographic: bool = False,
    ) -> Point2D:
        """Project 3D point onto 2D plane (perspective or orthographic)."""
        if orthographic:
            return Point2D(self.x, self.y)
        denom = camera_z - self.z
        if abs(denom) < 1e-6:
            denom = 1e-6 if denom >= 0 else -1e-6
        scale = focal_length / denom
        return Point2D(self.x * scale, self.y * scale)

    def to_dict(self) -> Dict[str, float]:
        """Serialize 3D point to dictionary."""
        return {"x": round(self.x, 6), "y": round(self.y, 6), "z": round(self.z, 6)}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Point3D:
        """Deserialize 3D point from dictionary."""
        return cls(x=float(data["x"]), y=float(data["y"]), z=float(data.get("z", 0.0)))


@dataclass
class LineSegment:
    """2D Line Segment between start and end points."""

    start: Point2D
    end: Point2D
    stroke_width: float = 1.0
    color: str = "#00ffff"
    layer: str = "default"
    opacity: float = 1.0

    @property
    def length(self) -> float:
        """Length of the segment."""
        return self.start.distance_to(self.end)

    @property
    def midpoint(self) -> Point2D:
        """Midpoint of the segment."""
        return Point2D((self.start.x + self.end.x) / 2.0, (self.start.y + self.end.y) / 2.0)

    def translate(self, dx: float, dy: float) -> LineSegment:
        """Translate segment."""
        return LineSegment(
            start=self.start.translate(dx, dy),
            end=self.end.translate(dx, dy),
            stroke_width=self.stroke_width,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
        )

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> LineSegment:
        """Scale segment."""
        return LineSegment(
            start=self.start.scale(factor, origin),
            end=self.end.scale(factor, origin),
            stroke_width=self.stroke_width * factor,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
        )

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> LineSegment:
        """Rotate segment."""
        return LineSegment(
            start=self.start.rotate(angle_rad, origin),
            end=self.end.rotate(angle_rad, origin),
            stroke_width=self.stroke_width,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize segment to dictionary."""
        return {
            "type": "line",
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
            "stroke_width": self.stroke_width,
            "color": self.color,
            "layer": self.layer,
            "opacity": self.opacity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LineSegment:
        """Deserialize segment from dictionary."""
        return cls(
            start=Point2D.from_dict(data["start"]),
            end=Point2D.from_dict(data["end"]),
            stroke_width=float(data.get("stroke_width", 1.0)),
            color=str(data.get("color", "#00ffff")),
            layer=str(data.get("layer", "default")),
            opacity=float(data.get("opacity", 1.0)),
        )


@dataclass
class Circle:
    """2D Circle with center and radius."""

    center: Point2D
    radius: float
    stroke_width: float = 1.0
    color: str = "#00ffff"
    fill: Optional[str] = None
    layer: str = "default"
    opacity: float = 1.0

    @property
    def area(self) -> float:
        """Area of circle."""
        return math.pi * self.radius * self.radius

    @property
    def circumference(self) -> float:
        """Circumference of circle."""
        return 2.0 * math.pi * self.radius

    def point_at_angle(self, angle_rad: float) -> Point2D:
        """Get point on circumference at given angle in radians."""
        return Point2D.from_polar(self.radius, angle_rad, self.center)

    def translate(self, dx: float, dy: float) -> Circle:
        """Translate circle."""
        return Circle(
            center=self.center.translate(dx, dy),
            radius=self.radius,
            stroke_width=self.stroke_width,
            color=self.color,
            fill=self.fill,
            layer=self.layer,
            opacity=self.opacity,
        )

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> Circle:
        """Scale circle."""
        return Circle(
            center=self.center.scale(factor, origin),
            radius=self.radius * factor,
            stroke_width=self.stroke_width * factor,
            color=self.color,
            fill=self.fill,
            layer=self.layer,
            opacity=self.opacity,
        )

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> Circle:
        """Rotate circle center around origin."""
        return Circle(
            center=self.center.rotate(angle_rad, origin),
            radius=self.radius,
            stroke_width=self.stroke_width,
            color=self.color,
            fill=self.fill,
            layer=self.layer,
            opacity=self.opacity,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize circle to dictionary."""
        return {
            "type": "circle",
            "center": self.center.to_dict(),
            "radius": round(self.radius, 6),
            "stroke_width": self.stroke_width,
            "color": self.color,
            "fill": self.fill,
            "layer": self.layer,
            "opacity": self.opacity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Circle:
        """Deserialize circle from dictionary."""
        return cls(
            center=Point2D.from_dict(data["center"]),
            radius=float(data["radius"]),
            stroke_width=float(data.get("stroke_width", 1.0)),
            color=str(data.get("color", "#00ffff")),
            fill=data.get("fill"),
            layer=str(data.get("layer", "default")),
            opacity=float(data.get("opacity", 1.0)),
        )


@dataclass
class Arc:
    """2D Circular Arc from start_angle to end_angle (in radians)."""

    center: Point2D
    radius: float
    start_angle: float  # In radians
    end_angle: float  # In radians
    stroke_width: float = 1.0
    color: str = "#00ffff"
    layer: str = "default"
    opacity: float = 1.0

    @property
    def start_point(self) -> Point2D:
        """Start point of the arc."""
        return Point2D.from_polar(self.radius, self.start_angle, self.center)

    @property
    def end_point(self) -> Point2D:
        """End point of the arc."""
        return Point2D.from_polar(self.radius, self.end_angle, self.center)

    @property
    def span_angle(self) -> float:
        """Sweep angle in radians (normalized [0, 2pi))."""
        diff = (self.end_angle - self.start_angle) % (2.0 * math.pi)
        return diff if diff > 0 else 2.0 * math.pi

    def translate(self, dx: float, dy: float) -> Arc:
        """Translate arc."""
        return Arc(
            center=self.center.translate(dx, dy),
            radius=self.radius,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
            stroke_width=self.stroke_width,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
        )

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> Arc:
        """Scale arc."""
        return Arc(
            center=self.center.scale(factor, origin),
            radius=self.radius * factor,
            start_angle=self.start_angle,
            end_angle=self.end_angle,
            stroke_width=self.stroke_width * factor,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
        )

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> Arc:
        """Rotate arc."""
        return Arc(
            center=self.center.rotate(angle_rad, origin),
            radius=self.radius,
            start_angle=self.start_angle + angle_rad,
            end_angle=self.end_angle + angle_rad,
            stroke_width=self.stroke_width,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize arc to dictionary."""
        return {
            "type": "arc",
            "center": self.center.to_dict(),
            "radius": round(self.radius, 6),
            "start_angle": round(self.start_angle, 6),
            "end_angle": round(self.end_angle, 6),
            "stroke_width": self.stroke_width,
            "color": self.color,
            "layer": self.layer,
            "opacity": self.opacity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Arc:
        """Deserialize arc from dictionary."""
        return cls(
            center=Point2D.from_dict(data["center"]),
            radius=float(data["radius"]),
            start_angle=float(data["start_angle"]),
            end_angle=float(data["end_angle"]),
            stroke_width=float(data.get("stroke_width", 1.0)),
            color=str(data.get("color", "#00ffff")),
            layer=str(data.get("layer", "default")),
            opacity=float(data.get("opacity", 1.0)),
        )


@dataclass
class Polygon:
    """2D Polygon defined by a sequence of vertices."""

    points: List[Point2D]
    stroke_width: float = 1.0
    color: str = "#00ffff"
    fill: Optional[str] = None
    layer: str = "default"
    opacity: float = 1.0
    closed: bool = True

    @property
    def centroid(self) -> Point2D:
        """Centroid of polygon vertices."""
        if not self.points:
            return Point2D(0.0, 0.0)
        cx = sum(p.x for p in self.points) / len(self.points)
        cy = sum(p.y for p in self.points) / len(self.points)
        return Point2D(cx, cy)

    def translate(self, dx: float, dy: float) -> Polygon:
        """Translate polygon."""
        return Polygon(
            points=[p.translate(dx, dy) for p in self.points],
            stroke_width=self.stroke_width,
            color=self.color,
            fill=self.fill,
            layer=self.layer,
            opacity=self.opacity,
            closed=self.closed,
        )

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> Polygon:
        """Scale polygon."""
        return Polygon(
            points=[p.scale(factor, origin) for p in self.points],
            stroke_width=self.stroke_width * factor,
            color=self.color,
            fill=self.fill,
            layer=self.layer,
            opacity=self.opacity,
            closed=self.closed,
        )

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> Polygon:
        """Rotate polygon."""
        return Polygon(
            points=[p.rotate(angle_rad, origin) for p in self.points],
            stroke_width=self.stroke_width,
            color=self.color,
            fill=self.fill,
            layer=self.layer,
            opacity=self.opacity,
            closed=self.closed,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize polygon to dictionary."""
        return {
            "type": "polygon",
            "points": [p.to_dict() for p in self.points],
            "stroke_width": self.stroke_width,
            "color": self.color,
            "fill": self.fill,
            "layer": self.layer,
            "opacity": self.opacity,
            "closed": self.closed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Polygon:
        """Deserialize polygon from dictionary."""
        return cls(
            points=[Point2D.from_dict(p) for p in data["points"]],
            stroke_width=float(data.get("stroke_width", 1.0)),
            color=str(data.get("color", "#00ffff")),
            fill=data.get("fill"),
            layer=str(data.get("layer", "default")),
            opacity=float(data.get("opacity", 1.0)),
            closed=bool(data.get("closed", True)),
        )


@dataclass
class Spline:
    """2D Parametric B-Spline / Catmull-Rom curve through control points."""

    control_points: List[Point2D]
    stroke_width: float = 1.0
    color: str = "#00ffff"
    layer: str = "default"
    opacity: float = 1.0
    degree: int = 3
    closed: bool = False

    def sample_points(self, samples_per_segment: int = 16) -> List[Point2D]:
        """Sample points along Catmull-Rom spline interpolation."""
        pts = list(self.control_points)
        if len(pts) < 2:
            return pts

        if self.closed:
            pts = [pts[-1]] + pts + [pts[0], pts[1]]
        else:
            pts = [pts[0]] + pts + [pts[-1]]

        result: List[Point2D] = []
        for i in range(1, len(pts) - 2):
            p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
            for step in range(samples_per_segment):
                t = step / float(samples_per_segment)
                t2 = t * t
                t3 = t2 * t
                # Catmull-Rom matrix blending
                x = 0.5 * (
                    (2 * p1.x)
                    + (-p0.x + p2.x) * t
                    + (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * t2
                    + (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * t3
                )
                y = 0.5 * (
                    (2 * p1.y)
                    + (-p0.y + p2.y) * t
                    + (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * t2
                    + (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * t3
                )
                result.append(Point2D(x, y))

        if not self.closed:
            result.append(self.control_points[-1])
        else:
            result.append(result[0])
        return result

    def translate(self, dx: float, dy: float) -> Spline:
        """Translate spline."""
        return Spline(
            control_points=[p.translate(dx, dy) for p in self.control_points],
            stroke_width=self.stroke_width,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
            degree=self.degree,
            closed=self.closed,
        )

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> Spline:
        """Scale spline."""
        return Spline(
            control_points=[p.scale(factor, origin) for p in self.control_points],
            stroke_width=self.stroke_width * factor,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
            degree=self.degree,
            closed=self.closed,
        )

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> Spline:
        """Rotate spline."""
        return Spline(
            control_points=[p.rotate(angle_rad, origin) for p in self.control_points],
            stroke_width=self.stroke_width,
            color=self.color,
            layer=self.layer,
            opacity=self.opacity,
            degree=self.degree,
            closed=self.closed,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize spline to dictionary."""
        return {
            "type": "spline",
            "control_points": [p.to_dict() for p in self.control_points],
            "stroke_width": self.stroke_width,
            "color": self.color,
            "layer": self.layer,
            "opacity": self.opacity,
            "degree": self.degree,
            "closed": self.closed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Spline:
        """Deserialize spline from dictionary."""
        return cls(
            control_points=[Point2D.from_dict(p) for p in data["control_points"]],
            stroke_width=float(data.get("stroke_width", 1.0)),
            color=str(data.get("color", "#00ffff")),
            layer=str(data.get("layer", "default")),
            opacity=float(data.get("opacity", 1.0)),
            degree=int(data.get("degree", 3)),
            closed=bool(data.get("closed", False)),
        )


@dataclass
class BoundingBox:
    """Axis-aligned 2D Bounding Box."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def width(self) -> float:
        """Width of the bounding box."""
        return max(0.0, self.max_x - self.min_x)

    @property
    def height(self) -> float:
        """Height of the bounding box."""
        return max(0.0, self.max_y - self.min_y)

    @property
    def center(self) -> Point2D:
        """Center point of bounding box."""
        return Point2D((self.min_x + self.max_x) / 2.0, (self.min_y + self.max_y) / 2.0)

    def to_tuple(self) -> Tuple[float, float, float, float, float, float]:
        """Return (min_x, min_y, max_x, max_y, width, height)."""
        return (self.min_x, self.min_y, self.max_x, self.max_y, self.width, self.height)


@dataclass
class GeometryAST:
    """Unified Geometric Abstract Syntax Tree containing all primitives and metadata."""

    lines: List[LineSegment] = field(default_factory=list)
    circles: List[Circle] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    polygons: List[Polygon] = field(default_factory=list)
    splines: List[Spline] = field(default_factory=list)
    points3d: List[Point3D] = field(default_factory=list)
    title: str = "Sacred Geometry AST"
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    layers: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def add_line(
        self,
        start: Point2D,
        end: Point2D,
        stroke_width: float = 1.0,
        color: str = "#00ffff",
        layer: str = "default",
        opacity: float = 1.0,
    ) -> LineSegment:
        """Convenience method to construct and append a LineSegment."""
        line = LineSegment(start, end, stroke_width, color, layer, opacity)
        self.lines.append(line)
        return line

    def add_circle(
        self,
        center: Point2D,
        radius: float,
        stroke_width: float = 1.0,
        color: str = "#00ffff",
        fill: Optional[str] = None,
        layer: str = "default",
        opacity: float = 1.0,
    ) -> Circle:
        """Convenience method to construct and append a Circle."""
        circle = Circle(center, radius, stroke_width, color, fill, layer, opacity)
        self.circles.append(circle)
        return circle

    def add_arc(
        self,
        center: Point2D,
        radius: float,
        start_angle: float,
        end_angle: float,
        stroke_width: float = 1.0,
        color: str = "#00ffff",
        layer: str = "default",
        opacity: float = 1.0,
    ) -> Arc:
        """Convenience method to construct and append an Arc."""
        arc = Arc(center, radius, start_angle, end_angle, stroke_width, color, layer, opacity)
        self.arcs.append(arc)
        return arc

    def add_polygon(
        self,
        points: Sequence[Point2D],
        stroke_width: float = 1.0,
        color: str = "#00ffff",
        fill: Optional[str] = None,
        layer: str = "default",
        opacity: float = 1.0,
        closed: bool = True,
    ) -> Polygon:
        """Convenience method to construct and append a Polygon."""
        poly = Polygon(list(points), stroke_width, color, fill, layer, opacity, closed)
        self.polygons.append(poly)
        return poly

    def add_spline(
        self,
        control_points: Sequence[Point2D],
        stroke_width: float = 1.0,
        color: str = "#00ffff",
        layer: str = "default",
        opacity: float = 1.0,
        degree: int = 3,
        closed: bool = False,
    ) -> Spline:
        """Convenience method to construct and append a Spline."""
        spline = Spline(
            list(control_points), stroke_width, color, layer, opacity, degree, closed
        )
        self.splines.append(spline)
        return spline

    def bounds(self) -> BoundingBox:
        """Compute accurate axis-aligned bounding box covering all primitives."""
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")
        has_items = False

        for line in self.lines:
            for p in (line.start, line.end):
                min_x = min(min_x, p.x)
                min_y = min(min_y, p.y)
                max_x = max(max_x, p.x)
                max_y = max(max_y, p.y)
                has_items = True

        for circle in self.circles:
            min_x = min(min_x, circle.center.x - circle.radius)
            min_y = min(min_y, circle.center.y - circle.radius)
            max_x = max(max_x, circle.center.x + circle.radius)
            max_y = max(max_y, circle.center.y + circle.radius)
            has_items = True

        for arc in self.arcs:
            # Check arc start, end, and quadrant extrema if inside sweep
            sample_angles = [arc.start_angle, arc.end_angle]
            for quad_angle in [0.0, 0.5 * math.pi, math.pi, 1.5 * math.pi]:
                # Normalize angles
                normalized_start = arc.start_angle % (2 * math.pi)
                normalized_end = arc.end_angle % (2 * math.pi)
                if normalized_start < normalized_end:
                    if normalized_start <= quad_angle <= normalized_end:
                        sample_angles.append(quad_angle)
                else:
                    if quad_angle >= normalized_start or quad_angle <= normalized_end:
                        sample_angles.append(quad_angle)

            for a in sample_angles:
                p = arc.center.translate(arc.radius * math.cos(a), arc.radius * math.sin(a))
                min_x = min(min_x, p.x)
                min_y = min(min_y, p.y)
                max_x = max(max_x, p.x)
                max_y = max(max_y, p.y)
                has_items = True

        for poly in self.polygons:
            for p in poly.points:
                min_x = min(min_x, p.x)
                min_y = min(min_y, p.y)
                max_x = max(max_x, p.x)
                max_y = max(max_y, p.y)
                has_items = True

        for spline in self.splines:
            for p in spline.control_points:
                min_x = min(min_x, p.x)
                min_y = min(min_y, p.y)
                max_x = max(max_x, p.x)
                max_y = max(max_y, p.y)
                has_items = True

        if not has_items:
            return BoundingBox(0.0, 0.0, 0.0, 0.0)

        return BoundingBox(min_x, min_y, max_x, max_y)

    def translate(self, dx: float, dy: float) -> GeometryAST:
        """In-place translate all 2D primitives."""
        self.lines = [item.translate(dx, dy) for item in self.lines]
        self.circles = [item.translate(dx, dy) for item in self.circles]
        self.arcs = [item.translate(dx, dy) for item in self.arcs]
        self.polygons = [item.translate(dx, dy) for item in self.polygons]
        self.splines = [item.translate(dx, dy) for item in self.splines]
        return self

    def scale(self, factor: float, origin: Optional[Point2D] = None) -> GeometryAST:
        """In-place scale all 2D primitives."""
        self.lines = [item.scale(factor, origin) for item in self.lines]
        self.circles = [item.scale(factor, origin) for item in self.circles]
        self.arcs = [item.scale(factor, origin) for item in self.arcs]
        self.polygons = [item.scale(factor, origin) for item in self.polygons]
        self.splines = [item.scale(factor, origin) for item in self.splines]
        return self

    def rotate(self, angle_rad: float, origin: Optional[Point2D] = None) -> GeometryAST:
        """In-place rotate all 2D primitives."""
        self.lines = [item.rotate(angle_rad, origin) for item in self.lines]
        self.circles = [item.rotate(angle_rad, origin) for item in self.circles]
        self.arcs = [item.rotate(angle_rad, origin) for item in self.arcs]
        self.polygons = [item.rotate(angle_rad, origin) for item in self.polygons]
        self.splines = [item.rotate(angle_rad, origin) for item in self.splines]
        return self

    def center_at(self, target_cx: float = 0.0, target_cy: float = 0.0) -> GeometryAST:
        """Center the geometry AST at (target_cx, target_cy)."""
        bb = self.bounds()
        current_center = bb.center
        dx = target_cx - current_center.x
        dy = target_cy - current_center.y
        return self.translate(dx, dy)

    def fit_to_box(
        self,
        target_width: float,
        target_height: float,
        padding: float = 20.0,
        center: bool = True,
    ) -> GeometryAST:
        """Fit geometry inside bounding dimensions preserving aspect ratio."""
        bb = self.bounds()
        avail_w = max(1.0, target_width - 2.0 * padding)
        avail_h = max(1.0, target_height - 2.0 * padding)

        cur_w = max(1e-4, bb.width)
        cur_h = max(1e-4, bb.height)

        scale_factor = min(avail_w / cur_w, avail_h / cur_h)
        self.scale(scale_factor, origin=bb.center)

        if center:
            self.center_at(target_width / 2.0, target_height / 2.0)

        return self

    def stats(self) -> Dict[str, Any]:
        """Summary statistics of primitives in this AST."""
        bb = self.bounds()
        return {
            "total_primitives": (
                len(self.lines)
                + len(self.circles)
                + len(self.arcs)
                + len(self.polygons)
                + len(self.splines)
            ),
            "lines": len(self.lines),
            "circles": len(self.circles),
            "arcs": len(self.arcs),
            "polygons": len(self.polygons),
            "splines": len(self.splines),
            "points3d": len(self.points3d),
            "bounds": {
                "min_x": round(bb.min_x, 3),
                "min_y": round(bb.min_y, 3),
                "max_x": round(bb.max_x, 3),
                "max_y": round(bb.max_y, 3),
                "width": round(bb.width, 3),
                "height": round(bb.height, 3),
            },
        }

    @property
    def primitives(self) -> List[Any]:
        """Flattened list of all geometric primitives."""
        return self.lines + self.circles + self.arcs + self.polygons + self.splines

    @property
    def name(self) -> str:
        """Alias for title."""
        return self.title

    @name.setter
    def name(self, val: str) -> None:
        self.title = val

    @property
    def elements(self) -> List[Any]:
        """Alias for primitives."""
        return self.primitives

    def to_dict(self) -> Dict[str, Any]:
        """Serialize complete AST to JSON-friendly dictionary."""
        return {
            "title": self.title,
            "name": self.title,
            "description": self.description,
            "parameters": self.parameters,
            "tags": self.tags,
            "layers": self.layers,
            "primitives": [p.to_dict() for p in self.primitives],
            "lines": [l.to_dict() for l in self.lines],
            "circles": [c.to_dict() for c in self.circles],
            "arcs": [a.to_dict() for a in self.arcs],
            "polygons": [p.to_dict() for p in self.polygons],
            "splines": [s.to_dict() for s in self.splines],
            "points3d": [p3.to_dict() for p3 in self.points3d],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize AST to formatted JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> GeometryAST:
        """Deserialize AST from dictionary."""
        ast = cls(
            title=str(data.get("title", data.get("name", "Sacred Geometry AST"))),
            description=str(data.get("description", "")),
            parameters=dict(data.get("parameters", {})),
            tags=list(data.get("tags", [])),
            layers=dict(data.get("layers", {})),
        )

        for item in data.get("lines", []):
            ast.lines.append(LineSegment.from_dict(item))

        for item in data.get("circles", []):
            ast.circles.append(Circle.from_dict(item))

        for item in data.get("arcs", []):
            ast.arcs.append(Arc.from_dict(item))

        for item in data.get("polygons", []):
            ast.polygons.append(Polygon.from_dict(item))

        for item in data.get("splines", []):
            ast.splines.append(Spline.from_dict(item))

        for item in data.get("points3d", []):
            ast.points3d.append(Point3D.from_dict(item))

        return ast

    @classmethod
    def from_json(cls, json_str: str) -> GeometryAST:
        """Deserialize AST from JSON string."""
        return cls.from_dict(json.loads(json_str))


@dataclass
class PatternPreset:
    """Catalog Pattern Preset Definition with metadata and generator defaults."""

    id: str
    title: str
    category: str
    description: str
    default_parameters: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # beginner, medium, advanced, master
    historical_context: str = ""
    preview_hints: Dict[str, Any] = field(default_factory=dict)
    harmonic_ratios: List[str] = field(default_factory=lambda: ["1:1 (Unity)", "1:1.618 (Phi)", "1:1.732 (√3)"])

    @property
    def name(self) -> str:
        """Alias for title."""
        return self.title

    def to_dict(self) -> Dict[str, Any]:
        """Serialize preset to dictionary."""
        d = asdict(self)
        d["name"] = self.title
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PatternPreset:
        """Deserialize preset from dictionary."""
        ratios = data.get("harmonic_ratios", ["1:1 (Unity)", "1:1.618 (Phi)", "1:1.732 (√3)"])
        if isinstance(ratios, dict):
            ratios = [f"{k}={v}" for k, v in ratios.items()]
        return cls(
            id=data["id"],
            title=data.get("title", data.get("name", "")),
            category=data["category"],
            description=data["description"],
            default_parameters=data.get("default_parameters", {}),
            tags=data.get("tags", []),
            difficulty=data.get("difficulty", "medium"),
            historical_context=data.get("historical_context", ""),
            preview_hints=data.get("preview_hints", {}),
            harmonic_ratios=ratios,
        )

