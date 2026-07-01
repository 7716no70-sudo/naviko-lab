# navikoLAB/stable_life/stable_life_full_system_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeFullSystemReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.inputs = {
            "runtime_unified": self.root / "stable_life" / "reports" / "stable_life_runtime_unified_report_latest.json",
            "scheduler_completion": self.root / "stable_life" / "reports" / "stable_life_scheduler_completion_report_latest.json",
            "command_completion": self.root / "stable_life" / "reports" / "command_interface_completion_report_latest.json",
            "user_command_completion": self.root / "stable_life" / "reports" / "user_command_bridge_completion_report_latest.json",
            "external_input_completion": self.root / "stable_life" / "reports" / "external_input_gateway_completion_report_latest.json",
            "interaction_unified": self.root / "stable_life" / "reports" / "stable_life_interaction_layer_unified_report_latest.json",
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

        runtime_ok = data["runtime_unified"].get("StableLifeRuntimeUnified") is True
        scheduler_ok = data["scheduler_completion"].get("StableLifeSchedulerCompleted") is True
        command_ok = data["command_completion"].get("CommandInterfaceCompleted") is True
        user_command_ok = data["user_command_completion"].get("UserCommandBridgeCompleted") is True
        external_input_ok = data["external_input_completion"].get("ExternalInputGatewayCompleted") is True
        interaction_ok = data["interaction_unified"].get("InteractionLayerUnified") is True

        no_external = all([
            data["runtime_unified"].get("NoRealExternalOperation") is True,
            data["scheduler_completion"].get("RealExternalOperation") is False,
            data["command_completion"].get("RealExternalOperation") is False,
            data["user_command_completion"].get("RealExternalOperation") is False,
            data["external_input_completion"].get("RealExternalOperation") is False,
            data["interaction_unified"].get("NoRealExternalOperation") is True,
        ])

        no_delete = all([
            data["runtime_unified"].get("NoRealFileDelete") is True,
            data["scheduler_completion"].get("RealFileDelete") is False,
            data["command_completion"].get("RealFileDelete") is False,
            data["user_command_completion"].get("RealFileDelete") is False,
            data["external_input_completion"].get("RealFileDelete") is False,
            data["interaction_unified"].get("NoRealFileDelete") is True,
        ])

        no_dangerous_patch = all([
            data["runtime_unified"].get("NoDangerousAutoPatch") is True,
            data["scheduler_completion"].get("DangerousAutoPatch") is False,
            data["command_completion"].get("DangerousAutoPatch") is False,
            data["user_command_completion"].get("DangerousAutoPatch") is False,
            data["external_input_completion"].get("DangerousAutoPatch") is False,
            data["interaction_unified"].get("NoDangerousAutoPatch") is True,
        ])

        full_system_completed = all([
            all(found.values()),
            runtime_ok,
            scheduler_ok,
            command_ok,
            user_command_ok,
            external_input_ok,
            interaction_ok,
            no_external,
            no_delete,
            no_dangerous_patch,
        ])

        result = {
            "status": "completed",
            "phase": "Phase144 Stable Life Full System Report",
            "checked_at": self._now(),
            "StableLifeFullSystemCompleted": full_system_completed,
            "InputReportCount": len(self.inputs),
            "MissingInputCount": len([k for k, v in found.items() if not v]),
            "StableLifeRuntimeUnified": runtime_ok,
            "StableLifeSchedulerCompleted": scheduler_ok,
            "CommandInterfaceCompleted": command_ok,
            "UserCommandBridgeCompleted": user_command_ok,
            "ExternalInputGatewayCompleted": external_input_ok,
            "InteractionLayerUnified": interaction_ok,
            "NoRealExternalOperation": no_external,
            "NoRealFileDelete": no_delete,
            "NoDangerousAutoPatch": no_dangerous_patch,
            "SystemStatus": "stable_life_full_system_completed" if full_system_completed else "incomplete",
            "SafeToContinue": full_system_completed,
            "NextPhase": "Phase145 Stable Life Final Diagnostics",
            "MissingInputs": [k for k, v in found.items() if not v],
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"stable_life_full_system_report_{timestamp}.json"
        latest_path = self.output_dir / "stable_life_full_system_report_latest.json"

        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = StableLifeFullSystemReport()
    result = report.generate()

    print("=== Stable Life Full System Report ===")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"- {item}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()