from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.adoption_plan.original_adoption_dry_run_validator import OriginalAdoptionDryRunValidator

def main():
    validator = OriginalAdoptionDryRunValidator()
    result, result_path = validator.validate_new_plan()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-24 Original Adoption DryRun Validator",
        "validation_status": result["status"],
        "adoption_dry_run_valid": result["adoption_dry_run_valid"],
        "failed_count": result["failed_count"],
        "failed": result["failed"],
        "adoption_allowed": result["adoption_allowed"],
        "original_write_executed": result["original_write_executed"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "validation_path": result_path,
        "next_phase": "Phase2-25 AppOperator Original Adoption Readiness Report",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parents[1] / "reports"
    out_path = out_dir / f"app_operator_phase2_24_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-24 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ValidationStatus:", report["validation_status"])
    print("AdoptionDryRunValid:", report["adoption_dry_run_valid"])
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