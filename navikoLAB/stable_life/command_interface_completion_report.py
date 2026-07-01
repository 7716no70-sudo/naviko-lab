# navikoLAB/stable_life/command_interface_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class CommandInterfaceCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.command_report_path = (
            self.root / "stable_life" / "command_interface"
            / "stable_life_runtime_command_interface_report.json"
        )
        self.diagnostics_report_path = (
            self.root / "stable_life" / "command_interface"
            / "command_interface_diagnostics_report.json"
        )

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
        command_found, command = self._read_json(self.command_report_path)
        diagnostics_found, diagnostics = self._read_json(self.diagnostics_report_path)

        command_interface_completed = all([
            command_found,
            diagnostics_found,
            command.get("CommandSuccess") is True,
            command.get("SafeToContinue") is True,
            diagnostics.get("DiagnosticsPassed") is True,
            diagnostics.get("SafeToContinue") is True,
            diagnostics.get("NoRealExternalOperation") is True,
            diagnostics.get("NoRealFileDelete") is True,
            diagnostics.get("NoDangerousAutoPatch") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase136 Command Interface Completion Report",
            "checked_at": self._now(),
            "CommandInterfaceCompleted": command_interface_completed,
            "CommandReportFound": command_found,
            "DiagnosticsReportFound": diagnostics_found,
            "CommandSuccess": command.get("CommandSuccess") is True,
            "DiagnosticsPassed": diagnostics.get("DiagnosticsPassed") is True,
            "SupportedCommands": ["cycle", "status", "identity", "scheduler"],
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": command_interface_completed,
            "NextPhase": "Phase137 Stable Life Runtime User Command Bridge",
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"command_interface_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "command_interface_completion_report_latest.json"

        output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        latest_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = CommandInterfaceCompletionReport()
    result = report.generate()

    print("=== Command Interface Completion Report ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()