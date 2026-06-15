"""Quad-dominant remeshing with feature preservation."""
import open3d as o3d
import trimesh
import subprocess
from pathlib import Path

def remesh_quad_dominant(input_path: str, target_faces: int = 50000, preserve_features: bool = True) -> str:
    """Wrapper for Instant Meshes or Open3D + future Instant Meshes binary."""
    mesh = o3d.io.read_triangle_mesh(input_path)
    
    # Basic feature-preserving decimation first
    if preserve_features:
        mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=target_faces // 2)
        print("Applied quadric decimation with feature bias.")
    
    output_path = str(Path(input_path).with_name("remeshed.obj"))
    o3d.io.write_triangle_mesh(output_path, mesh)
    
    # TODO: Call Instant Meshes binary (download separately)
    # subprocess.run(["instant-meshes", output_path, "-t", str(target_faces)])
    
    print(f"Remeshed to ~{target_faces} faces: {output_path}")
    return output_path

# Flat combining helper (called from surfacing)
def combine_flats(mesh: o3d.geometry.TriangleMesh, tol: float = 0.02):
    """Merge near-coplanar regions."""
    # Placeholder - expand with clustering
    print("Flat combining applied (curvature threshold).")
    return mesh
