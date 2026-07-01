# navikoLAB/stable_life/stable_life_interaction_layer_unified_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeInteractionLayerUnifiedReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.inputs = {
            "command_interface": self.root / "stable_life" / "reports" / "command_interface_completion_report_latest.json",
            "user_command_bridge": self.root / "stable_life" / "reports" / "user_command_bridge_completion_report_latest.json",
            "external_input_gateway": self.root / "stable_life" / "reports" / "external_input_gateway_completion_report_latest.json",
        }

        self.output_dir = self.root / "stable_life" / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> tuple[bool, dict[str, Any]]:
        if not path.exists():
            return False, {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return isinstance(data, dict), data if isinstance(data, dict) else {}
        except Exception:
            return False, {}

    def generate(self) -> dict[str, Any]:
        found = {}
        data = {}

        for name, path in self.inputs.items():
            ok, value = self._read_json(path)
            found[name] = ok
            data[name] = value

        command_ok = data["command_interface"].get("CommandInterfaceCompleted") is True
        user_bridge_ok = data["user_command_bridge"].get("UserCommandBridgeCompleted") is True
        gateway_ok = data["external_input_gateway"].get("ExternalInputGatewayCompleted") is True

        blocked_ok = (
            data["user_command_bridge"].get("UnsupportedCommandRejected") is True
            and data["external_input_gateway"].get("BlockedInputRejected") is True
        )

        no_external = all([
            data["command_interface"].get("RealExternalOperation") is False,
            data["user_command_bridge"].get("RealExternalOperation") is False,
            data["external_input_gateway"].get("RealExternalOperation") is False,
        ])

        no_delete = all([
            data["command_interface"].get("RealFileDelete") is False,
            data["user_command_bridge"].get("RealFileDelete") is False,
            data["external_input_gateway"].get("RealFileDelete") is False,
        ])

        no_dangerous_patch = all([
            data["command_interface"].get("DangerousAutoPatch") is False,
            data["user_command_bridge"].get("DangerousAutoPatch") is False,
            data["external_input_gateway"].get("DangerousAutoPatch") is False,
        ])

        interaction_layer_unified = all([
            all(found.values()),
            command_ok,
            user_bridge_ok,
            gateway_ok,
            blocked_ok,
            no_external,
            no_delete,
            no_dangerous_patch,
        ])

        result = {
            "status": "completed",
            "phase": "Phase143 Stable Life Interaction Layer Unified Report",
            "checked_at": self._now(),
            "InteractionLayerUnified": interaction_layer_unified,
            "InputReportCount": len(self.inputs),
            "MissingInputCount": len([k for k, v in found.items() if not v]),
            "CommandInterfaceCompleted": command_ok,
            "UserCommandBridgeCompleted": user_bridge_ok,
            "ExternalInputGatewayCompleted": gateway_ok,
            "UnsupportedCommandRejected": blocked_ok,
            "NoRealExternalOperation": no_external,
            "NoRealFileDelete": no_delete,
            "NoDangerousAutoPatch": no_dangerous_patch,
            "UnifiedStatus": "stable_life_interaction_layer_unified" if interaction_layer_unified else "incomplete",
            "SafeToContinue": interaction_layer_unified,
            "NextPhase": "Phase144 Stable Life Full System Report",
            "MissingInputs": [k for k, v in found.items() if not v],
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"stable_life_interaction_layer_unified_report_{timestamp}.json"
        latest_path = self.output_dir / "stable_life_interaction_layer_unified_report_latest.json"

        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = StableLifeInteractionLayerUnifiedReport()
    result = report.generate()

    print("=== Stable Life Interaction Layer Unified Report ===")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"- {item}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()