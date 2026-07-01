from pathlib import Path
import json
from datetime import datetime

def main():
    root = Path(__file__).resolve().parents[1]

    package_items = {
        "approval": [
            "approval_decision_manager.py",
            "approved_operation_executor.py",
            "approval_log_manager.py",
            "manual_approval_bridge.py",
            "decision_aware_executor.py",
            "app_operator_dry_run_pipeline.py",
        ],
        "executors": [
            "real_gui_operation_executor.py",
        ],
        "policy": [
            "permission_policy.py",
            "permission_policy_integrator.py",
        ],
        "diagnostics": [
            "app_operator_integrated_diagnostics.py",
        ],
        "reflection": [
            "app_operator_reflection_saver.py",
        ],
        "experience": [
            "app_operator_experience_saver.py",
        ],
        "bridge": [
            "app_operator_original_bridge.py",
        ],
        "original_adoption": [
            "app_operator_adoption_request.py",
            "original_adoption_approval_gate.py",
            "human_approved_adoption_dry_run.py",
        ],
    }

    checks = {}
    missing = []

    for folder, files in package_items.items():
        checks[folder] = {}
        for file_name in files:
            exists = (root / folder / file_name).exists()
            checks[folder][file_name] = exists
            if not exists:
                missing.append(f"{folder}/{file_name}")

    report_files = sorted((root / "reports").glob("app_operator_phase2_*"))
    latest_reports = [str(p) for p in report_files[-20:]]

    summary = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-22 AppOperator Original Adoption Package Summary",
        "package_complete": len(missing) == 0,
        "missing_count": len(missing),
        "missing": missing,
        "package_checks": checks,
        "latest_reports": latest_reports,
        "safety_state": {
            "dry_run": True,
            "external_operation": False,
            "real_gui_operation": False,
            "original_auto_write": False,
            "original_write_executed": False,
            "human_approval_required": True,
        },
        "ready_for_next": "Original adoption planning only. No direct write.",
        "next_phase": "Phase2-23 Original Adoption Plan Builder",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = root / "reports"
    out_path = out_dir / f"app_operator_phase2_22_package_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-22 Package Summary ===")
    print("状態:", summary["status"])
    print("工程:", summary["phase"])
    print("PackageComplete:", summary["package_complete"])
    print("MissingCount:", summary["missing_count"])
    print("dry_run:", summary["safety_state"]["dry_run"])
    print("Real GUI Operation:", summary["safety_state"]["real_gui_operation"])
    print("外部操作実行:", summary["safety_state"]["external_operation"])
    print("OriginalAutoWrite:", summary["safety_state"]["original_auto_write"])
    print("OriginalWriteExecuted:", summary["safety_state"]["original_write_executed"])
    print("保存先:", out_path)
    print("次工程:", summary["next_phase"])

if __name__ == "__main__":
    main()