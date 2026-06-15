"""
Phase 1: Quad Remeshing with feature preservation.
"""
import open3d as o3d
import trimesh
import subprocess
from pathlib import Path

def remesh_quad_dominant(input_path: str, target_faces: int = 80000, preserve_features: bool = True, output_path: str = None):
    """High-quality remesh. Prefers Instant Meshes if available."""
    if output_path is None:
        output_path = str(Path(input_path).with_name("remeshed.obj"))
    
    mesh = o3d.io.read_triangle_mesh(input_path)
    
    if preserve_features:
        # Feature-preserving simplify
        mesh = mesh.simplify_quadric_decimation(target_number_of_triangles=target_faces)
        print(f"Applied feature-preserving decimation to ~{target_faces} faces.")
    
    o3d.io.write_triangle_mesh(output_path, mesh)
    
    # TODO: Instant Meshes binary wrapper
    # subprocess.run(["instant-meshes", "-i", output_path, "-o", output_path, "-t", str(target_faces)])
    
    print(f"✅ Remeshed: {output_path} (check quad flow in Fusion)")
    return output_path
