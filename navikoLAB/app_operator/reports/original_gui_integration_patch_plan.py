from pathlib import Path
from datetime import datetime
import json

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    plan = {
        "phase": "Phase6-16",
        "name": "Original GUI Integration Patch Plan",
        "status": "planned",
        "target_file": "naviko.py",
        "patch_policy": {
            "full_replace": False,
            "minimal_diff": True,
            "backup_required": True,
            "py_compile_required": True,
            "dry_run_first": True,
            "human_approval_required": True,
            "default_action": "reject",
        },
        "locator": {
            "primary": "def launch_original_ai_os(",
            "secondary": "def execute_groq_communication(",
            "insert_goal": "call HumanApproval connector before any real execution path",
        },
        "planned_change": [
            "add safe import with fallback",
            "call request_original_gui_human_approval() inside launch_original_ai_os() only for real execution preparation",
            "keep dry_run behavior unchanged",
            "block real_gui_operation by default",
            "do not write Original automatically",
        ],
        "safety": {
            "real_execution_allowed": False,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
            "risk_count": 0,
        },
        "safe_to_generate_patch": True,
        "next_phase": "Phase6-17 Original GUI Integration Minimal Patch",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"original_gui_integration_patch_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original GUI Integration Patch Plan ===")
    print("状態: planned")
    print("工程: Phase6-16 Original GUI Integration Patch Plan")
    print("TargetFile: naviko.py")
    print("PrimaryLocator: def launch_original_ai_os(")
    print("SecondaryLocator: def execute_groq_communication(")
    print("FullReplace: False")
    print("MinimalDiff: True")
    print("BackupRequired: True")
    print("PyCompileRequired: True")
    print("HumanApprovalRequired: True")
    print("DefaultAction: reject")
    print("RealExecutionAllowed: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToGeneratePatch: True")
    print("次工程: Phase6-17 Original GUI Integration Minimal Patch")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()