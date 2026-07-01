from pathlib import Path
from datetime import datetime
import json

from .original_integration_validator import OriginalIntegrationValidator


def main():

    validator = OriginalIntegrationValidator()

    result = validator.validate("Safety Report")

    report = {

        "status": "completed",

        "phase": "Phase3-10 Original Integration Safety Report",

        "pipeline_valid": result["valid"],

        "pipeline_completed": result["checks"]["pipeline_completed"],

        "dry_run": result["checks"]["dry_run"],

        "external_operation_disabled":
            result["checks"]["external_operation_disabled"],

        "real_gui_operation_disabled":
            result["checks"]["real_gui_operation_disabled"],

        "original_write_disabled":
            result["checks"]["original_write_disabled"],

        "ready_for_phase4": result["valid"]

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"original_integration_safety_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Original Integration Safety Report ===")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()