from pathlib import Path
from datetime import datetime
import json

from .mission_router import MissionRouter


def main():

    router = MissionRouter()

    result = router.execute(

        "Original Integration DryRun"

    )

    report = {

        "status": result["status"],

        "mission_routed": result["routed"],

        "app_operator_called": result["app_operator_called"],

        "dry_run": True,

        "external_operation": False,

        "real_gui_operation": False,

        "original_write": False

    }

    report_dir = Path(__file__).parent / "reports"

    report_dir.mkdir(exist_ok=True)

    file = report_dir / f"mission_router_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"

    file.write_text(

        json.dumps(report, indent=4, ensure_ascii=False),

        encoding="utf-8"

    )

    print("=== Mission Router Completion Report ===")

    for k, v in report.items():

        print(f"{k}: {v}")

    print("保存先:", file)


if __name__ == "__main__":

    main()