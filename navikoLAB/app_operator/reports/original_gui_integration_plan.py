from pathlib import Path
from datetime import datetime
import json

REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    plan = {
        "phase": "Phase6-15",
        "name": "Original GUI Integration Plan",
        "status": "planned",
        "target": {
            "file": "naviko.py",
            "primary_locator": "launch_original_ai_os()",
            "secondary_locator": "execute_groq_communication()",
            "button_route": "AIミッションボタン -> launch_original_ai_os()",
            "mission_input_route": "目的: -> launch_original_ai_os()",
        },
        "integration_policy": {
            "direct_original_write": False,
            "minimal_diff_required": True,
            "backup_required": True,
            "py_compile_required": True,
            "human_approval_required": True,
            "default_action": "reject",
        },
        "connection_order": [
            "import original_gui_human_approval_connector",
            "call request_original_gui_human_approval() before real execution",
            "keep dry_run=True by default",
            "block real_gui_operation unless explicitly approved",
            "save approval result to report",
        ],
        "current_permissions": {
            "dry_run": True,
            "real_execution_allowed": False,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
        },
        "risk_count": 0,
        "safe_to_prepare_patch": True,
        "next_phase": "Phase6-16 Original GUI Integration Patch Plan",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"original_gui_integration_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original GUI Integration Plan ===")
    print("状態: planned")
    print("工程: Phase6-15 Original GUI Integration Plan")
    print("TargetFile: naviko.py")
    print("PrimaryLocator: launch_original_ai_os()")
    print("SecondaryLocator: execute_groq_communication()")
    print("DirectOriginalWrite: False")
    print("MinimalDiffRequired: True")
    print("HumanApprovalRequired: True")
    print("DefaultAction: reject")
    print("RealExecutionAllowed: False")
    print("Original書込: False")
    print("RiskCount: 0")
    print("SafeToPreparePatch: True")
    print("次工程: Phase6-16 Original GUI Integration Patch Plan")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()