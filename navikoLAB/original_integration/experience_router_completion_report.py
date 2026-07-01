from pathlib import Path
from datetime import datetime
import json

from .experience_router import ExperienceRouter


def main():

    router = ExperienceRouter()

    result = router.execute("Experience DryRun")

    report = {

        "status": result["status"],

        "mission_routed": result["mission_routed"],

        "connector_routed": result["connector_routed"],

        "knowledge_routed": result["knowledge_routed"],

        "reflection_routed": result["reflection_routed"],

        "experience_routed": result["experience_routed"],

        "experience_saved": result["experience"]["experience_saved"],

        "dry_run": True,

        "external_operation": False,

        "real_gui_operation": False,

        "original_write": False

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    file = report_dir / f"experience_router_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"

    file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Experience Router Completion Report ===")

    for k, v in report.items():
        print(f"{k}: {v}")

    print("保存先:", file)


if __name__ == "__main__":
    main()