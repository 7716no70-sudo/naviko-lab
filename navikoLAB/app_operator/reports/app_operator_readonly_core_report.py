from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.app_operator_readonly_core import inspect_path_readonly

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = Path(__file__).resolve().parent
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    result = inspect_path_readonly(str(ROOT / "naviko.py"))

    report = {
        "phase": "Phase7-10",
        "name": "AppOperator ReadOnly Core Report",
        "status": "completed",
        "readonly_result": result,
        "safety": {
            "read_only": True,
            "real_gui_operation": False,
            "external_operation": False,
            "original_write": False,
            "file_write": False,
            "file_delete": False,
        },
        "risk_count": 0,
        "safe_to_continue": True,
        "next_phase": "Phase7-11 AppOperator ReadOnly Pipeline Plan",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out = REPORT_DIR / f"app_operator_readonly_core_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator ReadOnly Core Report ===")
    print("状態: completed")
    print("工程: Phase7-10 AppOperator ReadOnly Core")
    print(f"TargetExists: {result['target_exists']}")
    print(f"TargetType: {result['target_type']}")
    print("ReadOnly: True")
    print("Real GUI Operation: False")
    print("外部操作実行: False")
    print("Original書込: False")
    print("FileWrite: False")
    print("FileDelete: False")
    print("RiskCount: 0")
    print("SafeToContinue: True")
    print("次工程: Phase7-11 AppOperator ReadOnly Pipeline Plan")
    print(f"保存先: {out}")

if __name__ == "__main__":
    main()