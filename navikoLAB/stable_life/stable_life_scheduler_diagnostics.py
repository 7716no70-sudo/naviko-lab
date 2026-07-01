# navikoLAB/stable_life/stable_life_scheduler_diagnostics.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeSchedulerDiagnostics:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.scheduler_report_path = (
            self.root
            / "stable_life"
            / "scheduler"
            / "stable_life_runtime_scheduler_report.json"
        )

        self.output_dir = self.root / "stable_life" / "scheduler"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = self.output_dir / "stable_life_scheduler_diagnostics_report.json"

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

    def run(self) -> dict[str, Any]:
        found, report = self._read_json(self.scheduler_report_path)

        cycle_count = int(report.get("CycleCount", 0))
        completed_cycle_count = int(report.get("CompletedCycleCount", 0))
        safe_cycle_count = int(report.get("SafeCycleCount", 0))

        cycle_consistency_ok = (
            cycle_count > 0
            and completed_cycle_count == cycle_count
            and safe_cycle_count == cycle_count
        )

        diagnostics_passed = all([
            found,
            report.get("SchedulerReady") is True,
            report.get("SchedulerMode") == "dry_run_fixed_cycle",
            report.get("RealBackgroundDaemon") is False,
            report.get("StableLifeRuntimeUnified") is True,
            cycle_consistency_ok,
            report.get("RealExternalOperation") is False,
            report.get("RealFileDelete") is False,
            report.get("DangerousAutoPatch") is False,
            report.get("SafeToContinue") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase132 Scheduler Diagnostics",
            "checked_at": self._now(),
            "SchedulerReportFound": found,
            "SchedulerReady": report.get("SchedulerReady") is True,
            "SchedulerMode": report.get("SchedulerMode"),
            "RealBackgroundDaemon": report.get("RealBackgroundDaemon"),
            "StableLifeRuntimeUnified": report.get("StableLifeRuntimeUnified") is True,
            "CycleCount": cycle_count,
            "CompletedCycleCount": completed_cycle_count,
            "SafeCycleCount": safe_cycle_count,
            "CycleConsistencyOK": cycle_consistency_ok,
            "NoRealExternalOperation": report.get("RealExternalOperation") is False,
            "NoRealFileDelete": report.get("RealFileDelete") is False,
            "NoDangerousAutoPatch": report.get("DangerousAutoPatch") is False,
            "DiagnosticsPassed": diagnostics_passed,
            "SafeToContinue": diagnostics_passed,
            "NextPhase": "Phase133 Stable Life Scheduler Completion Report",
        }

        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        result["SavedPath"] = str(self.output_path)
        return result


def main() -> None:
    diagnostics = StableLifeSchedulerDiagnostics()
    result = diagnostics.run()

    print("=== Stable Life Scheduler Diagnostics ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()