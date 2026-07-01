from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.original_adoption_package_validator import OriginalAdoptionPackageValidator

def main():
    validator = OriginalAdoptionPackageValidator()
    result, result_path = validator.validate_new_package()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-29 Original Adoption DryRun Package Validator",
        "validation_status": result["status"],
        "package_valid": result["package_valid"],
        "failed_count": result["failed_count"],
        "failed": result["failed"],
        "adoption_allowed": result["adoption_allowed"],
        "original_write_executed": result["original_write_executed"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "validation_path": result_path,
        "next_phase": "Phase2-30 AppOperator Original Adoption Final Package Report",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_path = Path(__file__).resolve().parent / f"app_operator_phase2_29_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-29 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ValidationStatus:", report["validation_status"])
    print("PackageValid:", report["package_valid"])
    print("FailedCount:", report["failed_count"])
    print("AdoptionAllowed:", report["adoption_allowed"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Validation保存先:", result_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()