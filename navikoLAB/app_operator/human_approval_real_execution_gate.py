from pathlib import Path
from datetime import datetime
import json

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def evaluate_human_approval(approved=False):
    return {
        "human_approved": bool(approved),
        "real_execution_allowed": bool(approved),
        "blocked": not bool(approved),
        "reason": "human_approval_required" if not approved else "human_approved",
    }

def main():
    approval = evaluate_human_approval(approved=False)

    result = {
        "phase": "Phase6-2",
        "name": "HumanApproval Real Execution Gate",
        "status": "blocked",
        "approval": approval,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "app_operator_real_execution": False,
        "original_write": False,
        "next_phase": "Phase6-3 PermissionPolicy Step Execution Gate",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"human_approval_real_execution_gate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== HumanApproval Real Execution Gate ===")
    print("状態: blocked")
    print("工程: Phase6-2 HumanApproval Real Execution Gate")
    print("HumanApproved: False")
    print("RealExecutionAllowed: False")
    print("Blocked: True")
    print("Reason: human_approval_required")
    print("AppOperator実実行: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("次工程: Phase6-3 PermissionPolicy Step Execution Gate")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()