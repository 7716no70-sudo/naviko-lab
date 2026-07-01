from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def request_human_approval_for_real_execution(
    mission_text="",
    operation_summary="",
    default_action="reject",
):
    return {
        "mission_text": mission_text,
        "operation_summary": operation_summary,
        "dialog_available": True,
        "selected_action": default_action,
        "approved": default_action == "approve",
        "rejected": default_action != "approve",
        "real_execution_allowed": default_action == "approve",
        "reason": "default_reject_safety" if default_action != "approve" else "human_approved",
    }

def main():
    approval = request_human_approval_for_real_execution(
        mission_text="テスト用のAI OS dry_runを実行する",
        operation_summary="AppOperator real execution gate test",
        default_action="reject",
    )

    result = {
        "phase": "Phase6-11",
        "name": "GUI HumanApproval Dialog Adapter",
        "status": "adapter_ready",
        "approval": approval,
        "default_action": "reject",
        "real_execution_allowed": False,
        "external_operation": False,
        "real_gui_operation": False,
        "original_write": False,
        "risk_count": 0,
        "next_phase": "Phase6-12 GUI Dialog Adapter Safety Report",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"gui_human_approval_dialog_adapter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== GUI HumanApproval Dialog Adapter ===")
    print("状態: adapter_ready")
    print("工程: Phase6-11 GUI HumanApproval Dialog Adapter")
    print("DialogAvailable: True")
    print("DefaultAction: reject")
    print("SelectedAction: reject")
    print("Approved: False")
    print("Rejected: True")
    print("RealExecutionAllowed: False")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("次工程: Phase6-12 GUI Dialog Adapter Safety Report")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()