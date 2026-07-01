import json
from pathlib import Path
from datetime import datetime


class GoalDrivenDaemonManager:
    def __init__(self):
        self.goal_dir = Path("navikoLAB/goal_daemon/goals")
        self.event_dir = Path("navikoLAB/event_trigger/events")
        self.log_dir = Path("navikoLAB/goal_daemon/logs")

        self.goal_dir.mkdir(parents=True, exist_ok=True)
        self.event_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        goals = self._load_goals()

        pending_goals = [
            g for g in goals
            if g.get("status") == "pending" and g.get("safe") is True
        ]

        generated_events = []

        for goal in pending_goals:
            event = {
                "type": "daemon",
                "status": "pending",
                "safe": True,
                "mode": "dry_run",
                "source": "goal_driven_daemon",
                "goal_id": goal.get("id"),
                "goal_title": goal.get("title"),
                "created_at": timestamp,
                "external_operation_allowed": False,
                "original_write_allowed": False,
                "file_delete_allowed": False,
            }

            event_path = self.event_dir / (
                f"goal_event_{goal.get('id', 'unknown')}_{timestamp}.json"
            )

            with event_path.open("w", encoding="utf-8") as f:
                json.dump(event, f, ensure_ascii=False, indent=2)

            generated_events.append(str(event_path))

        result = {
            "status": "completed",
            "phase": "Phase78-1 Goal Driven Daemon Manager",
            "timestamp": timestamp,
            "goal_count": len(goals),
            "pending_safe_goal_count": len(pending_goals),
            "generated_event_count": len(generated_events),
            "generated_events": generated_events,
            "mode": "dry_run",
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"goal_driven_daemon_manager_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result

    def _load_goals(self):
        goals = []

        for path in sorted(self.goal_dir.glob("*.json")):
            try:
                with path.open("r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, dict):
                    goals.append(data)
            except Exception:
                continue

        return goals


if __name__ == "__main__":
    manager = GoalDrivenDaemonManager()
    report = manager.run()

    print("=== Goal Driven Daemon Manager ===")
    for k, v in report.items():
        print(f"{k}: {v}")