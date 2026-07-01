# navikoLAB/stable_life/stable_life_runtime_scheduler.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_adapter import StableLifeRuntimeAdapter
from navikoLAB.stable_life.stable_life_runtime_unified_report import StableLifeRuntimeUnifiedReport


class StableLifeRuntimeScheduler:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.output_dir = self.root / "stable_life" / "scheduler"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.output_dir / "stable_life_runtime_scheduler_report.json"
        self.history_path = self.output_dir / "stable_life_runtime_scheduler_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run_scheduled_cycles(self, cycle_count: int = 2) -> dict[str, Any]:
        adapter = StableLifeRuntimeAdapter(self.root)
        started_at = self._now()

        cycles: list[dict[str, Any]] = []

        for i in range(1, cycle_count + 1):
            event = {
                "event_type": "scheduled_stable_life_cycle",
                "cycle": i,
                "text": f"Phase131 scheduler cycle {i} としてStable Life Runtimeを実行した",
                "source": "dry_run_scheduler",
            }

            adapter_result = adapter.run_from_runtime(event)

            cycles.append(
                {
                    "cycle": i,
                    "runtime_integrated": adapter_result.get("stable_life_runtime_integrated") is True,
                    "safe_to_continue": adapter_result.get("safe_to_continue") is True,
                    "integrity_score": adapter_result.get("integrity_score"),
                }
            )

        unified_result = StableLifeRuntimeUnifiedReport(self.root).generate()

        completed_count = sum(1 for c in cycles if c["runtime_integrated"])
        safe_count = sum(1 for c in cycles if c["safe_to_continue"])

        scheduler_ready = (
            completed_count == cycle_count
            and safe_count == cycle_count
            and unified_result.get("StableLifeRuntimeUnified") is True
        )

        result = {
            "status": "completed",
            "phase": "Phase131 Stable Life Runtime Scheduler",
            "started_at": started_at,
            "completed_at": self._now(),
            "CycleCount": cycle_count,
            "CompletedCycleCount": completed_count,
            "SafeCycleCount": safe_count,
            "StableLifeRuntimeUnified": unified_result.get("StableLifeRuntimeUnified") is True,
            "SchedulerReady": scheduler_ready,
            "SchedulerMode": "dry_run_fixed_cycle",
            "RealBackgroundDaemon": False,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": scheduler_ready,
            "NextPhase": "Phase132 Scheduler Diagnostics",
            "CycleResults": cycles,
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
    scheduler = StableLifeRuntimeScheduler()
    result = scheduler.run_scheduled_cycles(cycle_count=2)

    print("=== Stable Life Runtime Scheduler ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"CycleCount: {result['CycleCount']}")
    print(f"CompletedCycleCount: {result['CompletedCycleCount']}")
    print(f"SafeCycleCount: {result['SafeCycleCount']}")
    print(f"StableLifeRuntimeUnified: {result['StableLifeRuntimeUnified']}")
    print(f"SchedulerReady: {result['SchedulerReady']}")
    print(f"SchedulerMode: {result['SchedulerMode']}")
    print(f"RealBackgroundDaemon: {result['RealBackgroundDaemon']}")
    print(f"RealExternalOperation: {result['RealExternalOperation']}")
    print(f"RealFileDelete: {result['RealFileDelete']}")
    print(f"DangerousAutoPatch: {result['DangerousAutoPatch']}")
    print("--- CycleResults ---")
    for item in result["CycleResults"]:
        print(
            f"cycle {item['cycle']}: "
            f"runtime_integrated={item['runtime_integrated']}, "
            f"safe={item['safe_to_continue']}, "
            f"integrity={item['integrity_score']}"
        )
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()