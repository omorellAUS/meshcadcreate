# MeshCADCreate

**Ultimate Mesh-to-Parametric CAD Tool for Fusion 360**

A blunt, engineering-grade reverse engineering pipeline that converts noisy .STL / .OBJ / .PLY scans (up to 300k faces) into high-quality quad-dominant remeshes and **editable parametric B-rep / prismatic solids**.

Designed specifically for real workflows: Revopoint foot/shoe last scanning (Perth Resoles), mechanical parts (Mining, machinery, turbines, compressors parts and componnents), and hybrid organic/prismatic geometry.

## Core Features (Building Now)

- **Alignment-First (Mandatory Phase 0)**: Drag-select surfaces → fit planes (RANSAC + metrics), align primary to XY, secondary to XZ/YZ, cylindrical axis to Z.
- **Quad Remeshing**: Edge preservation, flat region triangle combining (better than Fusion's mesh tab).
- **Multi-Axis Cross-Sections**: Configurable manual counts (e.g. 15 on X, 5 on Y, 10 on Z — up to ~30 per axis) + support for 45° and adaptive spacing.
- **Surfacing & Solids**: NURBS/spline fitting, lofting/extruding with parametric history. Direct Fusion 360 sketch projection + construction geometry.
- **Metrics & Guidance**: Deviation analysis (Hausdorff), curvature maps, warnings on noisy data. User-guided where full auto fails.
- **Fusion 360 Integration**: Push aligned mesh + sketches + lofts with full feature history.

This will outperform Quad Remesher + native Fusion tools for your use cases once complete.

## Quick Start (Test-Net Phase)

```bash
git clone <your-private-repo>
cd meshcadcreate
pip install -e .
meshcad --help
