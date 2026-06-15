import open3d as o3d
import numpy as np
from scipy.spatial import ConvexHull
import trimesh
from typing import Tuple, List

def load_mesh(file_path: str):
    """Load and preprocess."""
    mesh = o3d.io.read_triangle_mesh(file_path)
    mesh.compute_vertex_normals()
    print(f"Loaded mesh: {len(mesh.vertices)} vertices, {len(mesh.triangles)} faces")
    return mesh

def ransac_plane_fit(points: np.ndarray, threshold: float = 0.01, max_iterations: int = 1000) -> Tuple[np.ndarray, np.ndarray, float]:
    """RANSAC plane fit with deviation metric."""
    best_normal = None
    best_centroid = None
    best_inliers = 0
    for _ in range(max_iterations):
        sample = points[np.random.choice(len(points), 3, replace=False)]
        centroid = np.mean(sample, axis=0)
        normal = np.cross(sample[1] - sample[0], sample[2] - sample[0])
        normal /= np.linalg.norm(normal)
        dists = np.abs(np.dot(points - centroid, normal))
        inliers = np.sum(dists < threshold)
        if inliers > best_inliers:
            best_inliers = inliers
            best_normal = normal
            best_centroid = centroid
    max_dev = np.max(np.abs(np.dot(points - best_centroid, best_normal)))
    print(f"Plane fit - max deviation: {max_dev:.4f} mm | Inliers: {best_inliers}/{len(points)}")
    if max_dev > 0.2:
        print("WARNING: High deviation - noisy selection or non-planar surface.")
    return best_centroid, best_normal, max_dev

def fit_cylinder_axis(points: np.ndarray) -> Tuple[np.ndarray, np.ndarray, float]:
    """Simple PCA-based cylinder axis approx + residual."""
    centroid = np.mean(points, axis=0)
    _, _, vh = np.linalg.svd(points - centroid)
    direction = vh[0]
    # Residual (distance to axis)
    residuals = np.linalg.norm(np.cross(points - centroid, direction), axis=1)
    max_res = np.max(residuals)
    print(f"Cylinder axis fit - max residual: {max_res:.4f} mm")
    return centroid, direction, max_res

def align_mesh(mesh: o3d.geometry.TriangleMesh, plane_normal: np.ndarray, plane_centroid: np.ndarray, target_normal=np.array([0.,0.,1.])):
    """Align selected plane to XY."""
    R = o3d.geometry.get_rotation_matrix_from_two_vectors(plane_normal, target_normal)
    mesh.rotate(R, center=plane_centroid)
    mesh.translate(-R @ plane_centroid)
    return mesh

# Basic visualizer picker simulation (for MVP; replace with full PySide/Open3D event loop later)
def simulate_drag_select(mesh: o3d.geometry.TriangleMesh, num_points: int = 50) -> np.ndarray:
    """Simulate user selection - in real GUI, use picking."""
    points = np.asarray(mesh.sample_points_uniformly(num_points).points)
    print("Simulated drag-select: sampled points for plane/cylinder.")
    return points

# CLI-friendly main function
def run_alignment(input_path: str, output_path: str = "aligned.stl"):
    mesh = load_mesh(input_path)
    # Primary plane (XY)
    pts1 = simulate_drag_select(mesh)
    c1, n1, _ = ransac_plane_fit(pts1)
    mesh = align_mesh(mesh, n1, c1)
    # Secondary / Cylinder example
    pts_cyl = simulate_drag_select(mesh)
    _, _, res = fit_cylinder_axis(pts_cyl)
    o3d.io.write_triangle_mesh(output_path, mesh)
    print(f"Aligned mesh saved to {output_path}")
    return mesh
