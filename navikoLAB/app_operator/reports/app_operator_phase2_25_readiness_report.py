from pathlib import Path
import json
from datetime import datetime

def main():
    root = Path(__file__).resolve().parents[1]

    required_paths = {
        "permission_policy": root / "policy" / "permission_policy.py",
        "permission_integrator": root / "policy" / "permission_policy_integrator.py",
        "manual_approval_bridge": root / "approval" / "manual_approval_bridge.py",
        "decision_aware_executor": root / "approval" / "decision_aware_executor.py",
        "dry_run_pipeline": root / "approval" / "app_operator_dry_run_pipeline.py",
        "integrated_diagnostics": root / "diagnostics" / "app_operator_integrated_diagnostics.py",
        "reflection_saver": root / "reflection" / "app_operator_reflection_saver.py",
        "experience_saver": root / "experience" / "app_operator_experience_saver.py",
        "original_bridge": root / "bridge" / "app_operator_original_bridge.py",
        "adoption_request": root / "original_adoption" / "app_operator_adoption_request.py",
        "adoption_gate": root / "original_adoption" / "original_adoption_approval_gate.py",
        "adoption_plan_builder": root / "adoption_plan" / "original_adoption_plan_builder.py",
        "dry_run_validator": root / "adoption_plan" / "original_adoption_dry_run_validator.py",
    }

    path_checks = {name: path.exists() for name, path in required_paths.items()}
    missing = [name for name, ok in path_checks.items() if not ok]

    safety = {
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "original_auto_write": False,
        "original_write_executed": False,
        "requires_human_approval": True,
    }

    readiness = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-25 AppOperator Original Adoption Readiness Report",
        "readiness_result": "ready_for_human_review" if not missing else "not_ready",
        "required_path_count": len(required_paths),
        "missing_count": len(missing),
        "missing": missing,
        "path_checks": path_checks,
        "safety": safety,
        "original_adoption_allowed_now": False,
        "reason": "Ready for human review only. Original write remains disabled.",
        "next_phase": "Phase2-26 Human Review Checklist",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_path = root / "reports" / f"app_operator_phase2_25_readiness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(readiness, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-25 Readiness Report ===")
    print("状態:", readiness["status"])
    print("工程:", readiness["phase"])
    print("ReadinessResult:", readiness["readiness_result"])
    print("RequiredPathCount:", readiness["required_path_count"])
    print("MissingCount:", readiness["missing_count"])
    print("OriginalAdoptionAllowedNow:", readiness["original_adoption_allowed_now"])
    print("Reason:", readiness["reason"])
    print("dry_run:", safety["dry_run"])
    print("Real GUI Operation:", safety["real_gui_operation"])
    print("外部操作実行:", safety["external_operation"])
    print("OriginalAutoWrite:", safety["original_auto_write"])
    print("OriginalWriteExecuted:", safety["original_write_executed"])
    print("保存先:", out_path)
    print("次工程:", readiness["next_phase"])

if __name__ == "__main__":
    main()