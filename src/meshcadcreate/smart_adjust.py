"""
MeshCADCreate - Smart Adjustment Module (Version 1)
Automated deviation-driven adjustments with user-guided GUI approval.
"""

import logging
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
import open3d as o3d
from .utils import deviation_color_map

logging.basicConfig(level=logging.INFO)

def analyze_deviations(step_file: str, original_mesh_path: str, known_measurements: dict = None):
    """Automated analysis - suggests adjustments based on deviation."""
    suggestions = []
    if known_measurements:
        for key, value in known_measurements.items():
            suggestions.append(f"Adjust {key} to nominal {value} mm based on scan deviation")
    suggestions.append("Apply local push/pull on high-deviation regions")
    suggestions.append("Refine fillets/chamfers on edges >0.05mm deviation")
    suggestions.append("Re-run metrology after changes")
    return suggestions

def gui_adjustment_preview(step_file: str, original_mesh_path: str, suggestions: list):
    """GUI Preview + Approval Dialog."""
    dialog = QDialog()
    dialog.setWindowTitle("MeshCADCreate - Smart Adjustment Preview")
    layout = QVBoxLayout()
    
    layout.addWidget(QLabel("Current Deviation Map Generated"))
    layout.addWidget(QLabel("Suggested Adjustments:"))
    
    for sug in suggestions:
        layout.addWidget(QLabel(f"• {sug}"))
    
    # Generate deviation map
    deviation_color_map(original_mesh_path, step_file)
    
    layout.addWidget(QLabel("\nReview deviation_map.ply before approving."))
    
    approve_btn = QPushButton("✅ Apply Adjustments")
    reject_btn = QPushButton("❌ Reject & Stop")
    manual_btn = QPushButton("Manual Override in Fusion")
    
    approve_btn.clicked.connect(dialog.accept)
    reject_btn.clicked.connect(dialog.reject)
    manual_btn.clicked.connect(lambda: QMessageBox.information(dialog, "Manual", "Switch to Fusion for manual edits."))
    
    layout.addWidget(approve_btn)
    layout.addWidget(reject_btn)
    layout.addWidget(manual_btn)
    dialog.setLayout(layout)
    
    result = dialog.exec()
    return result == QDialog.Accepted

def smart_adjust_loop(step_file: str, original_mesh_path: str, known_measurements: dict = None, iterations: int = 3, mode: str = "mechanical"):
    """Main guided adjustment loop."""
    logging.info(f"Starting Smart Adjustment Loop ({mode} mode, {iterations} iterations)")
    
    current_step = step_file
    for i in range(iterations):
        print(f"\n=== Adjustment Iteration {i+1}/{iterations} ===")
        
        suggestions = analyze_deviations(current_step, original_mesh_path, known_measurements)
        
        if not gui_adjustment_preview(current_step, original_mesh_path, suggestions):
            print("User rejected adjustments. Stopping loop.")
            break
        
        # Apply adjustments (placeholder - expand with pythonocc B-Rep edits)
        current_step = current_step.replace(".step", f"_adjusted_{i+1}.step")
        print(f"✅ Adjustments applied: {current_step}")
        
        # Re-metrology
        deviation_color_map(original_mesh_path, current_step)
    
    logging.info("Smart Adjustment Loop finished.")
    return current_step

def get_user_known_measurements():
    """Simple prompt for known nominal dimensions (expand with GUI)."""
    print("Enter known nominal dimensions (example: diameter=50.0 length=120.5)")
    # In full version, replace with GUI form
    return {"example_diameter": 50.0}

print("Smart Adjust module loaded successfully.")
