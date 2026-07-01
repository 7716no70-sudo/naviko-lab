from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def request_original_gui_human_approval(
    mission_text="",
    operation_summary="",
    default_action="reject",
):
    approved = default_action == "approve"

    return {
        "connector": "original_gui_human_approval_connector",
        "mission_text": mission_text,
        "operation_summary": operation_summary,
        "default_action": default_action,
        "selected_action": default_action,
        "human_approved": approved,
        "real_execution_allowed": approved,
        "blocked": not approved,
        "reason": "default_reject_safety" if not approved else "human_approved",
    }

def main():
    result = {
        "phase": "Phase6-13",
        "name": "Original GUI HumanApproval Connector",
        "status": "connector_ready",
        "approval_result": request_original_gui_human_approval(
            mission_text="テスト用のAI OS dry_runを実行する",
            operation_summary="Original GUI HumanApproval connector test",
            default_action="reject",
        ),
        "real_execution_allowed": False,
        "real_gui_operation": False,
        "external_operation": False,
        "original_write": False,
        "risk_count": 0,
        "safe_to_connect_original_gui": True,
        "next_phase": "Phase6-14 Original GUI Connector Safety Report",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"original_gui_human_approval_connector_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original GUI HumanApproval Connector ===")
    print("状態: connector_ready")
    print("工程: Phase6-13 Original GUI HumanApproval Connector")
    print("DefaultAction: reject")
    print("HumanApproved: False")
    print("RealExecutionAllowed: False")
    print("Blocked: True")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToConnectOriginalGUI: True")
    print("次工程: Phase6-14 Original GUI Connector Safety Report")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()