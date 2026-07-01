from datetime import datetime
from pathlib import Path
import json

from navikoLAB.approval.approval_diagnostics import run_approval_diagnostics

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "approval" / "reports"


def create_approval_completion_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = run_approval_diagnostics()

    report = {
        "status": "completed" if diagnostics["status"] == "passed" else "incomplete",
        "stage": "第39工程 HumanApprovalWorkflow",
        "diagnostics": diagnostics,
        "original_direct_write": False,
        "auto_apply": False,
        "human_approval_required": True,
        "backup_required": True,
        "syntax_check_required": True,
        "startup_check_required": True,
        "rollback_required": True,
        "next_stage": "第40工程 Release Candidate v2.0",
    }

    path = REPORT_DIR / f"approval_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    return report, path


if __name__ == "__main__":
    report, path = create_approval_completion_report()

    print("=== Approval Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["stage"])
    print("診断:", report["diagnostics"]["status"])
    print("確認項目:", report["diagnostics"]["check_count"])
    print("通過:", report["diagnostics"]["passed"])
    print("失敗:", report["diagnostics"]["failed"])
    print("Original直接書込:", report["original_direct_write"])
    print("自動反映:", report["auto_apply"])
    print("人間承認必須:", report["human_approval_required"])
    print("バックアップ必須:", report["backup_required"])
    print("構文チェック必須:", report["syntax_check_required"])
    print("起動確認必須:", report["startup_check_required"])
    print("ロールバック必須:", report["rollback_required"])
    print("保存先:", path)
    print("次工程:", report["next_stage"])