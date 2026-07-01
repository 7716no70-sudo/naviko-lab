import json
from pathlib import Path
from datetime import datetime


class GoalTestGenerator:
    def __init__(self):
        self.goal_dir = Path("navikoLAB/goal_daemon/goals")
        self.log_dir = Path("navikoLAB/goal_daemon/logs")

        self.goal_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def generate(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        goal = {
            "id": f"test_goal_{timestamp}",
            "title": "Phase78 safe goal daemon test",
            "status": "pending",
            "safe": True,
            "priority": "low",
            "mode": "dry_run",
            "created_at": timestamp,
            "description": "Goal Driven Daemon の安全テスト用ゴール",
            "external_operation_allowed": False,
            "original_write_allowed": False,
            "file_delete_allowed": False,
        }

        goal_path = self.goal_dir / f"{goal['id']}.json"

        with goal_path.open("w", encoding="utf-8") as f:
            json.dump(goal, f, ensure_ascii=False, indent=2)

        result = {
            "status": "completed",
            "phase": "Phase78-2 Goal Test Generator",
            "timestamp": timestamp,
            "test_goal_created": True,
            "goal_path": str(goal_path),
            "goal_id": goal["id"],
            "goal_safe": goal["safe"],
            "goal_status": goal["status"],
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"goal_test_generator_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    generator = GoalTestGenerator()
    report = generator.generate()

    print("=== Goal Test Generator ===")
    for k, v in report.items():
        print(f"{k}: {v}")