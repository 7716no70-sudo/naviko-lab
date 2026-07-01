from pathlib import Path
from datetime import datetime
import json

from .original_integration_validator import OriginalIntegrationValidator


def main():

    validator = OriginalIntegrationValidator()

    result = validator.validate("Pipeline Validation")

    report = {

        "status": result["status"],

        "valid": result["valid"],

        **result["checks"]

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"original_integration_validator_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Original Integration Validator Completion Report ===")

    for key, value in report.items():
        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()