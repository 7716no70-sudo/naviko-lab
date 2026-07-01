# navikoLAB/stable_life/self_repair_loop.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class SelfRepairLoop:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.required_paths = {
            "semantic_memory_index": self.root / "stable_life" / "semantic_memory" / "semantic_memory_index.json",
            "experience_learning_index": self.root / "stable_life" / "experience_learning" / "experience_learning_index.json",
            "stable_personality": self.root / "stable_life" / "personality" / "stable_personality.json",
            "stable_goal_tree": self.root / "stable_life" / "goals" / "stable_goal_tree.json",
        }

        self.repair_dir = self.root / "stable_life" / "self_repair"
        self.repair_dir.mkdir(parents=True, exist_ok=True)

        self.report_path = self.repair_dir / "self_repair_report.json"
        self.history_path = self.repair_dir / "self_repair_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def diagnose(self) -> dict[str, Any]:
        path_status = {}

        for name, path in self.required_paths.items():
            path_status[name] = {
                "path": str(path),
                "exists": path.exists(),
            }

        missing = [
            name
            for name, status in path_status.items()
            if not status["exists"]
        ]

        json_errors = []
        for name, path in self.required_paths.items():
            if not path.exists():
                continue
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                json_errors.append(
                    {
                        "name": name,
                        "path": str(path),
                        "error": str(e),
                    }
                )

        return {
            "checked_at": self._now(),
            "path_status": path_status,
            "missing": missing,
            "json_errors": json_errors,
            "healthy": not missing and not json_errors,
        }

    def build_repair_plan(self, diagnosis: dict[str, Any]) -> dict[str, Any]:
        actions = []

        for name in diagnosis.get("missing", []):
            actions.append(
                {
                    "target": name,
                    "action": "recreate_minimal_safe_file",
                    "risk": "low",
                    "auto_execute": False,
                    "reason": "required stable_life file is missing",
                }
            )

        for error in diagnosis.get("json_errors", []):
            actions.append(
                {
                    "target": error["name"],
                    "action": "backup_and_recreate_from_last_known_schema",
                    "risk": "medium",
                    "auto_execute": False,
                    "reason": "json parse error detected",
                }
            )

        if not actions:
            actions.append(
                {
                    "target": "stable_life_kernel",
                    "action": "no_repair_needed",
                    "risk": "none",
                    "auto_execute": False,
                    "reason": "all required files exist and JSON is valid",
                }
            )

        return {
            "created_at": self._now(),
            "repair_required": any(a["action"] != "no_repair_needed" for a in actions),
            "actions": actions,
        }

    def save_report(
        self,
        diagnosis: dict[str, Any],
        repair_plan: dict[str, Any],
    ) -> None:
        report = {
            "status": "completed",
            "phase": "Phase115-5 Self Repair Loop",
            "diagnosis": diagnosis,
            "repair_plan": repair_plan,
            "real_file_delete": False,
            "dangerous_auto_patch": False,
            "auto_repair_executed": False,
            "safe_to_continue": diagnosis.get("healthy", False),
            "created_at": self._now(),
        }

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

    def run(self) -> dict[str, Any]:
        diagnosis = self.diagnose()
        repair_plan = self.build_repair_plan(diagnosis)
        self.save_report(diagnosis, repair_plan)

        return {
            "status": "completed",
            "phase": "Phase115-5 Self Repair Loop",
            "Healthy": diagnosis["healthy"],
            "MissingCount": len(diagnosis["missing"]),
            "JsonErrorCount": len(diagnosis["json_errors"]),
            "RepairRequired": repair_plan["repair_required"],
            "AutoRepairExecuted": False,
            "RealFileDelete": False,
            "DangerousAutoPatch": False,
            "ReportPath": str(self.report_path),
            "SafeToContinue": diagnosis["healthy"],
        }


def main() -> None:
    loop = SelfRepairLoop()
    result = loop.run()

    print("=== Self Repair Loop ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()