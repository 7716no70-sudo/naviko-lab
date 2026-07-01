# navikoLAB/stable_life/persistent_life_runtime_loop.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_adapter import StableLifeRuntimeAdapter


class PersistentLifeRuntimeLoop:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.loop_dir = self.root / "stable_life" / "persistent_runtime"
        self.loop_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.loop_dir / "persistent_life_runtime_loop_report.json"
        self.history_path = self.loop_dir / "persistent_life_runtime_loop_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run_loop(self, cycle_count: int = 3) -> dict[str, Any]:
        started_at = self._now()
        adapter = StableLifeRuntimeAdapter(self.root)

        cycle_results = []

        for i in range(1, cycle_count + 1):
            runtime_event = {
                "event_type": "persistent_life_cycle",
                "cycle": i,
                "text": f"Phase118 Persistent Life Runtime Loop cycle {i} を実行した",
                "source": "dry_run_persistent_life_loop",
            }

            result = adapter.run_from_runtime(runtime_event)

            cycle_results.append(
                {
                    "cycle": i,
                    "completed": result.get("stable_life_runtime_integrated") is True,
                    "safe_to_continue": result.get("safe_to_continue") is True,
                    "integrity_score": result.get("integrity_score"),
                }
            )

        completed_count = sum(1 for r in cycle_results if r["completed"])
        safe_count = sum(1 for r in cycle_results if r["safe_to_continue"])

        persistent_loop_completed = (
            completed_count == cycle_count
            and safe_count == cycle_count
        )

        report = {
            "status": "completed",
            "phase": "Phase118 Persistent Life Runtime Loop",
            "started_at": started_at,
            "completed_at": self._now(),
            "CycleCount": cycle_count,
            "CompletedCycleCount": completed_count,
            "SafeCycleCount": safe_count,
            "PersistentLifeRuntimeLoopCompleted": persistent_loop_completed,
            "CycleResults": cycle_results,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": persistent_loop_completed,
            "NextPhase": "Phase119 Life Runtime Diagnostics",
        }

        self._save(report)
        return report

    def _save(self, report: dict[str, Any]) -> None:
        self.report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

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
    loop = PersistentLifeRuntimeLoop()
    result = loop.run_loop(cycle_count=3)

    print("=== Persistent Life Runtime Loop ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"CycleCount: {result['CycleCount']}")
    print(f"CompletedCycleCount: {result['CompletedCycleCount']}")
    print(f"SafeCycleCount: {result['SafeCycleCount']}")
    print(f"PersistentLifeRuntimeLoopCompleted: {result['PersistentLifeRuntimeLoopCompleted']}")

    print("--- CycleResults ---")
    for item in result["CycleResults"]:
        print(
            f"cycle {item['cycle']}: "
            f"completed={item['completed']}, "
            f"safe={item['safe_to_continue']}, "
            f"integrity={item['integrity_score']}"
        )

    print(f"RealExternalOperation: {result['RealExternalOperation']}")
    print(f"RealFileDelete: {result['RealFileDelete']}")
    print(f"DangerousAutoPatch: {result['DangerousAutoPatch']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()