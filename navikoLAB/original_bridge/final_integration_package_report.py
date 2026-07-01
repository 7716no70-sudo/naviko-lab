from pathlib import Path
from datetime import datetime
import json

from .end_to_end_dryrun import EndToEndDryRun


def main():

    runner = EndToEndDryRun()

    result = runner.execute("Final Integration Package")

    report = {

        "status": "completed",

        "phase": "Phase4-5 Final Integration Package",

        "bridge_ready": True,

        "facade_ready": True,

        "pipeline_ready": result["pipeline_completed"],

        "end_to_end_completed": result["end_to_end_completed"],

        "dry_run": result["status"] == "dry_run",

        "external_operation": result["external_operation"],

        "real_gui_operation": result["real_gui_operation"],

        "original_write": result["original_write"],

        "ready_for_phase5": (
            result["pipeline_completed"]
            and result["end_to_end_completed"]
            and not result["external_operation"]
            and not result["real_gui_operation"]
            and not result["original_write"]
        )

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"final_integration_package_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Final Integration Package Report ===")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()