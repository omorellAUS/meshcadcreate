"""
MeshCADCreate - Utilities Module (Version 1)
Contains tolerances, metrology, repair, deviation, and helper functions.
"""

import numpy as np
import open3d as o3d
import logging
from dataclasses import dataclass
from pathlib import Path
import json
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton
from PySide6.QtCore import Qt

logging.basicConfig(level=logging.INFO)

@dataclass
class Tolerances:
    plane_max_dev: float = 0.05
    cylinder_max_res: float = 0.02
    hausdorff_max: float = 0.1
    mode: str = "mechanical"

def create_tolerance_dialog(defaults: Tolerances = None) -> Tolerances:
    """GUI Drag Bars for tolerance adjustment."""
    if defaults is None:
        defaults = Tolerances()
    
    dialog = QDialog()
    dialog.setWindowTitle("MeshCADCreate - Set Tolerances")
    layout = QVBoxLayout()
    
    def make_slider(label_text, default_val):
        hlayout = QHBoxLayout()
        label = QLabel(f"{label_text}: {default_val:.3f} mm")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(1)
        slider.setMaximum(500)
        slider.setValue(int(default_val * 100))
        
        def update(val):
            label.setText(f"{label_text}: {val/100:.3f} mm")
        slider.valueChanged.connect(update)
        
        hlayout.addWidget(QLabel(label_text))
        hlayout.addWidget(slider)
        hlayout.addWidget(label)
        return slider, label
    
    plane_slider, _ = make_slider("Plane Max Dev (mm)", defaults.plane_max_dev)
    cyl_slider, _ = make_slider("Cylinder Residual (mm)", defaults.cylinder_max_res)
    haus_slider, _ = make_slider("Hausdorff Max (mm)", defaults.hausdorff_max)
    
    layout.addLayout(plane_slider.parentWidget().layout() if hasattr(plane_slider, 'parentWidget') else None)  # Simplified layout
    
    btn = QPushButton("Apply Tolerances")
    btn.clicked.connect(dialog.accept)
    layout.addWidget(btn)
    dialog.setLayout(layout)
    dialog.exec()
    
    return Tolerances(
        plane_max_dev=plane_slider.value() / 100,
        cylinder_max_res=cyl_slider.value() / 100,
        hausdorff_max=haus_slider.value() / 100,
        mode=defaults.mode
    )

def inspect_and_repair_mesh(mesh: o3d.geometry.TriangleMesh, max_hole_size: float = 8.0):
    """Import repair - denoise, fill holes, clean."""
    print("=== Mesh Repair ===")
    mesh = mesh.remove_non_manifold_edges()
    mesh = mesh.remove_degenerate_triangles()
    mesh = mesh.fill_holes(max_hole_size)
    print(f"Repaired mesh: {len(mesh.vertices)} vertices")
    return mesh

def compute_hausdorff_distance(original_path: str, processed_path: str, target_max=0.1):
    """Deviation check."""
    orig = o3d.io.read_triangle_mesh(original_path)
    proc = o3d.io.read_triangle_mesh(processed_path)
    dist = orig.compute_point_cloud_distance(proc)
    max_d = float(np.max(dist))
    if max_d > target_max:
        logging.warning(f"Hausdorff deviation {max_d:.4f}mm exceeds target {target_max}mm")
    else:
        logging.info(f"✅ Hausdorff: {max_d:.4f}mm (within target)")
    return max_d

def deviation_color_map(original_mesh_path: str, processed_path: str, output_ply="deviation_map.ply"):
    """Color spectrum deviation map."""
    orig = o3d.io.read_triangle_mesh(original_mesh_path)
    proc = o3d.io.read_triangle_mesh(processed_path)
    pcd = orig.sample_points_uniformly(100000)
    dists = np.asarray(pcd.compute_point_cloud_distance(proc))
    
    colors = np.zeros((len(dists), 3))
    norm = np.clip(dists / 0.2, 0, 1)
    colors[:, 0] = np.clip(2 * (norm - 0.5), 0, 1)   # Red
    colors[:, 1] = np.clip(1 - 2 * np.abs(norm - 0.5), 0, 1)  # Green
    colors[:, 2] = np.clip(2 * (0.5 - norm), 0, 1)   # Blue
    
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.io.write_point_cloud(output_ply, pcd)
    print(f"✅ Deviation color map saved: {output_ply}")
    return float(np.max(dists))

print("Utils module loaded successfully.")
