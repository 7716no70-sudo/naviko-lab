from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.approval.manual_approval_bridge import ManualApprovalBridge

def main():
    bridge = ManualApprovalBridge()

    test_decisions = [
        ("req_report_generate", "report_generate", "approve", "Level1 auto dry_run approved"),
        ("req_mouse_click", "mouse_click", "hold", "Level3 requires human review"),
        ("req_delete_file", "delete_file", "reject", "Level4 dangerous action rejected"),
    ]

    saved = []
    for request_id, action, decision, reason in test_decisions:
        record, path = bridge.create_decision(request_id, action, decision, reason)
        saved.append({"record": record, "path": path})

    summary = bridge.summarize()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-12 Approval UI bridge / manual decision input",
        "saved_decision_count": len(saved),
        "saved_decisions": saved,
        "summary": summary,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-13 ApprovedOperationExecutor decision integration",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_12_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-12 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("SavedDecisionCount:", report["saved_decision_count"])
    print("DecisionCount:", summary["decision_count"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()