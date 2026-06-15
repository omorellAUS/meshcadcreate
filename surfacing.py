# src/meshcadcreate/surfacing.py
import open3d as o3d
import numpy as np
import trimesh

def combine_flat_regions(mesh: o3d.geometry.TriangleMesh, tolerance: float = 0.01):
    """Merge coplanar triangles into larger polygons (better than Fusion)."""
    # Simple curvature-based clustering (expand with region growing)
    print("Flat combining: TODO full region-growing implementation.")
    # Placeholder: decimate flats
    mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=int(len(mesh.triangles)*0.7))
    return mesh

def basic_nurbs_loft(sections):
    """Stub for NURBS lofting between cross-sections."""
    print("NURBS loft: Use pythonocc or geomdl for production.")
    # Future: fit B-splines per section, loft
    return "Lofted solid placeholder"
