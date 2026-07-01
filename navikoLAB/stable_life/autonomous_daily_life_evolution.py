# navikoLAB/stable_life/autonomous_daily_life_evolution.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.stable_life_runtime_adapter import StableLifeRuntimeAdapter
from navikoLAB.stable_life.long_term_life_memory_consolidation import (
    LongTermLifeMemoryConsolidation,
)
from navikoLAB.stable_life.life_memory_reflection_engine import (
    LifeMemoryReflectionEngine,
)
from navikoLAB.stable_life.stable_life_final_completion_report import (
    StableLifeFinalCompletionReport,
)


class AutonomousDailyLifeEvolution:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.output_dir = self.root / "stable_life" / "daily_life_evolution"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.output_dir / "autonomous_daily_life_evolution_report.json"
        self.history_path = self.output_dir / "autonomous_daily_life_evolution_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run_daily_cycle(self, daily_experience: str) -> dict[str, Any]:
        started_at = self._now()

        runtime_result = StableLifeRuntimeAdapter(self.root).run_from_runtime(
            {
                "event_type": "daily_life_experience",
                "text": daily_experience,
                "source": "phase147_daily_life_evolution",
            }
        )

        memory_result = LongTermLifeMemoryConsolidation(self.root).consolidate()
        reflection_result = LifeMemoryReflectionEngine(self.root).reflect()
        final_result = StableLifeFinalCompletionReport(self.root).generate()

        daily_evolution_completed = all([
            runtime_result.get("safe_to_continue") is True,
            memory_result.get("SafeToContinue") is True,
            reflection_result.get("SafeToContinue") is True,
            final_result.get("SafeToContinue") is True,
        ])

        result = {
            "status": "completed",
            "phase": "Phase147 Autonomous Daily Life Evolution",
            "started_at": started_at,
            "completed_at": self._now(),
            "DailyExperience": daily_experience,
            "RuntimeIntegrated": runtime_result.get("stable_life_runtime_integrated") is True,
            "LongTermLifeMemoryReady": memory_result.get("LongTermLifeMemoryReady") is True,
            "ReflectionReady": reflection_result.get("ReflectionReady") is True,
            "StableLifeCompleted": final_result.get("StableLifeCompleted") is True,
            "DailyEvolutionCompleted": daily_evolution_completed,
            "DominantMeaning": memory_result.get("DominantMeaning"),
            "DominantConcept": memory_result.get("DominantConcept"),
            "DominantLearningCategory": memory_result.get("DominantLearningCategory"),
            "ReflectionText": reflection_result.get("ReflectionText"),
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": daily_evolution_completed,
            "NextPhase": "Phase148 Daily Life Evolution Diagnostics",
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
    evolution = AutonomousDailyLifeEvolution()

    result = evolution.run_daily_cycle(
        "Phase147として、Navikoは安定した生命基盤の上で日常経験を1件取り込み、記憶と反省へ接続した。"
    )

    print("=== Autonomous Daily Life Evolution ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"RuntimeIntegrated: {result['RuntimeIntegrated']}")
    print(f"LongTermLifeMemoryReady: {result['LongTermLifeMemoryReady']}")
    print(f"ReflectionReady: {result['ReflectionReady']}")
    print(f"StableLifeCompleted: {result['StableLifeCompleted']}")
    print(f"DailyEvolutionCompleted: {result['DailyEvolutionCompleted']}")
    print(f"DominantMeaning: {result['DominantMeaning']}")
    print(f"DominantConcept: {result['DominantConcept']}")
    print(f"DominantLearningCategory: {result['DominantLearningCategory']}")
    print(f"RealExternalOperation: {result['RealExternalOperation']}")
    print(f"RealFileDelete: {result['RealFileDelete']}")
    print(f"DangerousAutoPatch: {result['DangerousAutoPatch']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"NextPhase: {result['NextPhase']}")


if __name__ == "__main__":
    main()