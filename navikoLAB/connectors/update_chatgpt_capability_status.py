from pathlib import Path
from datetime import datetime
import json
import shutil
import os


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

CAPABILITY_REGISTRY = LAB_ROOT / "capabilities" / "capability_registry.json"
BACKUP_DIR = LAB_ROOT / "capabilities" / "backups"


def load_registry():
    if not CAPABILITY_REGISTRY.exists():
        raise FileNotFoundError(f"not found: {CAPABILITY_REGISTRY}")

    return json.loads(CAPABILITY_REGISTRY.read_text(encoding="utf-8"))


def save_registry(data):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"capability_registry_before_chatgpt_status_{now}.json"

    shutil.copy2(CAPABILITY_REGISTRY, backup_path)

    CAPABILITY_REGISTRY.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return backup_path


def iter_capabilities(data):
    if isinstance(data, dict) and isinstance(data.get("capabilities"), list):
        return data["capabilities"]

    if isinstance(data, dict):
        return [
            value for value in data.values()
            if isinstance(value, dict)
        ]

    if isinstance(data, list):
        return data

    return []


def update_chatgpt_status():
    data = load_registry()
    capabilities = iter_capabilities(data)

    api_key_exists = bool(os.environ.get("OPENAI_API_KEY"))

    target = None

    for cap in capabilities:
        cap_id = str(cap.get("id", cap.get("name", ""))).lower()

        if cap_id == "chatgpt":
            target = cap
            break

    if target is None:
        return {
            "status": "failed",
            "reason": "chatgpt capability が見つかりません。",
            "backup": None,
        }

    before = dict(target)

    target["enabled"] = True
    target["connector"] = "chatgpt"
    target["api_env"] = "OPENAI_API_KEY"
    target["api_status"] = "ready" if api_key_exists else "key_missing"

    # 既存statusは互換性のため残しつつ、正式Connector接続済みであることを表す
    target["status"] = "api_ready" if api_key_exists else "api_key_missing"

    target.setdefault("notes", [])
    if isinstance(target["notes"], list):
        note = "ChatGPTConnector formal connector registered via ConnectorDispatcher."
        if note not in target["notes"]:
            target["notes"].append(note)

    backup_path = save_registry(data)

    return {
        "status": "updated",
        "api_key_exists": api_key_exists,
        "before": before,
        "after": target,
        "backup": str(backup_path),
    }


def main():
    result = update_chatgpt_status()

    print("=== ChatGPT Capability 状態整理 ===")
    print(f"状態: {result.get('status')}")

    if result.get("reason"):
        print(f"理由: {result.get('reason')}")

    if result.get("api_key_exists") is not None:
        print(f"OPENAI_API_KEY: {'あり' if result['api_key_exists'] else 'なし'}")

    print(f"バックアップ: {result.get('backup')}")

    after = result.get("after")
    if after:
        print("---------------")
        print(f"id: {after.get('id')}")
        print(f"enabled: {after.get('enabled')}")
        print(f"status: {after.get('status')}")
        print(f"connector: {after.get('connector')}")
        print(f"api_env: {after.get('api_env')}")
        print(f"api_status: {after.get('api_status')}")


if __name__ == "__main__":
    main()