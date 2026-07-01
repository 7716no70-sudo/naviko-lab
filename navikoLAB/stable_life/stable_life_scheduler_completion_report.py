# navikoLAB/stable_life/stable_life_scheduler_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeSchedulerCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.scheduler_report_path = (
            self.root / "stable_life" / "scheduler"
            / "stable_life_runtime_scheduler_report.json"
        )
        self.diagnostics_report_path = (
            self.root / "stable_life" / "scheduler"
            / "stable_life_scheduler_diagnostics_report.json"
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
        scheduler_found, scheduler = self._read_json(self.scheduler_report_path)
        diagnostics_found, diagnostics = self._read_json(self.diagnostics_report_path)

        scheduler_completed = all([
            scheduler_found,
            diagnostics_found,
            scheduler.get("SchedulerReady") is True,
            scheduler.get("SchedulerMode") == "dry_run_fixed_cycle",
            scheduler.get("RealBackgroundDaemon") is False,
            scheduler.get("SafeToContinue") is True,
            diagnostics.get("DiagnosticsPassed") is True,
            diagnostics.get("CycleConsistencyOK") is True,
            diagnostics.get("SafeToContinue") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase133 Stable Life Scheduler Completion Report",
            "checked_at": self._now(),
            "StableLifeSchedulerCompleted": scheduler_completed,
            "SchedulerReportFound": scheduler_found,
            "DiagnosticsReportFound": diagnostics_found,
            "SchedulerReady": scheduler.get("SchedulerReady") is True,
            "SchedulerMode": scheduler.get("SchedulerMode"),
            "RealBackgroundDaemon": scheduler.get("RealBackgroundDaemon"),
            "CycleCount": scheduler.get("CycleCount"),
            "CompletedCycleCount": scheduler.get("CompletedCycleCount"),
            "SafeCycleCount": scheduler.get("SafeCycleCount"),
            "CycleConsistencyOK": diagnostics.get("CycleConsistencyOK") is True,
            "DiagnosticsPassed": diagnostics.get("DiagnosticsPassed") is True,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": scheduler_completed,
            "NextPhase": "Phase134 Stable Life Runtime Command Interface",
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"stable_life_scheduler_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "stable_life_scheduler_completion_report_latest.json"

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
    report = StableLifeSchedulerCompletionReport()
    result = report.generate()

    print("=== Stable Life Scheduler Completion Report ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()