from datetime import datetime
from pathlib import Path
import json

from navikoLAB.release.v2_completion_judgement import judge_v2_completion

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "release" / "reports"


def create_release_completion_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    judgement = judge_v2_completion()

    report = {
        "status": "completed" if judgement["status"] == "v2_release_candidate_ready" else "incomplete",
        "stage": "第40工程 Release Candidate v2.0",
        "version": judgement["version"],
        "base_score": judgement["base_score"],
        "completion_score": judgement["completion_score"],
        "diagnostics_status": judgement["diagnostics"]["status"],
        "diagnostics": judgement["diagnostics"],
        "limitations": judgement["limitations"],
        "remaining_count": judgement["remaining_count"],
        "final_judgement": judgement["final_judgement"],
        "project_status": "Original Naviko v2.0 RC Ready",
        "next_stage": "Post-v2.0 External Connector Activation / Real App Operation",
    }

    path = REPORT_DIR / f"release_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    return report, path


if __name__ == "__main__":
    report, path = create_release_completion_report()

    print("=== Release Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["stage"])
    print("Version:", report["version"])
    print("診断:", report["diagnostics_status"])
    print("確認項目:", report["diagnostics"]["check_count"])
    print("通過:", report["diagnostics"]["passed"])
    print("失敗:", report["diagnostics"]["failed"])
    print("基盤スコア:", report["base_score"])
    print("完成度:", report["completion_score"])
    print("残課題数:", report["remaining_count"])
    print("ProjectStatus:", report["project_status"])
    print("保存先:", path)
    print("次工程:", report["next_stage"])