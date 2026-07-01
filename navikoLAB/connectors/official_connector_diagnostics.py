from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "navikoLAB" / "connectors" / "configs"


class OfficialConnectorDiagnostics:
    def load_latest_config(self) -> dict:
        files = sorted(CONFIG_DIR.glob("official_connector_config_*.json")) if CONFIG_DIR.exists() else []

        if not files:
            return {
                "status": "missing",
                "connectors": {},
            }

        latest = files[-1]

        try:
            data = json.loads(latest.read_text(encoding="utf-8"))
            data["_source"] = str(latest)
            return data
        except Exception as e:
            return {
                "status": "read_failed",
                "error": str(e),
                "connectors": {},
                "_source": str(latest),
            }

    def run(self) -> dict:
        config = self.load_latest_config()
        connectors = config.get("connectors", {})

        ready = [
            name
            for name, info in connectors.items()
            if info.get("status") == "ready"
        ]

        missing = [
            name
            for name, info in connectors.items()
            if info.get("status") != "ready"
        ]

        return {
            "status": "passed" if connectors else "warning",
            "connector_count": len(connectors),
            "ready_count": len(ready),
            "missing_count": len(missing),
            "ready": ready,
            "missing": missing,
            "external_call_executed": False,
            "source": config.get("_source"),
        }


def main() -> None:
    result = OfficialConnectorDiagnostics().run()

    print("=== Official Connector Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"Connector数: {result['connector_count']}")
    print(f"Ready数: {result['ready_count']}")
    print(f"APIキー不足数: {result['missing_count']}")
    print(f"外部通信実行: {result['external_call_executed']}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()