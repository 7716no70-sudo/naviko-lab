from pathlib import Path
import json
from datetime import datetime

class OriginalAdoptionDryRunPackageBuilder:
    def __init__(self, package_dir=None):
        self.package_dir = Path(package_dir or Path(__file__).resolve().parent / "dry_run_packages")
        self.package_dir.mkdir(parents=True, exist_ok=True)

    def build_package(self):
        package = {
            "status": "packaged",
            "phase": "Post-v2.0 Phase2-28 Original Adoption DryRun Package Builder",
            "package_type": "original_adoption_dry_run",
            "target": "Original Naviko",
            "source": "AppOperator Package",
            "included_modules": [
                "policy/permission_policy.py",
                "policy/permission_policy_integrator.py",
                "approval/manual_approval_bridge.py",
                "approval/decision_aware_executor.py",
                "approval/app_operator_dry_run_pipeline.py",
                "diagnostics/app_operator_integrated_diagnostics.py",
                "reflection/app_operator_reflection_saver.py",
                "experience/app_operator_experience_saver.py",
                "bridge/app_operator_original_bridge.py",
                "original_adoption/app_operator_adoption_request.py",
                "original_adoption/original_adoption_approval_gate.py",
                "original_adoption/human_review_approval_record.py",
            ],
            "safety_conditions": {
                "dry_run": True,
                "external_operation": False,
                "real_gui_operation": False,
                "original_auto_write": False,
                "original_write_executed": False,
                "human_review_record_required": True,
            },
            "adoption_allowed": False,
            "reason": "Dry-run package only. Original write is disabled.",
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.package_dir / f"original_adoption_dry_run_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
        return package, str(path)