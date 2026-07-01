from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def evaluate_permission_policy(step_name, human_approved=False):
    allowed_steps = {
        "read_only_check": True,
        "dry_run_app_operation": True,
        "real_gui_operation": False,
        "external_operation": False,
        "original_write": False,
    }

    base_allowed = allowed_steps.get(step_name, False)
    final_allowed = bool(base_allowed and human_approved)

    return {
        "step_name": step_name,
        "base_allowed_by_policy": base_allowed,
        "human_approved": bool(human_approved),
        "final_allowed": final_allowed,
        "blocked": not final_allowed,
        "reason": "human_approval_required_or_policy_blocked" if not final_allowed else "allowed",
    }

def main():
    checks = [
        evaluate_permission_policy("read_only_check", human_approved=False),
        evaluate_permission_policy("dry_run_app_operation", human_approved=False),
        evaluate_permission_policy("real_gui_operation", human_approved=False),
        evaluate_permission_policy("external_operation", human_approved=False),
        evaluate_permission_policy("original_write", human_approved=False),
    ]

    result = {
        "phase": "Phase6-3",
        "name": "PermissionPolicy Step Execution Gate",
        "status": "blocked",
        "checks": checks,
        "real_execution_allowed": False,
        "safe_steps_defined": True,
        "human_approval_required": True,
        "policy_gate_active": True,
        "next_phase": "Phase6-4 AppOperator Real Execution Gate",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"permission_policy_step_execution_gate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== PermissionPolicy Step Execution Gate ===")
    print("状態: blocked")
    print("工程: Phase6-3 PermissionPolicy Step Execution Gate")
    print("SafeStepsDefined: True")
    print("PolicyGateActive: True")
    print("HumanApproval必須: True")
    print("RealExecutionAllowed: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("次工程: Phase6-4 AppOperator Real Execution Gate")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()