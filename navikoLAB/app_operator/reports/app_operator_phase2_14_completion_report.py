from pathlib import Path
import json
from datetime import datetime

from navikoLAB.app_operator.approval.app_operator_dry_run_pipeline import AppOperatorDryRunPipeline

def main():
    pipeline = AppOperatorDryRunPipeline()

    operations = [
        {"request_id": "phase2_14_report", "action": "report_generate"},
        {"request_id": "phase2_14_browser", "action": "browser_search"},
        {"request_id": "phase2_14_mouse", "action": "mouse_click"},
        {"request_id": "phase2_14_keyboard", "action": "keyboard_input"},
        {"request_id": "phase2_14_delete", "action": "delete_file"},
    ]

    results = [pipeline.run(op) for op in operations]

    report = {
        "status": "completed",
        "phase": "Post-v2.0 Phase2-14 AppOperator End-to-End dry_run pipeline",
        "pipeline": "AppOperatorDryRunPipeline",
        "operation_count": len(results),
        "results": results,
        "dry_run": True,
        "external_operation": False,
        "real_gui_operation": False,
        "next_phase": "Phase2-15 AppOperator Diagnostics Integration",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    out_dir = Path(__file__).resolve().parent
    out_path = out_dir / f"app_operator_phase2_14_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== AppOperator Phase2-14 Completion Report ===")
    print("状態:", report["status"])
    print("工程:", report["phase"])
    print("Pipeline:", report["pipeline"])
    print("OperationCount:", report["operation_count"])
    print("dry_run:", report["dry_run"])
    print("Real GUI Operation:", report["real_gui_operation"])
    print("外部操作実行:", report["external_operation"])
    print("保存先:", out_path)
    print("次工程:", report["next_phase"])

if __name__ == "__main__":
    main()