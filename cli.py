# src/meshcadcreate/cli.py
import argparse
from .alignment import multi_datum_align, load_mesh
from .slicing import generate_multi_axis_planes

def main():
    parser = argparse.ArgumentParser(description="MeshCADCreate - Proprietary RE Tool")
    subparsers = parser.add_subparsers(dest="command")
    
    # Align
    a = subparsers.add_parser("align")
    a.add_argument("--input", required=True)
    a.add_argument("--output", default="aligned.stl")
    a.add_argument("--plane1", nargs="+", type=int, help="Point indices for primary plane")
    
    # Slice
    s = subparsers.add_parser("slice")
    s.add_argument("--input", required=True)
    s.add_argument("--num-x", type=int, default=10)
    s.add_argument("--num-y", type=int, default=5)
    s.add_argument("--num-z", type=int, default=10)
    
    args = parser.parse_args()
    
    if args.command == "align":
        mesh = load_mesh(args.input)
        # Example usage - replace with real indices from GUI
        aligned = multi_datum_align(mesh, plane1_indices=args.plane1 or list(range(50)))
        o3d.io.write_triangle_mesh(args.output, aligned)
    elif args.command == "slice":
        planes = generate_multi_axis_planes(o3d.io.read_triangle_mesh(args.input), args.num_x, args.num_y, args.num_z)

if __name__ == "__main__":
    main()
