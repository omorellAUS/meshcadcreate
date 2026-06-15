import argparse
from .alignment import run_alignment

def main():
    parser = argparse.ArgumentParser(description="MeshCADCreate CLI")
    sub = parser.add_subparsers(dest="command")
    
    align_p = sub.add_parser("align")
    align_p.add_argument("--input", required=True)
    align_p.add_argument("--output", default="aligned.stl")
    
    args = parser.parse_args()
    if args.command == "align":
        run_alignment(args.input, args.output)

if __name__ == "__main__":
    main()
