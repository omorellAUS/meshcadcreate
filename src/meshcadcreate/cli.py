"""Command line interface for MeshCADCreate."""
import argparse
import open3d as o3d
from .alignment import run_alignment_gui, multi_datum_align, load_mesh
from .remeshing import remesh_quad_dominant
from .slicing import generate_multi_axis_planes

def main():
    parser = argparse.ArgumentParser(description="MeshCADCreate - Proprietary RE Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Align with GUI
    a = subparsers.add_parser("align", help="GUI-driven datum alignment")
    a.add_argument("--input", required=True)
    a.add_argument("--output", default="aligned.stl")

    # Remesh
    r = subparsers.add_parser("remesh", help="Quad remeshing")
    r.add_argument("--input", required=True)
    r.add_argument("--target-faces", type=int, default=80000)

    # Slice
    s = subparsers.add_parser("slice", help="Multi-axis slicing")
    s.add_argument("--input", required=True)
    s.add_argument("--num-x", type=int, default=15)
    s.add_argument("--num-y", type=int, default=5)
    s.add_argument("--num-z", type=int, default=10)

    args = parser.parse_args()

    if args.command == "align":
        run_alignment_gui(args.input, args.output)
    elif args.command == "remesh":
        remesh_quad_dominant(args.input, args.target_faces)
    elif args.command == "slice":
        mesh = o3d.io.read_triangle_mesh(args.input)
        planes = generate_multi_axis_planes(mesh, args.num_x, args.num_y, args.num_z)
        print("Planes ready for cross-section extraction.")

if __name__ == "__main__":
    main()
