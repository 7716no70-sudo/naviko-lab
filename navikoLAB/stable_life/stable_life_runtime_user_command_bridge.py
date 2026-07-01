# navikoLAB/stable_life/stable_life_runtime_user_command_bridge.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_command_interface import (
    StableLifeRuntimeCommandInterface,
)


class StableLifeRuntimeUserCommandBridge:
    SUPPORTED_COMMANDS = {
        "cycle",
        "status",
        "identity",
        "scheduler",
    }

    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.output_dir = self.root / "stable_life" / "user_command_bridge"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = (
            self.output_dir / "stable_life_runtime_user_command_bridge_report.json"
        )
        self.history_path = (
            self.output_dir / "stable_life_runtime_user_command_bridge_history.json"
        )

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def execute_user_command(
        self,
        user_command: str,
        text: str = "",
    ) -> dict[str, Any]:

        command = user_command.strip().lower()

        accepted = command in self.SUPPORTED_COMMANDS

        if accepted:
            interface = StableLifeRuntimeCommandInterface(self.root)
            interface_result = interface.execute(command=command, text=text)

            payload = interface_result.get("Payload", {})
            command_success = interface_result.get("CommandSuccess") is True

        else:
            payload = {
                "command_result": "unsupported_command",
                "supported_commands": sorted(self.SUPPORTED_COMMANDS),
            }
            command_success = False

        bridge_ready = accepted and command_success

        result = {
            "status": "completed",
            "phase": "Phase137 Stable Life Runtime User Command Bridge",
            "created_at": self._now(),
            "UserCommand": command,
            "CommandAccepted": accepted,
            "CommandSuccess": command_success,
            "BridgeReady": bridge_ready,
            "Payload": payload,
            "SupportedCommands": sorted(self.SUPPORTED_COMMANDS),
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": bridge_ready,
            "NextPhase": "Phase138 User Command Bridge Diagnostics",
        }

        self.report_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        self._append_history(result)

        result["SavedPath"] = str(self.report_path)
        return result

    def _append_history(self, result: dict[str, Any]) -> None:
        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(result)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    bridge = StableLifeRuntimeUserCommandBridge()

    result = bridge.execute_user_command(
        user_command="status",
        text="Phase137 bridge test",
    )

    print("=== Stable Life Runtime User Command Bridge ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"UserCommand: {result['UserCommand']}")
    print(f"CommandAccepted: {result['CommandAccepted']}")
    print(f"CommandSuccess: {result['CommandSuccess']}")
    print(f"BridgeReady: {result['BridgeReady']}")
    print("--- Payload ---")
    print(json.dumps(result["Payload"], ensure_ascii=False, indent=2))
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()