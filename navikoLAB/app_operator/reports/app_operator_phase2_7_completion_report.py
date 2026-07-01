from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.approval.approval_decision_manager import ApprovalDecisionManager
from navikoLAB.app_operator.approval.approved_operation_executor import ApprovedOperationExecutor

def main():
    manager = ApprovalDecisionManager()
    executor = ApprovedOperationExecutor()

    decisions = manager.review_requests()
    executions = [executor.execute(d) for d in decisions]

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-7 Approval Request Review",
        "approval_requests": len(decisions),
        "decisions": decisions,
        "executions": executions,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Post-v2.0 Phase2-8 Real GUI Automation",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_7_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-7 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("ApprovalRequests:", report["approval_requests"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()