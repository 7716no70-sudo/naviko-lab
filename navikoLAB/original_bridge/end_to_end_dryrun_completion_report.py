from pathlib import Path
from datetime import datetime
import json

from .end_to_end_dryrun import EndToEndDryRun


def main():

    runner = EndToEndDryRun()

    result = runner.execute("End-to-End DryRun")

    report = {

        "status": result["status"],

        "end_to_end_completed": result["end_to_end_completed"],

        "pipeline_completed": result["pipeline_completed"],

        "dry_run": result["status"] == "dry_run",

        "external_operation": result["external_operation"],

        "real_gui_operation": result["real_gui_operation"],

        "original_write": result["original_write"]

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"end_to_end_dryrun_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== End-to-End DryRun Completion Report ===")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()