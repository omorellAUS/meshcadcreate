"""Shared utilities (deviation, saving selections, etc.)."""
import numpy as np
import json
from pathlib import Path

def save_selection(mesh_path: str, indices: list, label: str = "selection"):
    """Save picked indices for reuse."""
    data = {"mesh": mesh_path, "indices": indices.tolist() if hasattr(indices, 'tolist') else indices}
    path = Path(mesh_path).with_name(f"{label}_indices.json")
    with open(path, 'w') as f:
        json.dump(data, f)
    print(f"Saved selection to {path}")

def compute_hausdorff_distance(original: o3d.geometry.TriangleMesh, processed: o3d.geometry.TriangleMesh):
    """Deviation metric."""
    dist = original.compute_point_cloud_distance(processed)
    print(f"Hausdorff deviation: max={max(dist):.4f} mm")
    return max(dist)
