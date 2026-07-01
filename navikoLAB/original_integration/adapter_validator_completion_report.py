from pathlib import Path
import json
from datetime import datetime

from .adapter_request import AdapterRequest
from .adapter_validator import AdapterValidator


def main():

    validator = AdapterValidator()

    request = AdapterRequest(
        mission="Validator DryRun"
    )

    result = validator.validate(request)

    report = {

        "status": "completed",

        "valid": result["valid"],

        "error_count": len(result["errors"]),

        "dry_run": True,

        "external_operation": False,

        "real_gui_operation": False,

        "original_write": False

    }

    report_dir = Path(__file__).parent / "reports"

    report_dir.mkdir(exist_ok=True)

    file = report_dir / f"adapter_validator_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"

    file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Adapter Validator Completion Report ===")

    for k, v in report.items():
        print(f"{k}: {v}")

    print("保存先:", file)


if __name__ == "__main__":
    main()