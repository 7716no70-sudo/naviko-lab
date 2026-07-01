# navikoLAB/stable_life/command_interface_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class CommandInterfaceDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.command_report_path = (
            self.root
            / "stable_life"
            / "command_interface"
            / "stable_life_runtime_command_interface_report.json"
        )

        self.output_dir = self.root / "stable_life" / "command_interface"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = (
            self.output_dir
            / "command_interface_diagnostics_report.json"
        )

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json(self, path: Path) -> tuple[bool, dict[str, Any]]:
        if not path.exists():
            return False, {}

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return True, data
            return False, {}
        except Exception:
            return False, {}

    def run(self) -> dict[str, Any]:
        found, report = self._read_json(self.command_report_path)

        payload = report.get("Payload", {})

        diagnostics_passed = all([
            found,
            report.get("CommandSuccess") is True,
            report.get("SafeToContinue") is True,
            report.get("RealExternalOperation") is False,
            report.get("RealFileDelete") is False,
            report.get("DangerousAutoPatch") is False,
            payload.get("safe") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase135 Command Interface Diagnostics",
            "checked_at": self._now(),
            "CommandReportFound": found,
            "CommandSuccess": report.get("CommandSuccess") is True,
            "PayloadSafe": payload.get("safe") is True,
            "NoRealExternalOperation": report.get("RealExternalOperation") is False,
            "NoRealFileDelete": report.get("RealFileDelete") is False,
            "NoDangerousAutoPatch": report.get("DangerousAutoPatch") is False,
            "DiagnosticsPassed": diagnostics_passed,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase136 Command Interface Completion Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = CommandInterfaceDiagnostics()
    result = diagnostics.run()

    print("=== Command Interface Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()