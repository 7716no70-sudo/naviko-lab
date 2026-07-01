from pathlib import Path
import json
from datetime import datetime

class AppOperatorOriginalBridge:
    def __init__(self, bridge_dir=None):
        self.bridge_dir = Path(bridge_dir or Path(__file__).resolve().parents[1] / "bridge")
        self.bridge_dir.mkdir(parents=True, exist_ok=True)

    def create_payload(self, diagnostic_result=None, reflection_path=None, experience_path=None):
        payload = {
            "status": "ready_for_original_review",
            "source": "AppOperator",
            "target": "Original Naviko",
            "phase": "Post-v2.0 Phase2-17 Original Bridge integration for AppOperator",
            "diagnostic_summary": {
                "status": diagnostic_result.get("status") if diagnostic_result else None,
                "dir_all_ok": diagnostic_result.get("dir_all_ok") if diagnostic_result else None,
                "policy_check_count": diagnostic_result.get("policy_check_count") if diagnostic_result else None,
                "pipeline_check_count": diagnostic_result.get("pipeline_check_count") if diagnostic_result else None,
            },
            "reflection_path": reflection_path,
            "experience_path": experience_path,
            "requires_human_approval": True,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "original_auto_write": False,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.bridge_dir / f"app_operator_original_bridge_payload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return payload, str(path)