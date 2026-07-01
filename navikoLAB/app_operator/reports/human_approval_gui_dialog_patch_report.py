from pathlib import Path
from datetime import datetime
import json

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = {
        "phase": "Phase7-6",
        "name": "HumanApproval GUI Dialog Patch Report",
        "status": "completed",
        "target_file": "naviko.py",
        "target_function": "launch_original_ai_os(parent_window, mission=None)",
        "completed_changes": [
            "HumanApproval connector replaced with GUI dialog adapter",
            "approval_result key fixed from human_approved to approved",
            "GUI mission input confirmed",
        ],
        "observed_result": {
            "input": "目的: テスト用のAI OS dry_runを実行する",
            "status": "blocked",
            "pipeline_completed": None,
        },
        "safety": {
            "human_approval_gui_dialog_connected": True,
            "permission_policy_still_blocks": True,
            "real_execution_allowed": False,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
        },
        "risk_count": 0,
        "safe_to_continue": True,
        "next_phase": "Phase7-7 PermissionPolicy Core Integration Plan",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"human_approval_gui_dialog_patch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== HumanApproval GUI Dialog Patch Report ===")
    print("状態: completed")
    print("工程: Phase7-6 HumanApproval GUI Dialog Patch Report")
    print("TargetFile: naviko.py")
    print("TargetFunction: launch_original_ai_os(parent_window, mission=None)")
    print("GUIDialogConnected: True")
    print("KeyFix: human_approved -> approved")
    print("ObservedStatus: blocked")
    print("PermissionPolicyStillBlocks: True")
    print("RealExecutionAllowed: False")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToContinue: True")
    print("次工程: Phase7-7 PermissionPolicy Core Integration Plan")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()