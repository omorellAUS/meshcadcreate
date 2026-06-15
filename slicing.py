# src/meshcadcreate/slicing.py
import open3d as o3d
import numpy as np
import trimesh
from typing import Dict, List

def generate_multi_axis_planes(
    mesh: o3d.geometry.TriangleMesh,
    num_x: int = 10,
    num_y: int = 5,
    num_z: int = 10,
    include_45: bool = False,
    adaptive: bool = False
) -> Dict[str, List[float]]:
    """Configurable planes per axis (up to ~30)."""
    if any(n > 30 for n in (num_x, num_y, num_z)):
        print("WARNING: High plane count (>30/axis) risks noise overfitting on organic scans.")
    
    bbox = mesh.get_axis_aligned_bounding_box()
    minb, maxb = bbox.min_bound, bbox.max_bound
    
    planes: Dict[str, List[float]] = {}
    planes['x'] = np.linspace(minb[0], maxb[0], num_x + 2)[1:-1].tolist()
    planes['y'] = np.linspace(minb[1], maxb[1], num_y + 2)[1:-1].tolist()
    planes['z'] = np.linspace(minb[2], maxb[2], num_z + 2)[1:-1].tolist()
    
    if include_45:
        print("45° planes: TODO - implement rotated slicing.")
    
    if adaptive:
        print("Adaptive curvature-based: TODO (denser at high curvature).")
    
    print(f"Generated {len(planes['x'])} X, {len(planes['y'])} Y, {len(planes['z'])} Z planes.")
    return planes

def extract_cross_sections(mesh_path: str, planes: Dict[str, List[float]]) -> Dict:
    """Basic intersection (expand with spline fitting)."""
    mesh = trimesh.load(mesh_path)
    sections = {}
    for axis, positions in planes.items():
        sections[axis] = []
        for pos in positions:
            # Simple plane cut - upgrade to full profile + projection
            plane_normal = {'x': [1,0,0], 'y': [0,1,0], 'z': [0,0,1]}[axis]
            slice = mesh.section(plane_origin=[0,0,0], plane_normal=plane_normal)  # adjust origin per pos
            if slice is not None:
                sections[axis].append(slice)
    return sections

# Example
if __name__ == "__main__":
    # mesh = o3d.io.read_triangle_mesh("aligned.stl")
    # planes = generate_multi_axis_planes(mesh, num_x=15, num_y=5, num_z=10)
    pass
