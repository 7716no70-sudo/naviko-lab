from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.diagnostics.app_operator_integrated_diagnostics import AppOperatorIntegratedDiagnostics

def main():
    diagnostics = AppOperatorIntegratedDiagnostics()
    diagnostic_result = diagnostics.run()

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-15 AppOperator Diagnostics Integration",
        "diagnostic_status": diagnostic_result["status"],
        "dir_all_ok": diagnostic_result["dir_all_ok"],
        "policy_check_count": diagnostic_result["policy_check_count"],
        "pipeline_check_count": diagnostic_result["pipeline_check_count"],
        "diagnostic_result": diagnostic_result,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-16 AppOperator Reflection / Experience save",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_15_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-15 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("DirAllOK:", report["dir_all_ok"])
    print("PolicyCheckCount:", report["policy_check_count"])
    print("PipelineCheckCount:", report["pipeline_check_count"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()