from pathlib import Path
from datetime import datetime

from navikoLAB.capabilities.capability_connector import CapabilityConnector
from navikoLAB.capabilities.capability_router import CapabilityRouter


class CapabilityGUIBridge:
    """
    GUI表示用にCapability情報を整形する橋渡し。
    naviko.pyを肥大化させないため、表示ロジックをここに分離する。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        self.connector = CapabilityConnector(
            self.root_dir
        )

        self.router = CapabilityRouter(
            self.root_dir
        )

    def get_capability_summary(self):
        capabilities = self.connector.capabilities

        enabled = []
        disabled = []
        type_count = {}

        for item in capabilities:
            capability_type = item.get("type", "unknown")

            type_count[capability_type] = (
                type_count.get(capability_type, 0) + 1
            )

            if item.get("enabled"):
                enabled.append(item)
            else:
                disabled.append(item)

        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "total": len(capabilities),
            "enabled_count": len(enabled),
            "disabled_count": len(disabled),
            "type_count": type_count,
            "enabled": enabled,
            "disabled": disabled
        }

    def format_capability_summary(self):
        summary = self.get_capability_summary()

        lines = []
        lines.append("=== Capability GUI 診断 ===")
        lines.append(f"能力総数: {summary.get('total')}")
        lines.append(f"有効: {summary.get('enabled_count')}")
        lines.append(f"無効: {summary.get('disabled_count')}")
        lines.append(f"Type別: {summary.get('type_count')}")
        lines.append("")
        lines.append("=== 有効能力 ===")

        for item in summary.get("enabled", []):
            lines.append(
                f"- {item.get('id')} / {item.get('name')} / {item.get('type')} / {item.get('mode')}"
            )

        lines.append("")
        lines.append("=== 無効能力 ===")

        for item in summary.get("disabled", []):
            lines.append(
                f"- {item.get('id')} / {item.get('name')} / {item.get('type')} / {item.get('mode')}"
            )

        return "\n".join(lines)

    def diagnose_route(self, purpose):
        route_result = self.router.route(
            purpose
        )

        selected = [
            item.get("id", "unknown")
            for item in route_result.get("selected", [])
        ]

        lines = []
        lines.append("=== Capability Router GUI 診断 ===")
        lines.append(f"目的: {purpose}")
        lines.append(f"必要: {route_result.get('required_ids', [])}")
        lines.append(f"選択: {selected}")
        lines.append(f"不足: {route_result.get('missing', [])}")

        return "\n".join(lines)