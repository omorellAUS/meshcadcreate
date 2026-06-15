# MeshCADCreate

**Ultimate Proprietary Mesh-to-Parametric CAD Tool for Fusion 360**

Converts noisy Revopoint .STL/.OBJ/.PLY scans (up to 300k faces) into quad-dominant remeshes and editable parametric B-rep/prismatic solids. Tailored for shoe lasts (Perth Resoles) and mechanical parts (BHP).

## Features
- Alignment-First (planes + cylinder datums)
- Instant Meshes quad remeshing (or robust fallback)
- Multi-axis configurable slicing (adaptive)
- NURBS lofting / surfacing
- Deviation metrics everywhere
- Fusion 360 export skeleton

## Installation
```bash
pip install -e .
# For pythonocc NURBS (recommended):
# conda install -c conda-forge pythonocc-core
