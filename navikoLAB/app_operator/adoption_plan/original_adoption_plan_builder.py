from pathlib import Path
import json
from datetime import datetime

class OriginalAdoptionPlanBuilder:
    def __init__(self, plan_dir=None):
        self.plan_dir = Path(plan_dir or Path(__file__).resolve().parent)
        self.plan_dir.mkdir(parents=True, exist_ok=True)

    def build_plan(self):
        plan = {
            "status": "planned",
            "phase": "Post-v2.0 Phase2-23 Original Adoption Plan Builder",
            "target": "Original Naviko",
            "source": "AppOperator Package",
            "adoption_mode": "plan_only",
            "adoption_allowed": False,
            "requires_human_approval": True,
            "original_auto_write": False,
            "original_write_executed": False,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "adoption_items": [
                {
                    "name": "PermissionPolicy",
                    "purpose": "Classify actions into Level1-Level4 approval levels",
                    "risk": "low",
                    "adoption_type": "new module reference",
                },
                {
                    "name": "Approval flow",
                    "purpose": "Require approval before executor operations",
                    "risk": "medium",
                    "adoption_type": "controlled integration",
                },
                {
                    "name": "DecisionAwareExecutor",
                    "purpose": "Execute only approved dry_run operations",
                    "risk": "medium",
                    "adoption_type": "executor gate",
                },
                {
                    "name": "AppOperatorDryRunPipeline",
                    "purpose": "Connect PermissionPolicy, approval, and executor",
                    "risk": "medium",
                    "adoption_type": "pipeline bridge",
                },
                {
                    "name": "Reflection/Experience save",
                    "purpose": "Save AppOperator diagnostics as learning material",
                    "risk": "low",
                    "adoption_type": "knowledge integration",
                },
            ],
            "blocked_until": [
                "Human approval completed",
                "Original backup created",
                "Original syntax check passed",
                "Adoption dry_run passed",
                "Rollback route confirmed",
            ],
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.plan_dir / f"original_adoption_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        return plan, str(path)