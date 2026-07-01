# navikoLAB/stable_life/existence_integrity_monitor.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ExistenceIntegrityMonitor:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.targets = {
            "semantic_memory": self.root / "stable_life" / "semantic_memory" / "semantic_memory_index.json",
            "experience_learning": self.root / "stable_life" / "experience_learning" / "experience_learning_index.json",
            "personality": self.root / "stable_life" / "personality" / "stable_personality.json",
            "goals": self.root / "stable_life" / "goals" / "stable_goal_tree.json",
            "self_repair": self.root / "stable_life" / "self_repair" / "self_repair_report.json",
        }

        self.monitor_dir = self.root / "stable_life" / "existence_integrity"
        self.monitor_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.monitor_dir / "existence_integrity_report.json"
        self.history_path = self.monitor_dir / "existence_integrity_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def _read_json_safe(self, path: Path) -> tuple[bool, Any, str | None]:
        if not path.exists():
            return False, None, "missing"

        try:
            return True, json.loads(path.read_text(encoding="utf-8")), None
        except Exception as e:
            return False, None, str(e)

    def inspect_target(self, name: str, path: Path) -> dict[str, Any]:
        ok, data, error = self._read_json_safe(path)

        score = 0.0
        details: dict[str, Any] = {
            "name": name,
            "path": str(path),
            "exists": path.exists(),
            "json_ok": ok,
            "error": error,
        }

        if ok:
            score += 0.5

            if isinstance(data, dict):
                if data.get("count", 0) > 0:
                    score += 0.25
                if data.get("SafeToContinue") is True or data.get("safe_to_continue") is True:
                    score += 0.25
                if name == "personality" and "updated_at" in data:
                    score += 0.25
                if name == "goals" and "dream" in data:
                    score += 0.25

            score = min(score, 1.0)

        details["score"] = round(score, 3)
        return details

    def monitor(self) -> dict[str, Any]:
        inspections = {
            name: self.inspect_target(name, path)
            for name, path in self.targets.items()
        }

        scores = [item["score"] for item in inspections.values()]
        integrity_score = round(sum(scores) / len(scores), 3) if scores else 0.0

        healthy_targets = [
            name for name, item in inspections.items()
            if item["exists"] and item["json_ok"]
        ]

        failed_targets = [
            name for name, item in inspections.items()
            if not item["exists"] or not item["json_ok"]
        ]

        stable = integrity_score >= 0.75 and not failed_targets

        report = {
            "status": "completed",
            "phase": "Phase115-6 Existence Integrity Monitor",
            "checked_at": self._now(),
            "target_count": len(self.targets),
            "healthy_target_count": len(healthy_targets),
            "failed_target_count": len(failed_targets),
            "integrity_score": integrity_score,
            "stable": stable,
            "healthy_targets": healthy_targets,
            "failed_targets": failed_targets,
            "inspections": inspections,
            "safe_to_continue": stable,
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
    monitor = ExistenceIntegrityMonitor()
    result = monitor.monitor()

    print("=== Existence Integrity Monitor ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"TargetCount: {result['target_count']}")
    print(f"HealthyTargetCount: {result['healthy_target_count']}")
    print(f"FailedTargetCount: {result['failed_target_count']}")
    print(f"IntegrityScore: {result['integrity_score']}")
    print(f"Stable: {result['stable']}")
    print(f"SafeToContinue: {result['safe_to_continue']}")


if __name__ == "__main__":
    main()