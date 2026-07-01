from __future__ import annotations

import os
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "configs"
REPORT_DIR = BASE_DIR / "reports"

CONFIG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

API_KEY_ENV_NAMES = {
    "chatgpt": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "grok": "XAI_API_KEY",
}


def mask_api_key(value: str | None) -> str:
    if not value:
        return ""
    if len(value) <= 8:
        return "****"
    return value[:4] + "****" + value[-4:]


def get_api_key(provider: str) -> str | None:
    env_name = API_KEY_ENV_NAMES.get(provider)
    if not env_name:
        return None
    return os.environ.get(env_name)


def get_api_key_status() -> dict:
    results = {}

    for provider, env_name in API_KEY_ENV_NAMES.items():
        key = os.environ.get(env_name)
        results[provider] = {
            "env_name": env_name,
            "configured": bool(key),
            "masked": mask_api_key(key),
        }

    return results


def run_api_key_diagnostics() -> dict:
    status = get_api_key_status()
    configured_count = sum(1 for item in status.values() if item["configured"])
    missing_count = len(status) - configured_count

    result = {
        "status": "completed",
        "phase": "Post-v2.0 Phase1-2 API Key Manager",
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "provider_count": len(status),
        "configured_count": configured_count,
        "missing_count": missing_count,
        "external_access": False,
        "keys": status,
    }

    report_path = REPORT_DIR / f"api_key_manager_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result["report_path"] = str(report_path)
    return result


def main() -> None:
    result = run_api_key_diagnostics()

    print("=== API Key Manager Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"Provider数: {result['provider_count']}")
    print(f"設定済み: {result['configured_count']}")
    print(f"未設定: {result['missing_count']}")
    print(f"外部通信実行: {result['external_access']}")

    for provider, info in result["keys"].items():
        state = "configured" if info["configured"] else "missing"
        print(f"- {provider}: {state} / {info['env_name']} / {info['masked']}")

    print(f"保存先: {result['report_path']}")


if __name__ == "__main__":
    main()