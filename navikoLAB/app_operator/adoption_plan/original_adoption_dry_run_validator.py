from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.adoption_plan.original_adoption_plan_builder import OriginalAdoptionPlanBuilder

class OriginalAdoptionDryRunValidator:
    def __init__(self, validation_dir=None):
        self.validation_dir = Path(validation_dir or Path(__file__).resolve().parent / "validations")
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def validate(self, plan):
        checks = {
            "plan_status_planned": plan.get("status") == "planned",
            "adoption_mode_plan_only": plan.get("adoption_mode") == "plan_only",
            "adoption_not_allowed": plan.get("adoption_allowed") is False,
            "human_approval_required": plan.get("requires_human_approval") is True,
            "original_auto_write_false": plan.get("original_auto_write") is False,
            "original_write_executed_false": plan.get("original_write_executed") is False,
            "dry_run_true": plan.get("dry_run") is True,
            "external_operation_false": plan.get("external_operation") is False,
            "real_gui_operation_false": plan.get("real_gui_operation") is False,
            "adoption_items_present": len(plan.get("adoption_items", [])) > 0,
            "blocked_until_present": len(plan.get("blocked_until", [])) > 0,
        }

        failed = [name for name, ok in checks.items() if not ok]

        result = {
            "status": "passed" if not failed else "failed",
            "phase": "Post-v2.0 Phase2-24 Original Adoption DryRun Validator",
            "checks": checks,
            "failed_count": len(failed),
            "failed": failed,
            "adoption_dry_run_valid": len(failed) == 0,
            "adoption_allowed": False,
            "original_write_executed": False,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "validated_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.validation_dir / f"original_adoption_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result, str(path)

    def validate_new_plan(self):
        builder = OriginalAdoptionPlanBuilder()
        plan, plan_path = builder.build_plan()
        result, result_path = self.validate(plan)
        result["plan_path"] = plan_path
        return result, result_path