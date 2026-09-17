"""Multi-Format Sacred Geometry Exporters (SVG, AutoCAD DXF, 3D OBJ).

Provides high-precision exporters for vector graphics, CNC/Laser manufacturing,
and 3D printing/rendering:
- SVGExporter / export_svg (Vector graphics with themes and glow filters)
- DXFExporter / export_dxf (AutoCAD R2000 ASCII DXF for laser cutting and CNC milling)
- OBJExporter / export_obj (3D Wavefront OBJ relief medallion and polyhedra mesh with MTL)
"""

from .dxf_exporter import DXFExporter, export_dxf, hex_to_aci
from .obj_exporter import OBJExporter, export_obj
from .svg_exporter import SVG_THEMES, SVGExporter, export_svg

__all__ = [
    # SVG
    "SVGExporter",
    "export_svg",
    "SVG_THEMES",
    # DXF
    "DXFExporter",
    "export_dxf",
    "hex_to_aci",
    # OBJ
    "OBJExporter",
    "export_obj",
]
