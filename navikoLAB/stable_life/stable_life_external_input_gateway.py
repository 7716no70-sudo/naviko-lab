# navikoLAB/stable_life/stable_life_external_input_gateway.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_user_command_bridge import (
    StableLifeRuntimeUserCommandBridge,
)


class StableLifeExternalInputGateway:
    BLOCKED_WORDS = {
        "delete_all",
        "format",
        "shutdown",
        "external_send",
        "auto_patch",
        "overwrite_original",
    }

    COMMAND_ALIASES = {
        "状態": "status",
        "status": "status",
        "確認": "status",
        "cycle": "cycle",
        "実行": "cycle",
        "identity": "identity",
        "自己": "identity",
        "scheduler": "scheduler",
        "予定": "scheduler",
    }

    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.output_dir = self.root / "stable_life" / "external_input_gateway"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.output_dir / "stable_life_external_input_gateway_report.json"
        self.history_path = self.output_dir / "stable_life_external_input_gateway_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def normalize_input(self, raw_input: str) -> dict[str, Any]:
        text = raw_input.strip()
        lowered = text.lower()

        blocked_hits = [
            word for word in self.BLOCKED_WORDS
            if word in lowered
        ]

        if blocked_hits:
            return {
                "accepted": False,
                "reason": "blocked_word_detected",
                "blocked_hits": blocked_hits,
                "command": "",
                "text": text,
            }

        command = "status"
        for key, value in self.COMMAND_ALIASES.items():
            if key.lower() in lowered or key in text:
                command = value
                break

        return {
            "accepted": True,
            "reason": "normalized",
            "blocked_hits": [],
            "command": command,
            "text": text,
        }

    def receive(self, raw_input: str) -> dict[str, Any]:
        normalized = self.normalize_input(raw_input)

        if normalized["accepted"]:
            bridge = StableLifeRuntimeUserCommandBridge(self.root)
            bridge_result = bridge.execute_user_command(
                user_command=normalized["command"],
                text=normalized["text"],
            )

            forwarded = bridge_result.get("BridgeReady") is True
            payload = bridge_result.get("Payload", {})
        else:
            forwarded = False
            payload = {
                "command_result": "input_rejected",
                "reason": normalized["reason"],
                "blocked_hits": normalized["blocked_hits"],
            }

        gateway_completed = (
            normalized["accepted"] is True
            and forwarded is True
        ) or (
            normalized["accepted"] is False
            and forwarded is False
        )

        result = {
            "status": "completed",
            "phase": "Phase140 Stable Life External Input Gateway",
            "created_at": self._now(),
            "RawInput": raw_input,
            "Normalized": normalized,
            "ForwardedToUserCommandBridge": forwarded,
            "Payload": payload,
            "GatewayCompleted": gateway_completed,
            "RealExternalCommunication": False,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": gateway_completed,
            "NextPhase": "Phase141 External Input Gateway Diagnostics",
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
    gateway = StableLifeExternalInputGateway()

    result = gateway.receive("状態を確認して")

    print("=== Stable Life External Input Gateway ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"RawInput: {result['RawInput']}")
    print(f"Accepted: {result['Normalized']['accepted']}")
    print(f"Command: {result['Normalized']['command']}")
    print(f"ForwardedToUserCommandBridge: {result['ForwardedToUserCommandBridge']}")
    print(f"GatewayCompleted: {result['GatewayCompleted']}")
    print("--- Payload ---")
    print(json.dumps(result["Payload"], ensure_ascii=False, indent=2))
    print(f"RealExternalCommunication: {result['RealExternalCommunication']}")
    print(f"RealExternalOperation: {result['RealExternalOperation']}")
    print(f"RealFileDelete: {result['RealFileDelete']}")
    print(f"DangerousAutoPatch: {result['DangerousAutoPatch']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()