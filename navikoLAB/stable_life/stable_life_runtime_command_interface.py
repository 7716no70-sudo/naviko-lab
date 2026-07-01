# navikoLAB/stable_life/stable_life_runtime_command_interface.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_adapter import StableLifeRuntimeAdapter
from navikoLAB.stable_life.stable_life_runtime_unified_report import StableLifeRuntimeUnifiedReport


class StableLifeRuntimeCommandInterface:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.identity_bridge_path = (
            self.root / "stable_life" / "identity_runtime_bridge"
            / "life_identity_runtime_bridge_report.json"
        )
        self.scheduler_completion_path = (
            self.root / "stable_life" / "reports"
            / "stable_life_scheduler_completion_report_latest.json"
        )

        self.output_dir = self.root / "stable_life" / "command_interface"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.output_dir / "stable_life_runtime_command_interface_report.json"
        self.history_path = self.output_dir / "stable_life_runtime_command_interface_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def execute(self, command: str, text: str = "") -> dict[str, Any]:
        command = command.strip().lower()

        if command == "cycle":
            result = StableLifeRuntimeAdapter(self.root).run_from_runtime(
                {
                    "event_type": "command_cycle",
                    "text": text or "Command Interface から Stable Life Runtime cycle を実行した",
                    "source": "stable_life_command_interface",
                }
            )
            payload = {
                "command_result": "cycle_executed",
                "runtime_integrated": result.get("stable_life_runtime_integrated") is True,
                "safe": result.get("safe_to_continue") is True,
                "integrity_score": result.get("integrity_score"),
            }

        elif command == "status":
            result = StableLifeRuntimeUnifiedReport(self.root).generate()
            payload = {
                "command_result": "status_report_generated",
                "stable_life_runtime_unified": result.get("StableLifeRuntimeUnified") is True,
                "unified_status": result.get("UnifiedStatus"),
                "safe": result.get("SafeToContinue") is True,
            }

        elif command == "identity":
            bridge = self._read_json(self.identity_bridge_path)
            context = bridge.get("RuntimeReadableContext", {})
            payload = {
                "command_result": "identity_context_read",
                "bridge_context_ready": bridge.get("BridgeContextReady") is True,
                "runtime_read_only": bridge.get("RuntimeReadOnly") is True,
                "identity_statement": context.get("identity_statement", ""),
                "safe": bridge.get("SafeToContinue") is True,
            }

        elif command == "scheduler":
            scheduler = self._read_json(self.scheduler_completion_path)
            payload = {
                "command_result": "scheduler_status_read",
                "scheduler_completed": scheduler.get("StableLifeSchedulerCompleted") is True,
                "scheduler_mode": scheduler.get("SchedulerMode"),
                "real_background_daemon": scheduler.get("RealBackgroundDaemon"),
                "safe": scheduler.get("SafeToContinue") is True,
            }

        else:
            payload = {
                "command_result": "unknown_command",
                "supported_commands": ["cycle", "status", "identity", "scheduler"],
                "safe": False,
            }

        success = payload.get("safe") is True and payload.get("command_result") != "unknown_command"

        report = {
            "status": "completed",
            "phase": "Phase134 Stable Life Runtime Command Interface",
            "created_at": self._now(),
            "Command": command,
            "Payload": payload,
            "CommandSuccess": success,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": success,
            "NextPhase": "Phase135 Command Interface Diagnostics",
        }

        self.report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self._append_history(report)

        report["SavedPath"] = str(self.report_path)
        return report

    def _append_history(self, report: dict[str, Any]) -> None:
        if self.history_path.exists():
            history = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            history = {"count": 0, "items": []}

        history["items"].append(report)
        history["count"] = len(history["items"])

        self.history_path.write_text(
            json.dumps(history, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    interface = StableLifeRuntimeCommandInterface()

    result = interface.execute(
        command="status",
        text="Phase134 Command Interface status test",
    )

    print("=== Stable Life Runtime Command Interface ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"Command: {result['Command']}")
    print(f"CommandSuccess: {result['CommandSuccess']}")
    print("--- Payload ---")
    print(json.dumps(result["Payload"], ensure_ascii=False, indent=2))
    print(f"RealExternalOperation: {result['RealExternalOperation']}")
    print(f"RealFileDelete: {result['RealFileDelete']}")
    print(f"DangerousAutoPatch: {result['DangerousAutoPatch']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()