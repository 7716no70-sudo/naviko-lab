from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.approval.approval_log_manager import ApprovalLogManager
from navikoLAB.app_operator.policy.permission_policy_integrator import PermissionPolicyIntegrator

def main():
    log_manager = ApprovalLogManager()
    integrator = PermissionPolicyIntegrator()

    operations = [
        {"action": "report_generate", "approval_status": "auto_dry_run"},
        {"action": "browser_search", "approval_status": "simple_approval_required"},
        {"action": "mouse_click", "approval_status": "normal_approval_required"},
        {"action": "delete_file", "approval_status": "strict_approval_required"},
    ]

    saved_logs = []
    for op in operations:
        integrated = integrator.apply(op)
        saved_logs.append(log_manager.save_log(integrated))

    summary = log_manager.summarize()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-11 Approval UI / Approval Log Manager",
        "saved_log_count": len(saved_logs),
        "saved_logs": saved_logs,
        "summary": summary,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-12 Approval UI bridge / manual decision input",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_11_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-11 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("SavedLogCount:", report["saved_log_count"])
    print("ApprovalLogCount:", summary["log_count"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()