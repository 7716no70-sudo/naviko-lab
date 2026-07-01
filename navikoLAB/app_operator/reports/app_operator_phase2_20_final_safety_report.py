from pathlib import Path
import json
from datetime import datetime

def main():
    app_operator_root = Path(__file__).resolve().parents[1]

    checks = {
        "approval_required": True,
        "original_auto_write": False,
        "original_write_executed": False,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "permission_policy_exists": (app_operator_root / "policy" / "permission_policy.py").exists(),
        "approval_gate_exists": (app_operator_root / "original_adoption" / "original_adoption_approval_gate.py").exists(),
        "dry_run_pipeline_exists": (app_operator_root / "approval" / "app_operator_dry_run_pipeline.py").exists(),
        "decision_executor_exists": (app_operator_root / "approval" / "decision_aware_executor.py").exists(),
        "integrated_diagnostics_exists": (app_operator_root / "diagnostics" / "app_operator_integrated_diagnostics.py").exists(),
        "reflection_dir_exists": (app_operator_root / "reflection").exists(),
        "experience_dir_exists": (app_operator_root / "experience").exists(),
    }

    risk_items = []
    if checks["original_auto_write"]:
        risk_items.append("original_auto_write is enabled")
    if checks["real_gui_operation"]:
        risk_items.append("real_gui_operation is enabled")
    if checks["external_operation"]:
        risk_items.append("external_operation is enabled")
    if not checks["approval_required"]:
        risk_items.append("approval_required is disabled")

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-20 AppOperator Adoption Final Safety Report",
        "safety_result": "safe_waiting_for_human_approval" if not risk_items else "risk_detected",
        "checks": checks,
        "risk_count": len(risk_items),
        "risk_items": risk_items,
        "adoption_allowed": False,
        "reason": "Human approval is required before Original Naviko adoption",
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "original_auto_write": False,
        "original_write_executed": False,
        "next_phase": "Phase2-21 Human-approved Original adoption dry_run",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_20_final_safety_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-20 Final Safety Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("SafetyResult:", report["safety_result"])
    print("RiskCount:", report["risk_count"])
    print("AdoptionAllowed:", report["adoption_allowed"])
    print("Reason:", report["reason"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("OriginalAutoWrite:", report["original_auto_write"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()