from pathlib import Path
from datetime import datetime
import json
import shutil
import os


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

CAPABILITY_REGISTRY = LAB_ROOT / "capabilities" / "capability_registry.json"
BACKUP_DIR = LAB_ROOT / "capabilities" / "backups"


FORMAL_AI_CONNECTORS = {
    "claude": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "grok": "XAI_API_KEY",
}


def load_registry():
    if not CAPABILITY_REGISTRY.exists():
        raise FileNotFoundError(f"not found: {CAPABILITY_REGISTRY}")

    return json.loads(CAPABILITY_REGISTRY.read_text(encoding="utf-8"))


def save_registry(data):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"capability_registry_before_formal_ai_status_{now}.json"

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


def update_capability(cap, connector_id, api_env):
    api_key_exists = bool(os.environ.get(api_env))

    before = dict(cap)

    cap["connector"] = connector_id
    cap["api_env"] = api_env
    cap["api_status"] = "ready" if api_key_exists else "key_missing"
    cap["status"] = "api_ready" if api_key_exists else "api_key_missing"

    # APIキーが未設定でも、正式Connector登録済みとして有効化はまだしない。
    # ユーザーがGUIから有効化できるよう、enabledは既存値を維持する。
    cap.setdefault("notes", [])
    if isinstance(cap["notes"], list):
        note = f"{connector_id} formal connector registered via ConnectorDispatcher."
        if note not in cap["notes"]:
            cap["notes"].append(note)

    return before, dict(cap), api_key_exists


def update_formal_ai_status():
    data = load_registry()
    capabilities = iter_capabilities(data)

    updated = []
    missing = []

    for connector_id, api_env in FORMAL_AI_CONNECTORS.items():
        target = None

        for cap in capabilities:
            cap_id = str(cap.get("id", cap.get("name", ""))).lower()
            if cap_id == connector_id:
                target = cap
                break

        if target is None:
            missing.append(connector_id)
            continue

        before, after, api_key_exists = update_capability(
            target,
            connector_id,
            api_env
        )

        updated.append({
            "id": connector_id,
            "api_env": api_env,
            "api_key_exists": api_key_exists,
            "before": before,
            "after": after,
        })

    backup_path = save_registry(data)

    return {
        "status": "updated",
        "updated_count": len(updated),
        "missing_count": len(missing),
        "updated": updated,
        "missing": missing,
        "backup": str(backup_path),
    }


def main():
    result = update_formal_ai_status()

    print("=== Formal AI Capability 状態整理 ===")
    print(f"状態: {result.get('status')}")
    print(f"更新数: {result.get('updated_count')}")
    print(f"不足数: {result.get('missing_count')}")
    print(f"バックアップ: {result.get('backup')}")
    print("---------------")

    for item in result.get("updated", []):
        after = item["after"]

        print(f"id: {item['id']}")
        print(f"enabled: {after.get('enabled')}")
        print(f"status: {after.get('status')}")
        print(f"connector: {after.get('connector')}")
        print(f"api_env: {after.get('api_env')}")
        print(f"api_status: {after.get('api_status')}")
        print("---------------")

    if result.get("missing"):
        print("不足:")
        for connector_id in result["missing"]:
            print(f"- {connector_id}")


if __name__ == "__main__":
    main()