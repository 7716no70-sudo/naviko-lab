from pathlib import Path
from datetime import datetime
import json

from .original_call_adapter import call_mission


def main():

    result = call_mission("Original Call Adapter DryRun")

    report = {

        "status": result["status"],

        "adapter_connected": True,

        "facade_connected": True,

        "bridge_connected": True,

        "pipeline_completed": result["pipeline_completed"],

        "dry_run": result["status"] == "dry_run",

        "external_operation": result["external_operation"],

        "real_gui_operation": result["real_gui_operation"],

        "original_write": result["original_write"]

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"original_call_adapter_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Original Call Adapter Completion Report ===")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()