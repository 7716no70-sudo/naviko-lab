from pathlib import Path
from datetime import datetime
import json

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    plan = {
        "phase": "Phase6-20",
        "name": "PermissionPolicy Integration Patch Plan",
        "status": "planned",
        "target_file": "naviko.py",
        "target_function": "launch_original_ai_os(parent_window, mission=None)",
        "insert_after": "HumanApproval connector approved check",
        "integration_goal": "HumanApproval通過後にPermissionPolicyを確認し、許可されない場合はblockedで停止する",
        "patch_policy": {
            "full_replace": False,
            "minimal_diff": True,
            "backup_required": True,
            "py_compile_required": True,
            "dry_run_default": True,
            "real_gui_operation_default": False,
            "external_operation_default": False,
            "original_write_default": False,
        },
        "planned_route": [
            "mission input",
            "launch_original_ai_os",
            "HumanApproval connector",
            "PermissionPolicy check",
            "blocked unless policy allowed",
            "call_mission only when safe",
        ],
        "safety": {
            "real_execution_allowed": False,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
            "risk_count": 0,
        },
        "safe_to_generate_patch": True,
        "next_phase": "Phase6-21 PermissionPolicy Minimal Patch",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"permission_policy_integration_patch_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== PermissionPolicy Integration Patch Plan ===")
    print("状態: planned")
    print("工程: Phase6-20 PermissionPolicy Integration Patch Plan")
    print("TargetFile: naviko.py")
    print("TargetFunction: launch_original_ai_os(parent_window, mission=None)")
    print("InsertAfter: HumanApproval connector approved check")
    print("FullReplace: False")
    print("MinimalDiff: True")
    print("BackupRequired: True")
    print("PyCompileRequired: True")
    print("DryRunDefault: True")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToGeneratePatch: True")
    print("次工程: Phase6-21 PermissionPolicy Minimal Patch")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()