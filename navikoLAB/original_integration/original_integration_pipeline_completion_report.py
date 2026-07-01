from pathlib import Path
from datetime import datetime
import json

from .original_integration_pipeline import OriginalIntegrationPipeline


def main():

    pipeline = OriginalIntegrationPipeline()

    result = pipeline.execute(

        "Original Integration DryRun"

    )

    report = {

        "status": result["status"],

        "pipeline_completed": result["pipeline_completed"],

        "mission_routed": result["mission_routed"],

        "connector_routed": result["connector_routed"],

        "knowledge_routed": result["knowledge_routed"],

        "reflection_routed": result["reflection_routed"],

        "experience_routed": result["experience_routed"],

        "dry_run": True,

        "external_operation": result["external_operation"],

        "real_gui_operation": result["real_gui_operation"],

        "original_write": result["original_write"]

    }

    report_dir = Path(__file__).parent / "reports"

    report_dir.mkdir(exist_ok=True)

    report_file = report_dir / (
        f"original_integration_pipeline_completion_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    report_file.write_text(

        json.dumps(report, indent=4, ensure_ascii=False),

        encoding="utf-8"

    )

    print("=== Original Integration Pipeline Completion Report ===")

    for key, value in report.items():

        print(f"{key}: {value}")

    print("保存先:", report_file)


if __name__ == "__main__":
    main()