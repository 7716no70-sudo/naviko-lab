# navikoLAB/stable_life/stable_life_completion_report.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StableLifeCompletionReport:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.required_files = {
            "semantic_memory_engine": self.root / "stable_life" / "semantic_memory_engine.py",
            "experience_learning_engine": self.root / "stable_life" / "experience_learning_engine.py",
            "personality_stabilizer": self.root / "stable_life" / "personality_stabilizer.py",
            "long_term_goal_maintainer": self.root / "stable_life" / "long_term_goal_maintainer.py",
            "self_repair_loop": self.root / "stable_life" / "self_repair_loop.py",
            "existence_integrity_monitor": self.root / "stable_life" / "existence_integrity_monitor.py",
            "stable_life_controller": self.root / "stable_life" / "stable_life_controller.py",
        }

        self.required_reports = {
            "semantic_memory_index": self.root / "stable_life" / "semantic_memory" / "semantic_memory_index.json",
            "experience_learning_index": self.root / "stable_life" / "experience_learning" / "experience_learning_index.json",
            "stable_personality": self.root / "stable_life" / "personality" / "stable_personality.json",
            "stable_goal_tree": self.root / "stable_life" / "goals" / "stable_goal_tree.json",
            "self_repair_report": self.root / "stable_life" / "self_repair" / "self_repair_report.json",
            "existence_integrity_report": self.root / "stable_life" / "existence_integrity" / "existence_integrity_report.json",
            "stable_life_controller_report": self.root / "stable_life" / "controller" / "stable_life_controller_report.json",
        }

        self.output_dir = self.root / "stable_life" / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json_safe(self, path: Path) -> tuple[bool, dict[str, Any] | None]:
        if not path.exists():
            return False, None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return True, data
            return False, None
        except Exception:
            return False, None

    def generate(self) -> dict[str, Any]:
        file_status = {
            name: path.exists()
            for name, path in self.required_files.items()
        }

        report_status = {}
        report_data = {}

        for name, path in self.required_reports.items():
            ok, data = self._read_json_safe(path)
            report_status[name] = ok
            report_data[name] = data

        missing_files = [
            name for name, ok in file_status.items()
            if not ok
        ]

        missing_or_invalid_reports = [
            name for name, ok in report_status.items()
            if not ok
        ]

        integrity_score = 0.0
        integrity_report = report_data.get("existence_integrity_report") or {}
        if isinstance(integrity_report, dict):
            integrity_score = float(integrity_report.get("integrity_score", 0.0))

        controller_report = report_data.get("stable_life_controller_report") or {}
        controller_completed = bool(
            controller_report.get("stable_life_cycle_completed") is True
        )

        repair_report = report_data.get("self_repair_report") or {}
        repair_healthy = bool(
            repair_report.get("safe_to_continue") is True
        )

        semantic_index = report_data.get("semantic_memory_index") or {}
        semantic_count = int(semantic_index.get("count", 0))

        learning_index = report_data.get("experience_learning_index") or {}
        learning_count = int(learning_index.get("count", 0))

        personality = report_data.get("stable_personality") or {}
        personality_ready = bool(personality.get("updated_at"))

        goals = report_data.get("stable_goal_tree") or {}
        goals_ready = bool(goals.get("dream")) and bool(goals.get("today"))

        stable_life_kernel_completed = (
            not missing_files
            and not missing_or_invalid_reports
            and integrity_score >= 0.75
            and controller_completed
            and repair_healthy
            and semantic_count > 0
            and learning_count > 0
            and personality_ready
            and goals_ready
        )

        result = {
            "status": "completed",
            "phase": "Phase116 Stable Life Kernel Completion Report",
            "checked_at": self._now(),
            "StableLifeKernelCompleted": stable_life_kernel_completed,
            "RequiredFileCount": len(self.required_files),
            "MissingFileCount": len(missing_files),
            "RequiredReportCount": len(self.required_reports),
            "MissingOrInvalidReportCount": len(missing_or_invalid_reports),
            "SemanticMemoryCount": semantic_count,
            "ExperienceLearningCount": learning_count,
            "PersonalityReady": personality_ready,
            "GoalsReady": goals_ready,
            "RepairHealthy": repair_healthy,
            "ControllerCompleted": controller_completed,
            "IntegrityScore": integrity_score,
            "RealExternalOperation": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "SafeToContinue": stable_life_kernel_completed,
            "NextPhase": "Phase117 Stable Life Runtime Integration",
            "MissingFiles": missing_files,
            "MissingOrInvalidReports": missing_or_invalid_reports,
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"stable_life_completion_report_{timestamp}.json"
        latest_path = self.output_dir / "stable_life_completion_report_latest.json"

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
    report = StableLifeCompletionReport()
    result = report.generate()

    print("=== Stable Life Kernel Completion Report ===")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"- {item}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()