# navikoLAB/stable_life/stable_life_controller.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from navikoLAB.stable_life.semantic_memory_engine import SemanticMemoryEngine
from navikoLAB.stable_life.experience_learning_engine import ExperienceLearningEngine
from navikoLAB.stable_life.personality_stabilizer import PersonalityStabilizer
from navikoLAB.stable_life.long_term_goal_maintainer import LongTermGoalMaintainer
from navikoLAB.stable_life.self_repair_loop import SelfRepairLoop
from navikoLAB.stable_life.existence_integrity_monitor import ExistenceIntegrityMonitor


class StableLifeController:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.controller_dir = self.root / "stable_life" / "controller"
        self.controller_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.controller_dir / "stable_life_controller_report.json"
        self.history_path = self.controller_dir / "stable_life_controller_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def run_cycle(self, experience_text: str) -> dict[str, Any]:
        cycle_started_at = self._now()

        semantic_result = SemanticMemoryEngine(self.root).process(experience_text)
        learning_result = ExperienceLearningEngine(self.root).process_all()
        personality_result = PersonalityStabilizer(self.root).stabilize()
        goal_result = LongTermGoalMaintainer(self.root).maintain()
        repair_result = SelfRepairLoop(self.root).run()
        integrity_result = ExistenceIntegrityMonitor(self.root).monitor()

        safe_results = [
            semantic_result.get("SafeToContinue") is True,
            learning_result.get("SafeToContinue") is True,
            personality_result.get("SafeToContinue") is True,
            goal_result.get("SafeToContinue") is True,
            repair_result.get("SafeToContinue") is True,
            integrity_result.get("safe_to_continue") is True,
        ]

        stable_life_cycle_completed = all(safe_results)

        report = {
            "status": "completed",
            "phase": "Phase115-7 Stable Life Controller",
            "cycle_started_at": cycle_started_at,
            "cycle_completed_at": self._now(),
            "experience_text": experience_text,
            "semantic_result": semantic_result,
            "learning_result": learning_result,
            "personality_learning_count": personality_result.get("LearningItemCount"),
            "goal_today_count": goal_result.get("TodayGoalCount"),
            "repair_healthy": repair_result.get("Healthy"),
            "integrity_score": integrity_result.get("integrity_score"),
            "stable_life_cycle_completed": stable_life_cycle_completed,
            "safe_to_continue": stable_life_cycle_completed,
            "real_external_operation": False,
            "real_file_delete": False,
            "dangerous_auto_patch": False,
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
    controller = StableLifeController()

    sample = "Phase115 Stable Life Kernel の統合ライフサイクルを実行した"
    result = controller.run_cycle(sample)

    print("=== Stable Life Controller ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"StableLifeCycleCompleted: {result['stable_life_cycle_completed']}")
    print(f"IntegrityScore: {result['integrity_score']}")
    print(f"RepairHealthy: {result['repair_healthy']}")
    print(f"PersonalityLearningCount: {result['personality_learning_count']}")
    print(f"GoalTodayCount: {result['goal_today_count']}")
    print(f"RealExternalOperation: {result['real_external_operation']}")
    print(f"RealFileDelete: {result['real_file_delete']}")
    print(f"DangerousAutoPatch: {result['dangerous_auto_patch']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")


if __name__ == "__main__":
    main()