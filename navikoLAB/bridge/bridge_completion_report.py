from datetime import datetime
from pathlib import Path
import json

from navikoLAB.bridge.bridge_diagnostics import run_bridge_diagnostics

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "bridge" / "reports"


def create_bridge_completion_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = run_bridge_diagnostics()

    report = {
        "status": "completed" if diagnostics["status"] == "passed" else "incomplete",
        "stage": "第38工程 OriginalNaviko Bridge",
        "diagnostics": diagnostics,
        "original_direct_write": False,
        "auto_apply": False,
        "human_approval_required": True,
        "next_stage": "第39工程 HumanApprovalWorkflow",
    }

    path = REPORT_DIR / f"bridge_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return report, path


if __name__ == "__main__":
    report, path = create_bridge_completion_report()

    print("=== Bridge Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["stage"])
    print("診断:", report["diagnostics"]["status"])
    print("確認項目:", report["diagnostics"]["check_count"])
    print("通過:", report["diagnostics"]["passed"])
    print("失敗:", report["diagnostics"]["failed"])
    print("Original直接書込:", report["original_direct_write"])
    print("自動反映:", report["auto_apply"])
    print("人間承認必須:", report["human_approval_required"])
    print("保存先:", path)
    print("次工程:", report["next_stage"])