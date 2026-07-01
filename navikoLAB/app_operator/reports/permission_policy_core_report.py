from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.permission_policy_core import evaluate_permission

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    actions = [
        "read_only_check",
        "dry_run_app_operation",
        "real_gui_operation",
        "external_operation",
        "original_write",
    ]

    report = {
        "phase": "Phase7-1",
        "name": "PermissionPolicy Core Report",
        "status": "completed",
        "human_approved": False,
        "decisions": [
            evaluate_permission(action, human_approved=False)
            for action in actions
        ],
        "real_execution_allowed": False,
        "risk_count": 0,
        "next_phase": "Phase7-2 HumanApproval Dialog Core",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"permission_policy_core_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== PermissionPolicy Core Report ===")
    print("状態: completed")
    print("工程: Phase7-1 PermissionPolicy Core")
    print("HumanApproved: False")
    print("RealExecutionAllowed: False")
    print("RiskCount: 0")
    print("次工程: Phase7-2 HumanApproval Dialog Core")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()