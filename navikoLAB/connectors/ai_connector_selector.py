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

DEFAULT_PRIORITY = [
    "chatgpt",
    "claude",
    "gemini",
    "grok",
]


def select_ai_connector(task_type: str = "general", preferred: str | None = None) -> dict:
    key_status = get_api_key_status()

    candidates = []
    for provider in DEFAULT_PRIORITY:
        info = key_status.get(provider, {})
        candidates.append({
            "provider": provider,
            "configured": bool(info.get("configured")),
            "env_name": info.get("env_name"),
            "masked": info.get("masked", ""),
        })

    selected = None

    if preferred:
        preferred_info = key_status.get(preferred)
        if preferred_info and preferred_info.get("configured"):
            selected = preferred

    if not selected:
        for candidate in candidates:
            if candidate["configured"]:
                selected = candidate["provider"]
                break

    result = {
        "status": "selected" if selected else "safe_skipped",
        "task_type": task_type,
        "preferred": preferred,
        "selected": selected,
        "reason": "configured connector selected" if selected else "no configured AI connector",
        "priority": DEFAULT_PRIORITY,
        "candidates": candidates,
        "external_access": False,
        "selected_at": datetime.now().isoformat(timespec="seconds"),
    }

    return result


def create_selector_report(task_type: str = "general", preferred: str | None = None) -> dict:
    result = select_ai_connector(task_type=task_type, preferred=preferred)

    report_path = REPORT_DIR / f"ai_connector_selector_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result["report_path"] = str(report_path)
    return result


def main() -> None:
    result = create_selector_report(task_type="general")

    print("=== AI Connector Selector ===")
    print(f"状態: {result['status']}")
    print(f"用途: {result['task_type']}")
    print(f"選択: {result['selected']}")
    print(f"理由: {result['reason']}")
    print(f"外部通信実行: {result['external_access']}")

    print("候補:")
    for item in result["candidates"]:
        print(f"- {item['provider']}: configured={item['configured']} / env={item['env_name']}")

    print(f"保存先: {result['report_path']}")


if __name__ == "__main__":
    main()