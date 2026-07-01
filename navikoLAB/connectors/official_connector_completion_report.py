from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.connectors.official_connector_diagnostics import OfficialConnectorDiagnostics


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "connectors" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = OfficialConnectorDiagnostics().run()

    result = {
        "status": "completed",
        "stage": "第34工程 Connector正式化",
        "diagnostics": diagnostics,
        "completed_items": [
            "OfficialConnectorConfig",
            "OfficialConnectorDiagnostics",
            "OfficialConnectorCompletionReport",
        ],
        "safety": {
            "external_call_executed": False,
            "api_key_value_saved": False,
            "human_setup_required": diagnostics["missing_count"] > 0,
        },
        "next_stage": "第35工程 長期Knowledge / KnowledgeGraph / ExperienceGraph / ProjectKnowledge / ArchitectureMemory",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"official_connector_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Official Connector Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"Connector数: {diagnostics['connector_count']}")
    print(f"Ready数: {diagnostics['ready_count']}")
    print(f"APIキー不足数: {diagnostics['missing_count']}")
    print(f"外部通信実行: {diagnostics['external_call_executed']}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()