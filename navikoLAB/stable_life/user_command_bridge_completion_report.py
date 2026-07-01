# navikoLAB/stable_life/user_command_bridge_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class UserCommandBridgeCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.bridge_report_path = (
            self.root / "stable_life" / "user_command_bridge"
            / "stable_life_runtime_user_command_bridge_report.json"
        )
        self.diagnostics_report_path = (
            self.root / "stable_life" / "user_command_bridge"
            / "user_command_bridge_diagnostics_report.json"
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
        bridge_found, bridge = self._read_json(self.bridge_report_path)
        diagnostics_found, diagnostics = self._read_json(self.diagnostics_report_path)

        user_command_bridge_completed = all([
            bridge_found,
            diagnostics_found,
            diagnostics.get("DiagnosticsPassed") is True,
            diagnostics.get("AcceptedCommandOK") is True,
            diagnostics.get("RejectedCommandOK") is True,
            diagnostics.get("UnsupportedCommandRejected") is True,
            diagnostics.get("NoRealExternalOperation") is True,
            diagnostics.get("NoRealFileDelete") is True,
            diagnostics.get("NoDangerousAutoPatch") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase139 User Command Bridge Completion Report",
            "checked_at": self._now(),
            "UserCommandBridgeCompleted": user_command_bridge_completed,
            "BridgeReportFound": bridge_found,
            "DiagnosticsReportFound": diagnostics_found,
            "AcceptedCommandOK": diagnostics.get("AcceptedCommandOK") is True,
            "RejectedCommandOK": diagnostics.get("RejectedCommandOK") is True,
            "UnsupportedCommandRejected": diagnostics.get("UnsupportedCommandRejected") is True,
            "SupportedCommands": bridge.get("SupportedCommands", ["cycle", "status", "identity", "scheduler"]),
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": user_command_bridge_completed,
            "NextPhase": "Phase140 Stable Life External Input Gateway",
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"user_command_bridge_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "user_command_bridge_completion_report_latest.json"

        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        latest_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

        result["SavedPath"] = str(output_path)
        result["LatestPath"] = str(latest_path)
        return result


def main() -> None:
    report = UserCommandBridgeCompletionReport()
    result = report.generate()

    print("=== User Command Bridge Completion Report ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()