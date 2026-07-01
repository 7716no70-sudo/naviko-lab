from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.integration.integration_diagnostics import IntegrationDiagnostics


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "integration" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = IntegrationDiagnostics().run()

    result = {
        "status": "completed" if diagnostics["status"] == "passed" else "warning",
        "stage": "第32工程 Original Naviko統合",
        "diagnostics": diagnostics,
        "completed_items": [
            "OriginalIntegrationManager",
            "MissionPipeline",
            "IntegrationDiagnostics",
            "IntegrationCompletionReport",
        ],
        "connection_flow": [
            "MissionManager",
            "TaskPlanner",
            "CapabilityRouter",
            "ConnectorDispatcher",
            "SearchDispatcher",
            "DeepSearchEngine",
            "KnowledgeBase",
            "ExperienceManager",
            "KnowledgeReflection",
            "AutoImprovementSuggestion",
            "AutoRefactoringPlan",
            "OriginalNaviko",
        ],
        "next_stage": "第33工程 自己改善自動ループ / Mission自動生成 / Knowledge学習 / Experience学習 / 安全チェック / Original反映",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"integration_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Integration Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"IntegrationMap数: {diagnostics['integration_map_count']}")
    print(f"Pipeline数: {diagnostics['pipeline_count']}")
    print(f"不足候補: {len(diagnostics['missing'])}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()