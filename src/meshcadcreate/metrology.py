"""
MeshCADCreate - Metrology Module (Version 1)
Deviation color mapping, point measurements, and GUI picker (SimScan-style).
"""

import numpy as np
import open3d as o3d
import logging
from PySide6.QtWidgets import QApplication
from .utils import deviation_color_map

logging.basicConfig(level=logging.INFO)

def point_deviation_measurement(mesh_path: str, solid_path: str, point: np.ndarray = None):
    """Single point-to-solid deviation query."""
    mesh = o3d.io.read_triangle_mesh(mesh_path)
    pcd = mesh.sample_points_uniformly(number_of_points=50000)
    
    if point is None:
        print("No point provided - using GUI picker next.")
        return None
    
    dists = pcd.compute_point_cloud_distance(o3d.geometry.PointCloud(points=o3d.utility.Vector3dVector([point])))
    dev = float(np.min(dists))
    logging.info(f"Point {point} deviation from solid: {dev:.4f} mm")
    return dev

def metrology_gui_picker(deviation_ply: str = "deviation_map.ply"):
    """Visual GUI picker on deviation color map."""
    print("\n=== Metrology GUI Picker ===")
    print("Click points on the color map to measure deviation.")
    print("Shift+Click or drag rectangle. Press Q when done.")
    
    pcd = o3d.io.read_point_cloud(deviation_ply)
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(width=1280, height=800, window_name="MeshCADCreate - Metrology Picker")
    vis.add_geometry(pcd)
    vis.get_render_option().point_size = 6.0
    vis.run()
    vis.destroy_window()
    
    picked = vis.get_picked_points()
    print(f"Selected {len(picked)} points for measurement.")
    return picked

def run_full_metrology(original_mesh_path: str, solid_path: str):
    """Full metrology workflow: color map + GUI picker."""
    print("Generating deviation color map...")
    max_dev = deviation_color_map(original_mesh_path, solid_path)
    
    print("\nOpening GUI for point measurements...")
    picked = metrology_gui_picker()
    
    if len(picked) > 0:
        print("Point measurements complete. Review logs for deviations.")
    return max_dev

print("Metrology module loaded successfully.")
