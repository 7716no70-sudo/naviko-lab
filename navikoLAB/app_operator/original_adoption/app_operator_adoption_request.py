from pathlib import Path
import json
from datetime import datetime

class AppOperatorAdoptionRequest:
    def __init__(self, adoption_dir=None):
        self.adoption_dir = Path(adoption_dir or Path(__file__).resolve().parents[1] / "original_adoption")
        self.adoption_dir.mkdir(parents=True, exist_ok=True)

    def create_request(self, bridge_payload_path):
        request = {
            "status": "approval_required",
            "phase": "Post-v2.0 Phase2-18 AppOperator Original Adoption Request",
            "target": "Original Naviko",
            "source": "AppOperator",
            "bridge_payload_path": bridge_payload_path,
            "requested_items": [
                "PermissionPolicy",
                "ApprovalLogManager",
                "ManualApprovalBridge",
                "DecisionAwareExecutor",
                "AppOperatorDryRunPipeline",
                "AppOperatorIntegratedDiagnostics",
                "Reflection/Experience save",
                "Original Bridge Payload",
            ],
            "safety_conditions": [
                "Original auto-write is forbidden",
                "Human approval is required",
                "dry_run remains True",
                "real_gui_operation remains False",
                "external_operation remains False",
            ],
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "original_auto_write": False,
            "requires_human_approval": True,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.adoption_dir / f"app_operator_original_adoption_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(request, ensure_ascii=False, indent=2), encoding="utf-8")
        return request, str(path)