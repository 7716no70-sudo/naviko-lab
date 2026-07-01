from pathlib import Path
from datetime import datetime
import json

from .knowledge_router import KnowledgeRouter


def main():

    router = KnowledgeRouter()

    result = router.execute("Knowledge DryRun")

    report = {

        "status": result["status"],

        "mission_routed": result["mission_routed"],

        "connector_routed": result["connector_routed"],

        "knowledge_routed": result["knowledge_routed"],

        "knowledge_saved": result["knowledge"]["knowledge_saved"],

        "dry_run": True,

        "external_operation": False,

        "real_gui_operation": False,

        "original_write": False

    }

    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)

    file = report_dir / f"knowledge_router_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"

    file.write_text(
        json.dumps(report, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print("=== Knowledge Router Completion Report ===")

    for k, v in report.items():
        print(f"{k}: {v}")

    print("保存先:", file)


if __name__ == "__main__":
    main()