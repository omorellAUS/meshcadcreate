"""Utilities: deviation, IO, metrics."""
import numpy as np
import open3d as o3d
import json
from pathlib import Path

def save_selection(mesh_path: str, indices: list, label: str = "selection"):
    data = {"mesh": mesh_path, "indices": indices}
    path = Path(mesh_path).with_name(f"{label}_indices.json")
    with open(path, 'w') as f:
        json.dump(data, f)
    print(f"Saved selection: {path}")

def compute_hausdorff_distance(original_path: str, processed_path: str):
    """Hausdorff + max deviation metric."""
    orig = o3d.io.read_triangle_mesh(original_path)
    proc = o3d.io.read_triangle_mesh(processed_path)
    dist = orig.compute_point_cloud_distance(proc)
    max_d = float(np.max(dist))
    mean_d = float(np.mean(dist))
    print(f"Hausdorff deviation: max={max_d:.4f} mm | mean={mean_d:.4f} mm")
    if max_d > 0.2:
        print("WARNING: High deviation - consider more planes or better remeshing.")
    return max_d

def compute_plane_deviation(plane_centroid, plane_normal, points):
    dists = np.abs(np.dot(points - plane_centroid, plane_normal))
    return float(np.max(dists))
