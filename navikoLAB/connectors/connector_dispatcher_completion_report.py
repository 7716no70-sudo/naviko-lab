from pathlib import Path
from datetime import datetime
import json


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

CAPABILITY_REGISTRY = LAB_ROOT / "capabilities" / "capability_registry.json"
REPORT_DIR = LAB_ROOT / "reports"


def load_capabilities():
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


def build_connector_summary():
    capabilities = load_capabilities()

    connector_names = [
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

    found = []
    missing = []

    for name in connector_names:
        matched = None
        for cap in capabilities:
            cap_id = str(cap.get("id", cap.get("name", ""))).lower()
            if cap_id == name:
                matched = cap
                break

        if matched:
            found.append(matched)
        else:
            missing.append(name)

    enabled = [
        cap for cap in found
        if cap.get("enabled") is True
    ]

    disabled = [
        cap for cap in found
        if cap.get("enabled") is not True
    ]

    mock = [
        cap for cap in found
        if str(cap.get("status", "")).lower() == "mock"
        or str(cap.get("provider", "")).lower() == "mock"
    ]

    api = [
        cap for cap in found
        if str(cap.get("status", "")).lower() == "api"
        or str(cap.get("provider", "")).lower() == "api"
    ]

    return {
        "connector_total_expected": len(connector_names),
        "connector_found": len(found),
        "connector_missing": len(missing),
        "enabled_count": len(enabled),
        "disabled_count": len(disabled),
        "mock_count": len(mock),
        "api_count": len(api),
        "found": found,
        "missing": missing,
    }


def create_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    summary = build_connector_summary()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = REPORT_DIR / f"connector_dispatcher_completion_{now}.txt"

    lines = []
    lines.append("=== ConnectorDispatcher 完成レポート ===")
    lines.append(f"作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("【状態】")
    lines.append("第24工程-1 ConnectorDispatcher完成レポート作成")
    lines.append("")
    lines.append("【Connector概要】")
    lines.append(f"想定Connector数: {summary['connector_total_expected']}")
    lines.append(f"登録確認済Connector数: {summary['connector_found']}")
    lines.append(f"不足Connector数: {summary['connector_missing']}")
    lines.append(f"有効Connector数: {summary['enabled_count']}")
    lines.append(f"無効Connector数: {summary['disabled_count']}")
    lines.append(f"mock Connector数: {summary['mock_count']}")
    lines.append(f"api Connector数: {summary['api_count']}")
    lines.append("")
    lines.append("【登録済Connector】")

    for cap in summary["found"]:
        cap_id = cap.get("id", cap.get("name", "unknown"))
        enabled = cap.get("enabled", False)
        status = cap.get("status", cap.get("provider", "unknown"))
        lines.append(f"- {cap_id} / enabled={enabled} / status={status}")

    lines.append("")
    lines.append("【不足Connector】")

    if summary["missing"]:
        for name in summary["missing"]:
            lines.append(f"- {name}")
    else:
        lines.append("- なし")

    lines.append("")
    lines.append("【接続構造】")
    lines.append("Mission Dashboard")
    lines.append("↓")
    lines.append("Original Bridge")
    lines.append("↓")
    lines.append("AutonomousCapabilityFlow")
    lines.append("↓")
    lines.append("MissionCapabilityBridge")
    lines.append("↓")
    lines.append("CapabilityRouter")
    lines.append("↓")
    lines.append("AgentManager")
    lines.append("↓")
    lines.append("ConnectorDispatcher")
    lines.append("↓")
    lines.append("AgentExecutor")
    lines.append("↓")
    lines.append("MultiAIOrchestrator")
    lines.append("↓")
    lines.append("Reflection")
    lines.append("↓")
    lines.append("Improvement")
    lines.append("")
    lines.append("【完成判定】")

    if summary["connector_missing"] == 0:
        lines.append("ConnectorDispatcher工程: completed")
        lines.append("完成率: 100%")
    else:
        lines.append("ConnectorDispatcher工程: partial")
        lines.append("完成率: 要確認")

    lines.append("")
    lines.append("【次工程】")
    lines.append("第24工程-2 Connector診断ツール作成")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    return report_path, summary


def main():
    report_path, summary = create_report()

    print("=== ConnectorDispatcher 完成レポート作成 ===")
    print(f"保存先: {report_path}")
    print(f"想定Connector数: {summary['connector_total_expected']}")
    print(f"登録確認済Connector数: {summary['connector_found']}")
    print(f"不足Connector数: {summary['connector_missing']}")
    print(f"有効Connector数: {summary['enabled_count']}")
    print(f"無効Connector数: {summary['disabled_count']}")
    print(f"mock Connector数: {summary['mock_count']}")
    print(f"api Connector数: {summary['api_count']}")

    if summary["missing"]:
        print("不足Connector:")
        for name in summary["missing"]:
            print(f"- {name}")
    else:
        print("不足Connector: なし")


if __name__ == "__main__":
    main()