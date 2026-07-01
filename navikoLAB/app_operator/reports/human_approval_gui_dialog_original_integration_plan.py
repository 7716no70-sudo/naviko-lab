from pathlib import Path
from datetime import datetime
import json

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    plan = {
        "phase": "Phase7-4",
        "name": "HumanApproval GUI Dialog Original Integration Plan",
        "status": "planned",
        "target_file": "naviko.py",
        "target_function": "launch_original_ai_os(parent_window, mission=None)",
        "replace_target": "original_gui_human_approval_connector",
        "new_adapter": "human_approval_gui_dialog_adapter.request_human_approval_gui",
        "planned_behavior": {
            "parent_window_used": True,
            "enable_gui_dialog": True,
            "default_safe_action": "reject",
            "approve_action": "continue to PermissionPolicy",
            "reject_action": "return blocked",
        },
        "patch_policy": {
            "full_replace": False,
            "minimal_diff": True,
            "backup_required": True,
            "py_compile_required": True,
            "manual_review_required": True,
        },
        "safety": {
            "real_execution_allowed_without_approval": False,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
            "risk_count": 0,
        },
        "safe_to_generate_patch": True,
        "next_phase": "Phase7-5 HumanApproval GUI Dialog Minimal Patch",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"human_approval_gui_dialog_original_integration_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== HumanApproval GUI Dialog Original Integration Plan ===")
    print("状態: planned")
    print("工程: Phase7-4 HumanApproval GUI Dialog Original Integration Plan")
    print("TargetFile: naviko.py")
    print("TargetFunction: launch_original_ai_os(parent_window, mission=None)")
    print("NewAdapter: human_approval_gui_dialog_adapter.request_human_approval_gui")
    print("ParentWindowUsed: True")
    print("EnableGUIDialog: True")
    print("DefaultSafeAction: reject")
    print("FullReplace: False")
    print("MinimalDiff: True")
    print("BackupRequired: True")
    print("PyCompileRequired: True")
    print("RiskCount: 0")
    print("次工程: Phase7-5 HumanApproval GUI Dialog Minimal Patch")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()