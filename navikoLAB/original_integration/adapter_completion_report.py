from pathlib import Path
import json
from datetime import datetime

from .adapter_request import AdapterRequest
from .original_integration_adapter import OriginalIntegrationAdapter


def main():

    adapter = OriginalIntegrationAdapter()

    req = AdapterRequest(

        mission="Adapter DryRun"

    )

    result = adapter.execute(req)

    report = {

        "status": result.status,

        "routed": result.routed,

        "dry_run": result.dry_run,

        "app_operator_called": result.app_operator_called,

        "external_operation": False,

        "real_gui_operation": False,

        "original_write": False

    }

    report_dir = Path(__file__).parent / "reports"

    report_dir.mkdir(exist_ok=True)

    file = report_dir / f"adapter_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"

    file.write_text(

        json.dumps(report, indent=4, ensure_ascii=False),

        encoding="utf-8"

    )

    print("=== Original Integration Adapter Completion Report ===")

    for k, v in report.items():

        print(f"{k}: {v}")

    print("保存先:", file)


if __name__ == "__main__":

    main()