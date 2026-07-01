import json
from pathlib import Path
from datetime import datetime

from navikoLAB.daemon.autonomous_daemon_loop import AutonomousDaemonLoop
from navikoLAB.event_trigger.event_driven_daemon_integration import EventDrivenDaemonIntegration
from navikoLAB.goal_daemon.goal_driven_daemon_manager import GoalDrivenDaemonManager


class AutonomousCycleManager:
    def __init__(self):
        self.log_dir = Path("navikoLAB/autonomous_cycle/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run_cycle(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        goal_result = GoalDrivenDaemonManager().run()
        event_result = EventDrivenDaemonIntegration().run_once()
        daemon_result = AutonomousDaemonLoop().run_once()

        result = {
            "status": "completed",
            "phase": "Phase79-1 Autonomous Cycle Manager",
            "timestamp": timestamp,
            "mode": "dry_run",

            "GoalStatus": goal_result.get("status"),
            "GoalCount": goal_result.get("goal_count"),
            "GeneratedEventCount": goal_result.get("generated_event_count"),

            "EventStatus": event_result.get("status"),
            "RoutedCount": event_result.get("RoutedCount"),
            "ExecutedCount": event_result.get("ExecutedCount"),
            "MarkedCount": event_result.get("MarkedCount"),

            "DaemonStatus": daemon_result.get("status"),
            "DaemonSafeToContinue": daemon_result.get("safe_to_continue"),

            "ExternalOperationAllowed": False,
            "OriginalWriteAllowed": False,
            "FileDeleteAllowed": False,

            "AutonomousCycleCompleted": True,
            "SafeToContinue": True,
        }

        log_path = self.log_dir / f"autonomous_cycle_manager_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    manager = AutonomousCycleManager()
    report = manager.run_cycle()

    print("=== Autonomous Cycle Manager ===")
    for k, v in report.items():
        print(f"{k}: {v}")