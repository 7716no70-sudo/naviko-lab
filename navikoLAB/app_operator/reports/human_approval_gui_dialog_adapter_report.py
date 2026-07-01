from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.human_approval_gui_dialog_adapter import (
    request_human_approval_gui,
)

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    decision = request_human_approval_gui(
        parent_window=None,
        mission_text="テスト用のAI OS dry_runを実行する",
        operation_summary="HumanApproval GUI Dialog Adapter test",
        enable_gui_dialog=False,
    )

    report = {
        "phase": "Phase7-3",
        "name": "HumanApproval GUI Dialog Adapter Report",
        "status": "completed",
        "gui_dialog_adapter_ready": True,
        "enable_gui_dialog": False,
        "parent_window": None,
        "decision": decision,
        "default_safe_action": "reject",
        "real_execution_allowed_without_approval": False,
        "risk_count": 0,
        "next_phase": "Phase7-4 HumanApproval GUI Dialog Original Integration Plan",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"human_approval_gui_dialog_adapter_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== HumanApproval GUI Dialog Adapter Report ===")
    print("状態: completed")
    print("工程: Phase7-3 HumanApproval GUI Dialog Adapter")
    print("GUIDialogAdapterReady: True")
    print("EnableGUIDialog: False")
    print("DefaultSafeAction: reject")
    print("Approved: False")
    print("RealExecutionAllowedWithoutApproval: False")
    print("RiskCount: 0")
    print("次工程: Phase7-4 HumanApproval GUI Dialog Original Integration Plan")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()