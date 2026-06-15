"""
Phase 0: Datum Alignment Module - Updated with Basic GUI Picker
"""
import numpy as np
import open3d as o3d
import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from .utils import save_selection  # Will create utils.py next

# ... (keep existing load_mesh, fit_plane, align_mesh_to_plane, fit_cylinder, multi_datum_align from previous)

def gui_pick_points(mesh_path: str, window_name: str = "MeshCADCreate - Drag Select Points"):
    """Basic Open3D visualizer with picking for drag-select simulation."""
    mesh = o3d.io.read_triangle_mesh(mesh_path)
    mesh.compute_vertex_normals()
    
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window(window_name=window_name, width=1280, height=720)
    vis.add_geometry(mesh)
    vis.run()  # User selects points (Shift + click or rectangle in editing mode)
    vis.destroy_window()
    
    picked_points = np.asarray(vis.get_picked_points())  # Indices of selected points
    print(f"Selected {len(picked_points)} points via GUI.")
    if len(picked_points) < 10:
        print("WARNING: Few points selected - accuracy may suffer.")
    
    # Save for reuse
    save_selection(mesh_path, picked_points, "plane1")  # or cyl
    return picked_points, mesh

# Update multi_datum_align to accept GUI flow
def run_alignment_gui(input_path: str, output_path: str = "aligned.stl"):
    """Full GUI-driven alignment."""
    app = QApplication(sys.argv)  # For PySide
    print("Opening GUI picker for Primary Plane (XY)...")
    plane1_idx, _ = gui_pick_points(input_path)
    
    mesh = load_mesh(input_path)
    aligned = multi_datum_align(mesh, plane1_indices=plane1_idx.tolist())
    
    o3d.io.write_triangle_mesh(output_path, aligned)
    print(f"✅ GUI Aligned mesh saved: {output_path}")
    return aligned
