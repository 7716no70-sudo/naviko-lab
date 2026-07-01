from pathlib import Path
import json
from datetime import datetime

class AppOperatorReflectionSaver:
    def __init__(self, reflection_dir=None):
        self.reflection_dir = Path(reflection_dir or Path(__file__).resolve().parents[1] / "reflection")
        self.reflection_dir.mkdir(parents=True, exist_ok=True)

    def save(self, diagnostic_result):
        reflection = {
            "status": "completed",
            "source": "AppOperatorIntegratedDiagnostics",
            "summary": {
                "dir_all_ok": diagnostic_result.get("dir_all_ok"),
                "policy_check_count": diagnostic_result.get("policy_check_count"),
                "pipeline_check_count": diagnostic_result.get("pipeline_check_count"),
                "dry_run": diagnostic_result.get("dry_run"),
                "external_operation": diagnostic_result.get("external_operation"),
                "real_gui_operation": diagnostic_result.get("real_gui_operation"),
            },
            "good_points": [
                "PermissionPolicy is connected",
                "Approval decision flow is connected",
                "DecisionAwareExecutor blocks non-approved operations",
                "End-to-End dry_run pipeline completed",
            ],
            "next_improvements": [
                "Add manual approval UI",
                "Add real GUI executor behind approval gate",
                "Strengthen Level4 strict approval",
            ],
            "saved_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.reflection_dir / f"app_operator_reflection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(reflection, ensure_ascii=False, indent=2), encoding="utf-8")
        return reflection, str(path)