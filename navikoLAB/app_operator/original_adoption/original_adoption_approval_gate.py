from pathlib import Path
import json
from datetime import datetime

class OriginalAdoptionApprovalGate:
    def __init__(self, gate_dir=None):
        self.gate_dir = Path(gate_dir or Path(__file__).resolve().parent / "approval_gate")
        self.gate_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(self, adoption_request):
        status = adoption_request.get("status")
        requires_human_approval = adoption_request.get("requires_human_approval", True)
        original_auto_write = adoption_request.get("original_auto_write", False)

        if original_auto_write:
            gate_status = "blocked"
            reason = "original_auto_write must be False"
        elif requires_human_approval and status != "human_approved":
            gate_status = "approval_required"
            reason = "human approval is required before Original adoption"
        elif status == "human_approved":
            gate_status = "approved_for_dry_run_adoption"
            reason = "human approved, dry_run adoption only"
        else:
            gate_status = "approval_required"
            reason = "default approval required"

        result = {
            "gate_status": gate_status,
            "reason": reason,
            "input_status": status,
            "requires_human_approval": requires_human_approval,
            "original_auto_write": original_auto_write,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "original_write_executed": False,
            "checked_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.gate_dir / f"original_adoption_gate_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result, str(path)