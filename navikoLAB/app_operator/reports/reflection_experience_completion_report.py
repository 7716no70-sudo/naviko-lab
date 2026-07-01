from pathlib import Path
from datetime import datetime
import json

from navikoLAB.app_operator.reflection_experience_manager import (
    run_reflection_experience_manager_diagnostics,
)

ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "navikoLAB" / "app_operator" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    report = run_reflection_experience_manager_diagnostics()
    report["report_phase"] = "Phase10-5 Reflection Experience Completion Report"
    report["phase10_completed"] = True
    report["next_phase"] = "Phase11 Planner Feedback / Experience-Based Planning"

    out = REPORT_DIR / f"reflection_experience_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Reflection Experience Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["report_phase"])
    print("ReflectionSaved:", report["reflection_saved"])
    print("ExperienceSaved:", report["experience_saved"])
    print("IndexUpdated:", report["index_updated"])
    print("ReflectionCount:", report["reflection_count"])
    print("ExperienceCount:", report["experience_count"])
    print("SuccessCount:", report["success_count"])
    print("FailureCount:", report["failure_count"])
    print("Phase10Completed:", report["phase10_completed"])
    print("WorkspaceOnly:", report["workspace_only"])
    print("OriginalWrite:", report["original_write"])
    print("FileDelete:", report["file_delete"])
    print("RiskCount:", report["risk_count"])
    print("SafeToContinue:", report["safe_to_continue"])
    print("次工程:", report["next_phase"])
    print("保存先:", out)

if __name__ == "__main__":
    main()