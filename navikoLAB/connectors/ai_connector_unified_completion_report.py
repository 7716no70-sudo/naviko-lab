from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

try:
    from .ai_connector_unified_diagnostics import run_unified_ai_connector_diagnostics
except ImportError:
    from ai_connector_unified_diagnostics import run_unified_ai_connector_diagnostics


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def create_completion_report() -> dict:
    diagnostics = run_unified_ai_connector_diagnostics()

    result = {
        "status": "completed",
        "phase": "Post-v2.0 Phase1-6 Unified AI Connector Completion Report",
        "completed_at": datetime.now().isoformat(timespec="seconds"),
        "connector_count": diagnostics["connector_count"],
        "ready_count": diagnostics["ready_count"],
        "missing_count": diagnostics["missing_count"],
        "external_access": diagnostics["external_access"],
        "completed_items": [
            "API Key Manager created",
            "Unified AI Connector Diagnostics created",
            "ChatGPT Connector connected to API Key Manager",
            "Safe skipped mode confirmed",
            "External access disabled during diagnostics",
            "AI connector auto-selection created",
            "ConnectorDispatcher multi-AI routing created",
        ],

        "remaining_items": [
            "Real API call test after user API key configuration",
        ],

        "next_phase": "Post-v2.0 Phase1-16 Real API call test after API key configuration",
    }
        
    report_path = REPORT_DIR / f"ai_connector_unified_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result["report_path"] = str(report_path)
    return result


def main() -> None:
    result = create_completion_report()

    print("=== Unified AI Connector Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['phase']}")
    print(f"Connector数: {result['connector_count']}")
    print(f"Ready数: {result['ready_count']}")
    print(f"APIキー未設定数: {result['missing_count']}")
    print(f"外部通信実行: {result['external_access']}")
    print("完了項目:")
    for item in result["completed_items"]:
        print(f"- {item}")
    print("残項目:")
    for item in result["remaining_items"]:
        print(f"- {item}")
    print(f"保存先: {result['report_path']}")
    print(f"次工程: {result['next_phase']}")


if __name__ == "__main__":
    main()