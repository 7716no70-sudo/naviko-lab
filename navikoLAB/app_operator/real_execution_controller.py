from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def evaluate_real_execution_controller(
    mode="dry_run",
    human_approved=False,
    permission_policy_allowed=False,
    app_operator_ready=True,
):
    real_execution_allowed = bool(
        mode == "real_execution"
        and human_approved
        and permission_policy_allowed
        and app_operator_ready
    )

    return {
        "mode": mode,
        "human_approved": bool(human_approved),
        "permission_policy_allowed": bool(permission_policy_allowed),
        "app_operator_ready": bool(app_operator_ready),
        "real_execution_allowed": real_execution_allowed,
        "blocked": not real_execution_allowed,
        "reason": "dry_run_or_approval_or_policy_required" if not real_execution_allowed else "allowed",
    }

def main():
    controller = evaluate_real_execution_controller()

    result = {
        "phase": "Phase6-9",
        "name": "Real Execution Controller",
        "status": "controller_ready",
        "controller": controller,
        "external_operation": False,
        "real_gui_operation": False,
        "original_write": False,
        "risk_count": 0,
        "safe_to_continue": True,
        "next_phase": "Phase6-10 GUI HumanApproval Dialog Preparation",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"real_execution_controller_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Real Execution Controller ===")
    print("状態: controller_ready")
    print("工程: Phase6-9 Real Execution Controller")
    print("Mode: dry_run")
    print("HumanApproved: False")
    print("PermissionPolicyAllowed: False")
    print("AppOperatorReady: True")
    print("RealExecutionAllowed: False")
    print("Blocked: True")
    print("外部操作実行: False")
    print("Real GUI Operation: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToContinue: True")
    print("次工程: Phase6-10 GUI HumanApproval Dialog Preparation")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()