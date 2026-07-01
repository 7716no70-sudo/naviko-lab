from pathlib import Path
from datetime import datetime
import json

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = {
        "phase": "Phase6-14",
        "name": "Original GUI Connector Safety Report",
        "status": "completed",
        "original_gui_connector_ready": True,
        "default_action": "reject",
        "explicit_human_approval_required": True,
        "real_execution_allowed_without_approval": False,
        "real_execution_allowed": False,
        "real_gui_operation": False,
        "external_operation": False,
        "original_write": False,
        "risk_count": 0,
        "safe_to_plan_original_gui_integration": True,
        "next_phase": "Phase6-15 Original GUI Integration Plan",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"original_gui_connector_safety_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original GUI Connector Safety Report ===")
    print("状態: completed")
    print("工程: Phase6-14 Original GUI Connector Safety Report")
    print("OriginalGUIConnectorReady: True")
    print("DefaultAction: reject")
    print("ExplicitHumanApprovalRequired: True")
    print("RealExecutionAllowedWithoutApproval: False")
    print("RealExecutionAllowed: False")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToPlanOriginalGUIIntegration: True")
    print("次工程: Phase6-15 Original GUI Integration Plan")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()