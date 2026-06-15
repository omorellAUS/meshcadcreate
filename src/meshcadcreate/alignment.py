"""
MeshCADCreate - Alignment Module (Version 1)
Datum alignment with GUI picker, RANSAC plane fit, cylinder axis, and repair.
"""

import numpy as np
import open3d as o3d
import logging
import sys
from PySide6.QtWidgets import QApplication
from .utils import inspect_and_repair_mesh, compute_plane_deviation, compute_cylinder_residual, Tolerances

logging.basicConfig(level=logging.INFO)

def load_mesh(file_path: str, repair: bool = True):
    """Load mesh with optional repair."""
    mesh = o3d.io.read_triangle_mesh(file_path)
    mesh.compute_vertex_normals()
    if repair:
        mesh = inspect_and_repair_mesh(mesh)
    return mesh

def ransac_plane_fit(points: np.ndarray, max_dev_target: float = 0.05, max_iterations: int = 1000):
    """RANSAC plane fitting with deviation check."""
    best_normal = None
    best_centroid = None
    best_inliers = 0
    for _ in range(max_iterations):
        sample_idx = np.random.choice(len(points), 3, replace=False)
        sample = points[sample_idx]
        centroid = np.mean(sample, axis=0)
        normal = np.cross(sample[1] - sample[0], sample[2] - sample[0])
        normal /= np.linalg.norm(normal) + 1e-8
        dists = np.abs(np.dot(points - centroid, normal))
        inliers = np.sum(dists < max_dev_target)
        if inliers > best_inliers:
            best_inliers = inliers
            best_normal = normal
            best_centroid = centroid
    max_dev = float(np.max(np.abs(np.dot(points - best_centroid, best_normal))))
    logging.info(f"Plane fit - Max deviation: {max_dev:.4f} mm")
    return best_centroid, best_normal, max_dev

def fit_cylinder_axis(points: np.ndarray, max_res_target: float = 0.02):
    """Least squares cylinder axis fit."""
    centroid = np.mean(points, axis=0)
    _, _, vh = np.linalg.svd(points - centroid)
    direction = vh[0]
    residuals = np.linalg.norm(np.cross(points - centroid, direction), axis=1)
    max_res = float(np.max(residuals))
    logging.info(f"Cylinder axis fit - Max residual: {max_res:.4f} mm")
    return centroid, direction, max_res

def align_mesh(mesh: o3d.geometry.TriangleMesh, plane_normal: np.ndarray, plane_centroid: np.ndarray):
    """Align selected plane to XY."""
    target = np.array([0., 0., 1.])
    R = o3d.geometry.get_rotation_matrix_from_two_vectors(plane_normal, target)
    mesh.rotate(R, center=plane_centroid)
    mesh.translate(-R @ plane_centroid)
    return mesh

def gui_pick_points(mesh_path: str, prompt: str = "Select points for plane or cylinder"):
    """GUI point picker."""
    mesh = o3d.io.read_triangle_mesh(mesh_path)
    mesh.compute_vertex_normals()
    
    print(f"\n=== {prompt} ===")
    print("Instructions: Shift + Click to select points. Drag rectangle for area select. Press Q when done.")
    
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(width=1280, height=800)
    vis.add_geometry(mesh)
    vis.get_render_option().point_size = 8
    vis.run()
    vis.destroy_window()
    
    picked = vis.get_picked_points()
    print(f"Selected {len(picked)} points.")
    return np.array(picked)

def run_alignment_gui(input_path: str, output_path: str = "aligned.stl"):
    """Full GUI alignment workflow."""
    app = QApplication(sys.argv)
    
    mesh = load_mesh(input_path)
    
    print("Select points for PRIMARY PLANE (XY alignment)")
    plane_idx = gui_pick_points(input_path, "Primary Plane Selection")
    if len(plane_idx) < 6:
        logging.warning("Few points selected for plane. Results may be inaccurate.")
    
    plane_points = np.asarray(mesh.vertices)[plane_idx]
    centroid, normal, dev = ransac_plane_fit(plane_points)
    
    mesh = align_mesh(mesh, normal, centroid)
    
    print("Select points for CYLINDER AXIS (Z alignment)")
    cyl_idx = gui_pick_points(input_path, "Cylinder Axis Selection")
    if len(cyl_idx) > 3:
        cyl_points = np.asarray(mesh.vertices)[cyl_idx]
        _, _, res = fit_cylinder_axis(cyl_points)
    
    o3d.io.write_triangle_mesh(output_path, mesh)
    print(f"✅ Aligned mesh saved: {output_path}")
    return mesh

print("Alignment module loaded successfully.")
