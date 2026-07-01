from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.original_adoption.human_approved_adoption_dry_run import HumanApprovedAdoptionDryRun

def main():
    runner = HumanApprovedAdoptionDryRun()
    result, result_path = runner.run()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-21 Human-approved Original adoption dry_run",
        "gate_status": result["gate_status"],
        "adoption_dry_run_allowed": result["adoption_dry_run_allowed"],
        "original_write_executed": result["original_write_executed"],
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "result_path": result_path,
        "next_phase": "Phase2-22 AppOperator Original Adoption Package Summary",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_21_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-21 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("GateStatus:", report["gate_status"])
    print("AdoptionDryRunAllowed:", report["adoption_dry_run_allowed"])
    print("OriginalWriteExecuted:", report["original_write_executed"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("Result保存先:", result_path)
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()