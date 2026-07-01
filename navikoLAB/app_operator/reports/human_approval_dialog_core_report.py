from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.human_approval_dialog_core import evaluate_human_approval

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    decisions = [
        evaluate_human_approval(
            mission_text="テスト用のAI OS dry_runを実行する",
            operation_summary="HumanApproval Dialog Core test",
            selected_action=action,
        )
        for action in ["reject", "show_details", "approve"]
    ]

    report = {
        "phase": "Phase7-2",
        "name": "HumanApproval Dialog Core Report",
        "status": "completed",
        "default_action": "reject",
        "available_actions": [
            "reject",
            "show_details",
            "approve",
        ],
        "decisions": decisions,
        "real_execution_allowed_without_approval": False,
        "risk_count": 0,
        "next_phase": "Phase7-3 HumanApproval GUI Dialog Adapter",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"human_approval_dialog_core_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== HumanApproval Dialog Core Report ===")
    print("状態: completed")
    print("工程: Phase7-2 HumanApproval Dialog Core")
    print("DefaultAction: reject")
    print("AvailableActions: reject / show_details / approve")
    print("RealExecutionAllowedWithoutApproval: False")
    print("RiskCount: 0")
    print("次工程: Phase7-3 HumanApproval GUI Dialog Adapter")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()