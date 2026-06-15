"""
MeshCADCreate CLI - Main entrypoint for Version 1
"""

import argparse
import logging
import sys
import open3d as o3d
from .alignment import load_mesh, run_alignment_gui
from .remeshing import remesh_quad_dominant
from .slicing import generate_multi_axis_planes, extract_cross_sections
from .surfacing import nurbs_loft_from_sections
from .utils import compute_hausdorff_distance, create_tolerance_dialog
from .fusion_integration import push_to_fusion_parametric
from .smart_adjust import smart_adjust_loop

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="MeshCADCreate - Proprietary Mesh-to-Parametric CAD Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Full Pipeline (Recommended)
    full_p = subparsers.add_parser("full", help="Run complete workflow")
    full_p.add_argument("--input", required=True, help="Input scan file")
    full_p.add_argument("--mode", choices=["mechanical", "organic"], default="mechanical")
    full_p.add_argument("--target-faces", type=int, default=80000)
    full_p.add_argument("--adjust-tols", action="store_true", help="Open tolerance slider dialog")

    args = parser.parse_args()

    if args.command == "full":
        logging.info("=== Starting MeshCADCreate Full Pipeline ===")
        
        if args.adjust_tols:
            tolerances = create_tolerance_dialog()
            logging.info(f"Tolerances set: Plane={tolerances.plane_max_dev}mm, Cylinder={tolerances.cylinder_max_res}mm")

        # Alignment
        aligned_path = "aligned.stl"
        run_alignment_gui(args.input, aligned_path)
        
        # Remeshing
        remeshed_path = remesh_quad_dominant(aligned_path, args.target_faces)
        compute_hausdorff_distance(aligned_path, remeshed_path)
        
        # Slicing + Loft
        mesh = o3d.io.read_triangle_mesh(remeshed_path)
        planes = generate_multi_axis_planes(mesh, adaptive=True)
        sections = extract_cross_sections(remeshed_path, planes)
        lofted = nurbs_loft_from_sections(sections, mode=args.mode)
        
        # Fusion Push
        push_to_fusion_parametric(remeshed_path, sections)
        
        logging.info("=== Pipeline Complete ===")
        logging.info("Check deviation_map.ply for metrology results")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
