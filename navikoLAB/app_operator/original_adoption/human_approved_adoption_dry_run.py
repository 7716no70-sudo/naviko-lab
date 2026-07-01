from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.original_adoption_approval_gate import OriginalAdoptionApprovalGate

class HumanApprovedAdoptionDryRun:
    def __init__(self, output_dir=None):
        self.output_dir = Path(output_dir or Path(__file__).resolve().parent / "dry_run_adoption")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        approved_request = {
            "status": "human_approved",
            "source": "AppOperator",
            "target": "Original Naviko",
            "requires_human_approval": True,
            "original_auto_write": False,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
        }

        gate = OriginalAdoptionApprovalGate()
        gate_result, gate_path = gate.evaluate(approved_request)

        result = {
            "status": "completed",
            "phase": "Post-v2.0 Phase2-21 Human-approved Original adoption dry_run",
            "gate_status": gate_result["gate_status"],
            "gate_path": gate_path,
            "adoption_dry_run_allowed": gate_result["gate_status"] == "approved_for_dry_run_adoption",
            "original_write_executed": False,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.output_dir / f"human_approved_adoption_dry_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result, str(path)