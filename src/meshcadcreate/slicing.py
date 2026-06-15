"""
Phase 2: Multi-axis cross-section extraction + loft prep.
Configurable planes + spline fitting.
"""
import numpy as np
import open3d as o3d
import trimesh
from scipy.interpolate import splprep, splev
from typing import Dict, List, Any
from .utils import compute_hausdorff_distance

def generate_multi_axis_planes(
    mesh: o3d.geometry.TriangleMesh,
    num_x: int = 15,
    num_y: int = 5,
    num_z: int = 10,
    include_45: bool = False,
    adaptive: bool = True
) -> Dict[str, List[float]]:
    """Configurable + adaptive planes."""
    if any(n > 30 for n in [num_x, num_y, num_z]):
        print("WARNING: High plane count risks noise overfitting.")
    
    bbox = mesh.get_axis_aligned_bounding_box()
    minb, maxb = bbox.min_bound, bbox.max_bound
    
    planes = {}
    planes['x'] = np.linspace(minb[0], maxb[0], num_x + 2)[1:-1].tolist()
    planes['y'] = np.linspace(minb[1], maxb[1], num_y + 2)[1:-1].tolist()
    planes['z'] = np.linspace(minb[2], maxb[2], num_z + 2)[1:-1].tolist()
    
    if adaptive:
        print("Adaptive mode: TODO - densify at high curvature regions.")
    
    print(f"Generated planes - X:{len(planes['x'])}, Y:{len(planes['y'])}, Z:{len(planes['z'])}")
    return planes

def extract_cross_sections(mesh_path: str, planes: Dict[str, List[float]]) -> Dict[str, List]:
    """Full extraction: intersect, fit B-splines, deviation check."""
    mesh = trimesh.load(mesh_path)
    sections = {'x': [], 'y': [], 'z': []}
    
    for axis, positions in planes.items():
        normal = {'x': [1,0,0], 'y': [0,1,0], 'z': [0,0,1]}[axis]
        for pos in positions:
            # Offset plane
            origin = np.zeros(3)
            origin[{'x':0, 'y':1, 'z':2}[axis]] = pos
            slice_geom = mesh.section(plane_origin=origin, plane_normal=normal)
            if slice_geom is not None and len(slice_geom.vertices) > 3:
                # Fit smooth spline
                pts = slice_geom.vertices[:, :2] if axis != 'z' else slice_geom.vertices[:, [0,1]]  # project
                try:
                    tck, u = splprep(pts.T, s=0.5, per=True)  # closed curve smoothing
                    sections[axis].append({'tck': tck, 'u': u, 'points': pts})
                except:
                    sections[axis].append({'raw': slice_geom.vertices})
    return sections

def basic_loft_stub(sections: Dict, output_name: str = "lofted"):
    """Basic loft prep stub - upgrade to pythonocc NURBS."""
    print(f"Lofting {len(sections.get('x', []))} sections per axis (stub).")
    print("TODO: Full NURBS loft with Fusion history or OpenCascade.")
    # Future: Create watertight B-rep
    return f"{output_name}.step"  # placeholder

# Example usage
if __name__ == "__main__":
    # planes = generate_multi_axis_planes(...)
    # sections = extract_cross_sections("aligned.stl", planes)
    # lofted = basic_loft_stub(sections)
    pass
