from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

try:
    from .api_key_manager import get_api_key_status
except ImportError:
    from api_key_manager import get_api_key_status


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_unified_ai_connector_diagnostics() -> dict:
    key_status = get_api_key_status()

    connectors = {}
    ready_count = 0

    for provider, info in key_status.items():
        ready = bool(info.get("configured"))
        if ready:
            ready_count += 1

        connectors[provider] = {
            "provider": provider,
            "env_name": info.get("env_name"),
            "api_key_configured": ready,
            "api_key_masked": info.get("masked", ""),
            "runtime_mode": "real_api_ready" if ready else "safe_skipped",
            "external_access_tested": False,
        }

    result = {
        "status": "completed",
        "phase": "Post-v2.0 Phase1-5 Unified AI Connector Diagnostics",
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "connector_count": len(connectors),
        "ready_count": ready_count,
        "missing_count": len(connectors) - ready_count,
        "external_access": False,
        "connectors": connectors,
    }

    report_path = REPORT_DIR / f"ai_connector_unified_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result["report_path"] = str(report_path)
    return result


def main() -> None:
    result = run_unified_ai_connector_diagnostics()

    print("=== Unified AI Connector Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"Connector数: {result['connector_count']}")
    print(f"Ready数: {result['ready_count']}")
    print(f"未設定数: {result['missing_count']}")
    print(f"外部通信実行: {result['external_access']}")

    for name, info in result["connectors"].items():
        print(f"- {name}")
        print(f"  env: {info['env_name']}")
        print(f"  api_key: {info['api_key_configured']}")
        print(f"  mode: {info['runtime_mode']}")

    print(f"保存先: {result['report_path']}")


if __name__ == "__main__":
    main()