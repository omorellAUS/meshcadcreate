# MeshCADCreate

**Ultimate Proprietary Mesh-to-Parametric CAD Tool for Fusion 360**

Converts noisy .STL/.OBJ/.PLY scans (up to 300k faces) into quad-dominant remeshes and editable parametric B-rep solids. Designed for mechanical precision Machinery Parts and organic parts (shoe lasts).

## Current Realistic Workflow
See `docs/workflow.md` (or the itemised list in recent development notes).

## Installation
```bash
pip install -e .
# For full NURBS/B-Rep:
conda install -c conda-forge pythonocc-core
