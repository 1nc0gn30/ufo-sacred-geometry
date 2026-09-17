"""3D Wavefront OBJ & MTL Mesh Exporter for Sacred Geometry Medallions.

Transforms 2D/3D Sacred Geometry AST into physical 3D relief medallions,
engraved coins, architectural plaques, and 3D wireframe polyhedra.
Ready for 3D printing (STL/OBJ slicing in Cura/PrusaSlicer), Blender,
Three.js, Unreal Engine, and Unity.
100% Python Standard Library.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from ..compat import atomic_write_text
from ..models import Arc, Circle, GeometryAST, LineSegment, Point2D, Point3D, Polygon, Spline


class OBJExporter:
    """3D Wavefront OBJ & MTL Exporter for Sacred Geometry Medallions & Polyhedra."""

    def __init__(
        self,
        base_type: str = "cylinder",  # 'cylinder', 'box', or 'none' (wireframe only)
        base_radius_factor: float = 1.15,
        base_thickness: float = 4.0,
        relief_height: float = 1.8,
        stroke_width_3d: float = 0.8,
        circle_segments: int = 48,
        material_name: str = "SacredGold",
    ) -> None:
        self.base_type = base_type
        self.base_radius_factor = base_radius_factor
        self.base_thickness = base_thickness
        self.relief_height = relief_height
        self.stroke_width_3d = stroke_width_3d
        self.circle_segments = circle_segments
        self.material_name = material_name

        self._vertices: List[Tuple[float, float, float]] = []
        self._normals: List[Tuple[float, float, float]] = []
        self._faces: List[Tuple[List[int], Optional[int]]] = []  # ([vertex_indices 1-based], normal_idx 1-based)

    def _add_vertex(self, x: float, y: float, z: float) -> int:
        self._vertices.append((x, y, z))
        return len(self._vertices)  # 1-indexed

    def _add_normal(self, nx: float, ny: float, nz: float) -> int:
        length = math.sqrt(nx * nx + ny * ny + nz * nz)
        if length > 1e-6:
            nx /= length
            ny /= length
            nz /= length
        else:
            nx, ny, nz = 0.0, 0.0, 1.0
        self._normals.append((nx, ny, nz))
        return len(self._normals)  # 1-indexed

    def _add_face(self, v_indices: List[int], normal_idx: Optional[int] = None) -> None:
        self._faces.append((v_indices, normal_idx))

    def _build_base_plate(self, ast: GeometryAST) -> None:
        """Construct the 3D base medallion plate (cylinder or box)."""
        if self.base_type == "none":
            return

        bb = ast.bounds()
        center_x = (bb.min_x + bb.max_x) / 2.0
        center_y = (bb.min_y + bb.max_y) / 2.0
        max_dimension = max(bb.width, bb.height) / 2.0
        radius = max(10.0, max_dimension * self.base_radius_factor)

        z_bot = 0.0
        z_top = self.base_thickness

        n_up = self._add_normal(0.0, 0.0, 1.0)
        n_down = self._add_normal(0.0, 0.0, -1.0)

        if self.base_type == "box":
            half_w = radius
            half_h = radius
            # 8 box corners
            # Bottom (z=0)
            v_b1 = self._add_vertex(center_x - half_w, center_y - half_h, z_bot)
            v_b2 = self._add_vertex(center_x + half_w, center_y - half_h, z_bot)
            v_b3 = self._add_vertex(center_x + half_w, center_y + half_h, z_bot)
            v_b4 = self._add_vertex(center_x - half_w, center_y + half_h, z_bot)
            # Top (z=base_thickness)
            v_t1 = self._add_vertex(center_x - half_w, center_y - half_h, z_top)
            v_t2 = self._add_vertex(center_x + half_w, center_y - half_h, z_top)
            v_t3 = self._add_vertex(center_x + half_w, center_y + half_h, z_top)
            v_t4 = self._add_vertex(center_x - half_w, center_y + half_h, z_top)

            # Faces
            self._add_face([v_b1, v_b4, v_b3, v_b2], n_down)  # Bottom
            self._add_face([v_t1, v_t2, v_t3, v_t4], n_up)  # Top

            n_front = self._add_normal(0.0, -1.0, 0.0)
            n_back = self._add_normal(0.0, 1.0, 0.0)
            n_left = self._add_normal(-1.0, 0.0, 0.0)
            n_right = self._add_normal(1.0, 0.0, 0.0)

            self._add_face([v_b1, v_b2, v_t2, v_t1], n_front)
            self._add_face([v_b3, v_b4, v_t4, v_t3], n_back)
            self._add_face([v_b4, v_b1, v_t1, v_t4], n_left)
            self._add_face([v_b2, v_b3, v_t3, v_t2], n_right)

        else:  # 'cylinder'
            n_segs = self.circle_segments
            top_verts: List[int] = []
            bot_verts: List[int] = []

            for i in range(n_segs):
                angle = i * (2.0 * math.pi / n_segs)
                px = center_x + radius * math.cos(angle)
                py = center_y + radius * math.sin(angle)

                v_bot = self._add_vertex(px, py, z_bot)
                v_top = self._add_vertex(px, py, z_top)

                bot_verts.append(v_bot)
                top_verts.append(v_top)

            # Top & Bottom cap center points
            v_top_center = self._add_vertex(center_x, center_y, z_top)
            v_bot_center = self._add_vertex(center_x, center_y, z_bot)

            # Cap triangle fans
            for i in range(n_segs):
                i_next = (i + 1) % n_segs
                # Top Cap
                self._add_face([v_top_center, top_verts[i], top_verts[i_next]], n_up)
                # Bottom Cap
                self._add_face([v_bot_center, bot_verts[i_next], bot_verts[i]], n_down)

                # Side Quad Wall
                ang_mid = (i + 0.5) * (2.0 * math.pi / n_segs)
                n_side = self._add_normal(math.cos(ang_mid), math.sin(ang_mid), 0.0)
                self._add_face(
                    [bot_verts[i], bot_verts[i_next], top_verts[i_next], top_verts[i]],
                    n_side,
                )

    def _extrude_line_segment(self, line: LineSegment, z_base: float) -> None:
        """Extrude a 2D line segment into a 3D raised rectangular prism rib."""
        p1 = line.start
        p2 = line.end
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        dist = math.hypot(dx, dy)
        if dist < 1e-5:
            return

        w = max(0.2, self.stroke_width_3d * (line.stroke_width or 1.0) / 2.0)
        nx = -dy / dist * w
        ny = dx / dist * w

        z_top = z_base + self.relief_height

        # 4 Base Vertices (at z_base)
        v_b1 = self._add_vertex(p1.x + nx, p1.y + ny, z_base)
        v_b2 = self._add_vertex(p1.x - nx, p1.y - ny, z_base)
        v_b3 = self._add_vertex(p2.x - nx, p2.y - ny, z_base)
        v_b4 = self._add_vertex(p2.x + nx, p2.y + ny, z_base)

        # 4 Top Vertices (at z_top)
        v_t1 = self._add_vertex(p1.x + nx, p1.y + ny, z_top)
        v_t2 = self._add_vertex(p1.x - nx, p1.y - ny, z_top)
        v_t3 = self._add_vertex(p2.x - nx, p2.y - ny, z_top)
        v_t4 = self._add_vertex(p2.x + nx, p2.y + ny, z_top)

        n_up = self._add_normal(0.0, 0.0, 1.0)
        n_left = self._add_normal(nx, ny, 0.0)
        n_right = self._add_normal(-nx, -ny, 0.0)

        # Top Face
        self._add_face([v_t1, v_t2, v_t3, v_t4], n_up)
        # Left Side
        self._add_face([v_b1, v_t1, v_t4, v_b4], n_left)
        # Right Side
        self._add_face([v_b2, v_b3, v_t3, v_t2], n_right)

    def _extrude_circle(self, circle: Circle, z_base: float) -> None:
        """Extrude a 2D circle into a 3D raised concentric annular ring."""
        w = max(0.2, self.stroke_width_3d * (circle.stroke_width or 1.0) / 2.0)
        r_inner = max(0.1, circle.radius - w)
        r_outer = circle.radius + w

        cx, cy = circle.center.x, circle.center.y
        z_top = z_base + self.relief_height
        n_segs = max(16, min(64, self.circle_segments))

        top_in: List[int] = []
        top_out: List[int] = []
        bot_in: List[int] = []
        bot_out: List[int] = []

        for i in range(n_segs):
            ang = i * (2.0 * math.pi / n_segs)
            cos_a = math.cos(ang)
            sin_a = math.sin(ang)

            # Outer vertices
            px_out = cx + r_outer * cos_a
            py_out = cy + r_outer * sin_a
            bot_out.append(self._add_vertex(px_out, py_out, z_base))
            top_out.append(self._add_vertex(px_out, py_out, z_top))

            # Inner vertices
            px_in = cx + r_inner * cos_a
            py_in = cy + r_inner * sin_a
            bot_in.append(self._add_vertex(px_in, py_in, z_base))
            top_in.append(self._add_vertex(px_in, py_in, z_top))

        n_up = self._add_normal(0.0, 0.0, 1.0)

        for i in range(n_segs):
            i_next = (i + 1) % n_segs

            # Top ring quad
            self._add_face([top_in[i], top_out[i], top_out[i_next], top_in[i_next]], n_up)

            # Outer side wall
            ang_mid = (i + 0.5) * (2.0 * math.pi / n_segs)
            n_out = self._add_normal(math.cos(ang_mid), math.sin(ang_mid), 0.0)
            self._add_face(
                [bot_out[i], bot_out[i_next], top_out[i_next], top_out[i]],
                n_out,
            )

            # Inner side wall
            n_in = self._add_normal(-math.cos(ang_mid), -math.sin(ang_mid), 0.0)
            self._add_face(
                [bot_in[i], top_in[i], top_in[i_next], bot_in[i_next]],
                n_in,
            )

    def _extrude_polygon(self, poly: Polygon, z_base: float) -> None:
        """Extrude polygon perimeter lines into 3D raised ribs."""
        pts = poly.points
        if len(pts) < 2:
            return
        for i in range(len(pts) - (0 if poly.closed else 1)):
            p1 = pts[i]
            p2 = pts[(i + 1) % len(pts)]
            line = LineSegment(p1, p2, stroke_width=poly.stroke_width)
            self._extrude_line_segment(line, z_base)

    def export(self, ast: GeometryAST) -> str:
        """Generate 3D Wavefront OBJ string for the given GeometryAST."""
        self._vertices.clear()
        self._normals.clear()
        self._faces.clear()

        # 1. Build Medallion Base Plate
        self._build_base_plate(ast)

        # 2. Extrude All 2D Primitives on top of the medallion
        z_base = self.base_thickness if self.base_type != "none" else 0.0

        for line in ast.lines:
            self._extrude_line_segment(line, z_base)

        for circle in ast.circles:
            self._extrude_circle(circle, z_base)

        for arc in ast.arcs:
            # Convert arc to short line segments
            sweep = (arc.end_angle - arc.start_angle) % (2.0 * math.pi)
            if sweep < 0:
                sweep += 2.0 * math.pi
            n_steps = max(6, int(sweep * 12))
            for k in range(n_steps):
                a1 = arc.start_angle + (k / float(n_steps)) * sweep
                a2 = arc.start_angle + ((k + 1) / float(n_steps)) * sweep
                p1 = arc.center.translate(arc.radius * math.cos(a1), arc.radius * math.sin(a1))
                p2 = arc.center.translate(arc.radius * math.cos(a2), arc.radius * math.sin(a2))
                self._extrude_line_segment(LineSegment(p1, p2, stroke_width=arc.stroke_width), z_base)

        for poly in ast.polygons:
            self._extrude_polygon(poly, z_base)

        for spline in ast.splines:
            sampled = spline.sample_points(samples_per_segment=12)
            for k in range(len(sampled) - 1):
                self._extrude_line_segment(
                    LineSegment(sampled[k], sampled[k + 1], stroke_width=spline.stroke_width),
                    z_base,
                )

        # Format OBJ File
        lines: List[str] = [
            f"# UFO Sacred Geometry 3D Mesh Exporter",
            f"# Title: {ast.title}",
            f"# Total Vertices: {len(self._vertices)}",
            f"# Total Faces: {len(self._faces)}",
            f"mtllib {self.material_name}.mtl",
            f"o {ast.title.replace(' ', '_')}",
            f"usemtl {self.material_name}",
            "",
        ]

        # Vertices
        for vx, vy, vz in self._vertices:
            lines.append(f"v {vx:.5f} {vy:.5f} {vz:.5f}")

        lines.append("")

        # Normals
        for nx, ny, nz in self._normals:
            lines.append(f"vn {nx:.4f} {ny:.4f} {nz:.4f}")

        lines.append("")

        # Faces
        for v_indices, n_idx in self._faces:
            if n_idx is not None:
                f_str = " ".join(f"{v}//{n_idx}" for v in v_indices)
            else:
                f_str = " ".join(str(v) for v in v_indices)
            lines.append(f"f {f_str}")

        return "\n".join(lines) + "\n"

    def export_mtl(self) -> str:
        """Generate companion Wavefront MTL material definition."""
        return (
            f"# Sacred Geometry Material Library\n"
            f"newmtl {self.material_name}\n"
            f"Ka 0.24725 0.1995 0.0745\n"
            f"Kd 0.75164 0.60648 0.22648\n"
            f"Ks 0.628281 0.555802 0.366065\n"
            f"Ns 51.2\n"
            f"d 1.0\n"
            f"illum 2\n"
        )

    def export_to_file(
        self,
        ast: GeometryAST,
        obj_path: Union[str, Path],
        mtl_path: Optional[Union[str, Path]] = None,
    ) -> Path:
        """Export OBJ and companion MTL file atomically."""
        obj_target = Path(obj_path).resolve()
        obj_str = self.export(ast)
        written_obj = atomic_write_text(obj_target, obj_str)

        # Write MTL
        if mtl_path is None:
            mtl_target = obj_target.with_suffix(".mtl")
        else:
            mtl_target = Path(mtl_path).resolve()

        atomic_write_text(mtl_target, self.export_mtl())
        return written_obj


def export_obj(
    ast: GeometryAST,
    file_path: Optional[Union[str, Path]] = None,
    base_type: str = "cylinder",
    base_thickness: float = 4.0,
    relief_height: float = 1.8,
    relief_depth: Optional[float] = None,
    medallion_base: Optional[bool] = None,
    stroke_width_3d: float = 0.8,
    **kwargs: Any,
) -> str:
    """Convenience function to export GeometryAST to Wavefront OBJ string and optional file."""
    effective_relief = relief_depth if relief_depth is not None else relief_height
    effective_base = "cylinder" if medallion_base is True else (base_type if medallion_base is not False else "none")
    exporter = OBJExporter(
        base_type=effective_base,
        base_thickness=base_thickness,
        relief_height=effective_relief,
        stroke_width_3d=stroke_width_3d,
    )
    obj_str = exporter.export(ast)
    if file_path:
        exporter.export_to_file(ast, file_path)
    return obj_str

