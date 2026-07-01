from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY_FILE = ROOT / "navikoLAB" / "capabilities" / "capability_registry.json"
BACKUP_DIR = ROOT / "navikoLAB" / "original_adoption" / "capability_registry_backups"


def enable_app_operator() -> dict:
    result = {
        "status": "not_started",
        "registry_file": str(REGISTRY_FILE),
        "backup_file": None,
        "app_operator_found": False,
        "changed": False,
    }

    if not REGISTRY_FILE.exists():
        result["status"] = "failed"
        result["error"] = "capability_registry.json が見つかりません。"
        return result

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"capability_registry_before_app_operator_{now}.json"
    backup_file.write_text(
        REGISTRY_FILE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    result["backup_file"] = str(backup_file)

    capabilities = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))

    for capability in capabilities:
        if capability.get("id") == "app_operator":
            result["app_operator_found"] = True

            if capability.get("enabled") is not True or capability.get("status") != "mock":
                capability["enabled"] = True
                capability["status"] = "mock"
                result["changed"] = True

            break

    if not result["app_operator_found"]:
        capabilities.append(
            {
                "id": "app_operator",
                "name": "App Operator",
                "type": "app",
                "enabled": True,
                "status": "mock",
                "strengths": [
                    "app_operation",
                    "file_operation",
                    "workflow",
                ],
            }
        )
        result["app_operator_found"] = True
        result["changed"] = True

    REGISTRY_FILE.write_text(
        json.dumps(capabilities, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )

    result["status"] = "enabled"
    return result


def main() -> None:
    result = enable_app_operator()

    print("=== app_operator Capability 有効化 ===")
    print(f"状態: {result['status']}")
    print(f"登録ファイル: {result['registry_file']}")
    print(f"バックアップ: {result['backup_file']}")
    print(f"app_operatorあり: {result['app_operator_found']}")
    print(f"変更あり: {result['changed']}")

    if "error" in result:
        print(f"ERROR: {result['error']}")


if __name__ == "__main__":
    main()