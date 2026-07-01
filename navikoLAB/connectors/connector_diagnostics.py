from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

CAPABILITY_REGISTRY = LAB_ROOT / "capabilities" / "capability_registry.json"


EXPECTED_CONNECTORS = [
    "chatgpt",
    "app_operator",
    "image_ai",
    "video_ai",
    "browser",
    "voice_ai",
    "claude",
    "gemini",
    "grok",
]


def load_registry():
    if not CAPABILITY_REGISTRY.exists():
        return []

    try:
        data = json.loads(CAPABILITY_REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return []

    if isinstance(data, dict):
        if isinstance(data.get("capabilities"), list):
            return data["capabilities"]
        return list(data.values())

    if isinstance(data, list):
        return data

    return []


def find_connector(capabilities, connector_id):
    for cap in capabilities:
        cap_id = str(cap.get("id", cap.get("name", ""))).lower()
        if cap_id == connector_id:
            return cap
    return None


def diagnose_connectors():
    capabilities = load_registry()

    results = []
    enabled_count = 0
    disabled_count = 0
    mock_count = 0
    api_count = 0
    missing_count = 0

    for connector_id in EXPECTED_CONNECTORS:
        cap = find_connector(capabilities, connector_id)

        if not cap:
            missing_count += 1
            results.append({
                "id": connector_id,
                "exists": False,
                "enabled": False,
                "status": "missing",
                "type": "missing",
            })
            continue

        enabled = cap.get("enabled") is True
        status = str(cap.get("status", cap.get("provider", "unknown"))).lower()
        cap_type = str(cap.get("type", "unknown")).lower()

        if enabled:
            enabled_count += 1
        else:
            disabled_count += 1

        if status == "mock":
            mock_count += 1

        if status == "api":
            api_count += 1

        results.append({
            "id": connector_id,
            "exists": True,
            "enabled": enabled,
            "status": status,
            "type": cap_type,
        })

    return {
        "total_expected": len(EXPECTED_CONNECTORS),
        "registered_count": len(EXPECTED_CONNECTORS) - missing_count,
        "missing_count": missing_count,
        "enabled_count": enabled_count,
        "disabled_count": disabled_count,
        "mock_count": mock_count,
        "api_count": api_count,
        "connectors": results,
    }


def print_diagnostics():
    result = diagnose_connectors()

    print("=== Connector 診断 ===")
    print(f"想定Connector数: {result['total_expected']}")
    print(f"登録済Connector数: {result['registered_count']}")
    print(f"不足Connector数: {result['missing_count']}")
    print(f"有効Connector数: {result['enabled_count']}")
    print(f"無効Connector数: {result['disabled_count']}")
    print(f"mock Connector数: {result['mock_count']}")
    print(f"api Connector数: {result['api_count']}")
    print("---------------")

    for connector in result["connectors"]:
        print(
            f"- {connector['id']} / "
            f"exists={connector['exists']} / "
            f"enabled={connector['enabled']} / "
            f"status={connector['status']} / "
            f"type={connector['type']}"
        )

    print("---------------")

    if result["missing_count"] == 0:
        print("診断結果: passed")
    else:
        print("診断結果: warning")


def main():
    print_diagnostics()


if __name__ == "__main__":
    main()