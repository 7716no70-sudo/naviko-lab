from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    result = {
        "phase": "Phase6-10",
        "name": "GUI HumanApproval Dialog Preparation",
        "status": "prepared",
        "dialog_actions": [
            "approve",
            "reject",
            "show_details",
        ],
        "default_action": "reject",
        "real_execution_allowed": False,
        "requires_explicit_human_approval": True,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "original_write": False,
        "risk_count": 0,
        "next_phase": "Phase6-11 GUI HumanApproval Dialog Adapter",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"gui_human_approval_dialog_preparation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== GUI HumanApproval Dialog Preparation ===")
    print("状態: prepared")
    print("工程: Phase6-10 GUI HumanApproval Dialog Preparation")
    print("DialogActions: approve / reject / show_details")
    print("DefaultAction: reject")
    print("RequiresExplicitHumanApproval: True")
    print("RealExecutionAllowed: False")
    print("dry_run: True")
    print("外部操作実行: False")
    print("Real GUI Operation: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("次工程: Phase6-11 GUI HumanApproval Dialog Adapter")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()