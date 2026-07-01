from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.original_adoption_dry_run_package_builder import OriginalAdoptionDryRunPackageBuilder

class OriginalAdoptionPackageValidator:
    def __init__(self, validation_dir=None):
        self.validation_dir = Path(validation_dir or Path(__file__).resolve().parent / "package_validations")
        self.validation_dir.mkdir(parents=True, exist_ok=True)

    def validate(self, package):
        safety = package.get("safety_conditions", {})
        included_modules = package.get("included_modules", [])

        checks = {
            "package_status_packaged": package.get("status") == "packaged",
            "package_type_dry_run": package.get("package_type") == "original_adoption_dry_run",
            "included_modules_present": len(included_modules) >= 10,
            "dry_run_true": safety.get("dry_run") is True,
            "external_operation_false": safety.get("external_operation") is False,
            "real_gui_operation_false": safety.get("real_gui_operation") is False,
            "original_auto_write_false": safety.get("original_auto_write") is False,
            "original_write_executed_false": safety.get("original_write_executed") is False,
            "human_review_record_required": safety.get("human_review_record_required") is True,
            "adoption_allowed_false": package.get("adoption_allowed") is False,
        }

        failed = [name for name, ok in checks.items() if not ok]

        result = {
            "status": "passed" if not failed else "failed",
            "phase": "Post-v2.0 Phase2-29 Original Adoption DryRun Package Validator",
            "checks": checks,
            "failed_count": len(failed),
            "failed": failed,
            "package_valid": len(failed) == 0,
            "adoption_allowed": False,
            "original_write_executed": False,
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "validated_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.validation_dir / f"original_adoption_package_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        return result, str(path)

    def validate_new_package(self):
        builder = OriginalAdoptionDryRunPackageBuilder()
        package, package_path = builder.build_package()
        result, result_path = self.validate(package)
        result["package_path"] = package_path
        return result, result_path