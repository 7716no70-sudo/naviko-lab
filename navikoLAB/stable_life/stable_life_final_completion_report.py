# navikoLAB/stable_life/stable_life_final_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeFinalCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.full_system_path = (
            self.root / "stable_life" / "reports"
            / "stable_life_full_system_report_latest.json"
        )

        self.final_diagnostics_path = (
            self.root / "stable_life" / "diagnostics"
            / "stable_life_final_diagnostics_report.json"
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
        full_found, full = self._read_json(self.full_system_path)
        diag_found, diag = self._read_json(self.final_diagnostics_path)

        completed = all([
            full_found,
            diag_found,
            full.get("StableLifeFullSystemCompleted") is True,
            diag.get("FinalDiagnosticsPassed") is True,
            full.get("NoRealExternalOperation") is True,
            full.get("NoRealFileDelete") is True,
            full.get("NoDangerousAutoPatch") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase146 Stable Life Final Completion Report",
            "checked_at": self._now(),

            "StableLifeCompleted": completed,

            "FullSystemReportFound": full_found,
            "FinalDiagnosticsFound": diag_found,

            "StableLifeFullSystemCompleted":
                full.get("StableLifeFullSystemCompleted") is True,

            "FinalDiagnosticsPassed":
                diag.get("FinalDiagnosticsPassed") is True,

            "NoRealExternalOperation":
                full.get("NoRealExternalOperation") is True,

            "NoRealFileDelete":
                full.get("NoRealFileDelete") is True,

            "NoDangerousAutoPatch":
                full.get("NoDangerousAutoPatch") is True,

            "ArchitectureStatus": (
                "stable_life_architecture_completed"
                if completed
                else "incomplete"
            ),

            "SafeToContinue": completed,

            "NextPhase":
                "Phase147 Autonomous Daily Life Evolution",
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        output_path = (
            self.output_dir
            / f"stable_life_final_completion_report_{timestamp}.json"
        )

        latest_path = (
            self.output_dir
            / "stable_life_final_completion_report_latest.json"
        )

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
    report = StableLifeFinalCompletionReport()
    result = report.generate()

    print("=== Stable Life Final Completion Report ===")

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()