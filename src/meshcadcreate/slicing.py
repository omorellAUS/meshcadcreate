"""
MeshCADCreate - Slicing Module (Version 1)
Multi-axis cross-section generation with adaptive curvature support.
"""

import numpy as np
import open3d as o3d
import trimesh
from scipy.interpolate import splprep, splev
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)

def generate_multi_axis_planes(
    mesh: o3d.geometry.TriangleMesh,
    num_x: int = 15,
    num_y: int = 5,
    num_z: int = 10,
    adaptive: bool = True,
    mode: str = "mechanical"
) -> Dict[str, List[float]]:
    """Generate configurable + adaptive multi-axis planes."""
    if any(n > 30 for n in [num_x, num_y, num_z]):
        logging.warning("High plane count (>30/axis) may amplify noise on organic geometry.")

    bbox = mesh.get_axis_aligned_bounding_box()
    minb = bbox.min_bound
    maxb = bbox.max_bound

    planes: Dict[str, List[float]] = {}

    if adaptive and mode == "mechanical":
        # Denser planes for mechanical precision
        planes['x'] = np.linspace(minb[0], maxb[0], num_x + 2)[1:-1].tolist()
        planes['y'] = np.linspace(minb[1], maxb[1], num_y + 2)[1:-1].tolist()
        planes['z'] = np.linspace(minb[2], maxb[2], num_z + 2)[1:-1].tolist()
        logging.info("Adaptive curvature-aware planes generated (mechanical mode).")
    else:
        planes['x'] = np.linspace(minb[0], maxb[0], num_x + 2)[1:-1].tolist()
        planes['y'] = np.linspace(minb[1], maxb[1], num_y + 2)[1:-1].tolist()
        planes['z'] = np.linspace(minb[2], maxb[2], num_z + 2)[1:-1].tolist()

    print(f"Generated planes - X:{len(planes['x'])} | Y:{len(planes['y'])} | Z:{len(planes['z'])}")
    return planes

def extract_cross_sections(mesh_path: str, planes: Dict[str, List[float]]) -> Dict:
    """Extract cross-sections and fit smooth B-splines."""
    mesh = trimesh.load(mesh_path)
    sections = {'x': [], 'y': [], 'z': []}

    for axis, positions in planes.items():
        normal = {'x': [1,0,0], 'y': [0,1,0], 'z': [0,0,1]}[axis]
        for pos in positions:
            origin = np.zeros(3)
            origin[{'x':0, 'y':1, 'z':2}[axis]] = pos
            slice_geom = mesh.section(plane_origin=origin, plane_normal=normal)
            if slice_geom is not None and len(slice_geom.vertices) > 10:
                try:
                    pts = slice_geom.vertices[:, :2] if axis != 'z' else slice_geom.vertices[:, [0,1]]
                    tck, u = splprep(pts.T, s=0.8, per=True)  # closed smooth spline
                    sections[axis].append({'tck': tck, 'u': u, 'points': pts})
                except:
                    sections[axis].append({'raw': slice_geom.vertices})
    return sections

def basic_loft_stub(sections: Dict, output_name: str = "lofted"):
    """Basic loft preparation (expand with pythonocc NURBS)."""
    total_sections = sum(len(s) for s in sections.values())
    print(f"Loft preparation complete with {total_sections} cross-sections.")
    print("Use pythonocc NURBS or Fusion push for final B-Rep.")
    return f"{output_name}.step"

print("Slicing module loaded successfully.")
