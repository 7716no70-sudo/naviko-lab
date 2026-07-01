from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "navikoLAB" / "connectors" / "configs"


CONNECTOR_ENV_KEYS = {
    "chatgpt": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "grok": "XAI_API_KEY",
}


class OfficialConnectorConfig:
    def __init__(self) -> None:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    def check_api_keys(self) -> dict:
        results = {}

        for name, env_key in CONNECTOR_ENV_KEYS.items():
            value = os.environ.get(env_key)

            results[name] = {
                "env_key": env_key,
                "api_key_found": bool(value),
                "status": "ready" if value else "api_key_missing",
            }

        return results

    def save(self, results: dict) -> Path:
        output = CONFIG_DIR / f"official_connector_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        data = {
            "status": "completed",
            "stage": "第34工程 Connector正式化",
            "connectors": results,
            "external_call_executed": False,
            "generated_at": datetime.now().isoformat(timespec="seconds"),
        }

        output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return output

    def run(self) -> dict:
        results = self.check_api_keys()
        output = self.save(results)

        ready_count = sum(1 for item in results.values() if item["status"] == "ready")

        return {
            "status": "completed",
            "connector_count": len(results),
            "ready_count": ready_count,
            "missing_count": len(results) - ready_count,
            "output": str(output),
        }


def main() -> None:
    result = OfficialConnectorConfig().run()

    print("=== Official Connector Config ===")
    print(f"状態: {result['status']}")
    print(f"Connector数: {result['connector_count']}")
    print(f"Ready数: {result['ready_count']}")
    print(f"APIキー不足数: {result['missing_count']}")
    print(f"保存先: {result['output']}")


if __name__ == "__main__":
    main()