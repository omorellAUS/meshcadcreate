"""
MeshCADCreate Package Initialization (Version 1.0)
"""

__version__ = "1.0.0"
__author__ = "Oliver Ross Morell (Perth Resoles)"
__description__ = "Proprietary Mesh-to-Parametric CAD Tool for Fusion 360"

# Import main components for easy access
from .cli import main
from .utils import (
    Tolerances,
    create_tolerance_dialog,
    inspect_and_repair_mesh,
    compute_hausdorff_distance,
    deviation_color_map
)
from .alignment import load_mesh, run_alignment_gui
from .remeshing import remesh_quad_dominant
from .slicing import generate_multi_axis_planes, extract_cross_sections
from .surfacing import nurbs_loft_from_sections
from .fusion_integration import push_to_fusion_parametric
from .smart_adjust import smart_adjust_loop
from .metrology import run_full_metrology, metrology_gui_picker

# Make key functions available at package level
__all__ = [
    'main',
    'Tolerances',
    'create_tolerance_dialog',
    'load_mesh',
    'run_alignment_gui',
    'remesh_quad_dominant',
    'generate_multi_axis_planes',
    'extract_cross_sections',
    'nurbs_loft_from_sections',
    'push_to_fusion_parametric',
    'smart_adjust_loop',
    'run_full_metrology',
    'metrology_gui_picker'
]

print(f"MeshCADCreate v{__version__} initialized successfully.")
print("Ready for .app build or 'meshcad full --input your_scan.stl --mode mechanical'")
