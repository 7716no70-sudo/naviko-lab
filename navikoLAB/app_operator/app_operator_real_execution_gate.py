from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def evaluate_app_operator_real_execution(
    dry_run_completed=True,
    human_approved=False,
    permission_policy_allowed=False,
):
    allowed = bool(
        dry_run_completed
        and human_approved
        and permission_policy_allowed
    )

    return {
        "dry_run_completed": bool(dry_run_completed),
        "human_approved": bool(human_approved),
        "permission_policy_allowed": bool(permission_policy_allowed),
        "app_operator_real_execution_allowed": allowed,
        "blocked": not allowed,
        "reason": "approval_or_policy_not_satisfied" if not allowed else "allowed",
    }

def main():
    gate = evaluate_app_operator_real_execution()

    result = {
        "phase": "Phase6-4",
        "name": "AppOperator Real Execution Gate",
        "status": "blocked",
        "gate": gate,
        "real_gui_operation": False,
        "external_operation": False,
        "original_write": False,
        "safe_to_continue": True,
        "next_phase": "Phase6-5 Real Execution Safety Summary",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"app_operator_real_execution_gate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Real Execution Gate ===")
    print("状態: blocked")
    print("工程: Phase6-4 AppOperator Real Execution Gate")
    print("DryRunCompleted: True")
    print("HumanApproved: False")
    print("PermissionPolicyAllowed: False")
    print("AppOperatorRealExecutionAllowed: False")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("SafeToContinue: True")
    print("次工程: Phase6-5 Real Execution Safety Summary")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()