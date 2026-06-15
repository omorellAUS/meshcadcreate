"""Command line interface for MeshCADCreate."""
import argparse
import sys
import open3d as o3d
from .alignment import load_mesh, multi_datum_align
from .slicing import generate_multi_axis_planes

def main():
    parser = argparse.ArgumentParser(description="MeshCADCreate - Proprietary Mesh-to-Parametric Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Align command
    align_parser = subparsers.add_parser("align", help="Datum alignment (plane + cylinder)")
    align_parser.add_argument("--input", required=True, help="Input mesh file")
    align_parser.add_argument("--output", default="aligned.stl")
    align_parser.add_argument("--plane1", nargs="*", type=int, default=[], help="Point indices for primary plane (XY)")
    align_parser.add_argument("--cyl", nargs="*", type=int, default=[], help="Point indices for cylinder axis (Z)")

    # Slice command (post-alignment)
    slice_parser = subparsers.add_parser("slice", help="Multi-axis cross sections")
    slice_parser.add_argument("--input", required=True)
    slice_parser.add_argument("--num-x", type=int, default=10)
    slice_parser.add_argument("--num-y", type=int, default=5)
    slice_parser.add_argument("--num-z", type=int, default=10)
    slice_parser.add_argument("--adaptive", action="store_true")

    args = parser.parse_args()

    if args.command == "align":
        mesh = load_mesh(args.input)
        if not args.plane1:
            print("WARNING: No plane1 indices provided. Using simulated selection for testing.")
            # Simulate for now
            points = np.asarray(mesh.vertices)
            args.plane1 = list(range(min(200, len(points))))
        aligned = multi_datum_align(mesh, plane1_indices=args.plane1, cyl_indices=args.cyl if args.cyl else None)
        o3d.io.write_triangle_mesh(args.output, aligned)
        print(f"✅ Aligned mesh saved: {args.output}")

    elif args.command == "slice":
        mesh = o3d.io.read_triangle_mesh(args.input)
        planes = generate_multi_axis_planes(mesh, args.num_x, args.num_y, args.num_z, adaptive=args.adaptive)
        print("Cross-sections generated. Next: extract profiles + loft.")

if __name__ == "__main__":
    main()
