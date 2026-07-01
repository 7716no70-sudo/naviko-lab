from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.policy.permission_policy import PermissionPolicy

def main():
    policy = PermissionPolicy()

    test_actions = [
        "report_generate",
        "window_inspect",
        "browser_search",
        "open_application",
        "mouse_click",
        "keyboard_input",
        "ocr_read",
        "delete_file",
        "shutdown",
        "payment",
    ]

    results = [policy.classify(action) for action in test_actions]

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-9 Permission Policy",
        "policy": "PermissionPolicy",
        "levels": PermissionPolicy.LEVELS,
        "test_count": len(results),
        "results": results,
        "dry_run": True,
        "external_operation": False,
        "next_phase": "Phase2-10 PermissionPolicy integration with AppOperator",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_9_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-9 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Policy:", report["policy"])
    print("TestCount:", report["test_count"])
    print("dry_run:", report["dry_run"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()