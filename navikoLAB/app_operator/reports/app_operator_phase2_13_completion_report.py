from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.approval.decision_aware_executor import DecisionAwareExecutor
from navikoLAB.app_operator.approval.manual_approval_bridge import ManualApprovalBridge

def main():
    bridge = ManualApprovalBridge()
    executor = DecisionAwareExecutor(dry_run=True)

    test_items = [
        ("req_report_generate_13", "report_generate", "approve", "approved dry_run test"),
        ("req_mouse_click_13", "mouse_click", "hold", "waiting for human approval"),
        ("req_delete_file_13", "delete_file", "reject", "dangerous action rejected"),
    ]

    decisions = []
    execution_results = []

    for request_id, action, decision, reason in test_items:
        record, path = bridge.create_decision(request_id, action, decision, reason)
        decisions.append({"record": record, "path": path})
        execution_results.append(executor.execute_with_decision(record))

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-13 ApprovedOperationExecutor decision integration",
        "decision_count": len(decisions),
        "execution_count": len(execution_results),
        "decisions": decisions,
        "execution_results": execution_results,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-14 AppOperator End-to-End dry_run pipeline",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_13_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-13 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("DecisionCount:", report["decision_count"])
    print("ExecutionCount:", report["execution_count"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()