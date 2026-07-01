import json
from pathlib import Path
from datetime import datetime

from navikoLAB.goal_daemon.goal_driven_daemon_manager import GoalDrivenDaemonManager
from navikoLAB.event_trigger.event_driven_daemon_integration import EventDrivenDaemonIntegration


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    goal_result = GoalDrivenDaemonManager().run()
    event_result = EventDrivenDaemonIntegration().run_once()

    result = {
        "status": "completed",
        "phase": "Phase78-3 Goal Execution Test",
        "timestamp": timestamp,
        "GoalManagerStatus": goal_result.get("status"),
        "GoalCount": goal_result.get("goal_count"),
        "PendingSafeGoalCount": goal_result.get("pending_safe_goal_count"),
        "GeneratedEventCount": goal_result.get("generated_event_count"),
        "EventIntegrationStatus": event_result.get("status"),
        "RoutedCount": event_result.get("RoutedCount"),
        "ExecutedCount": event_result.get("ExecutedCount"),
        "MarkedCount": event_result.get("MarkedCount"),
        "Mode": goal_result.get("mode"),
        "GoalToEventPassed": goal_result.get("generated_event_count", 0) > 0,
        "EventToDaemonPassed": event_result.get("ExecutedCount", 0) > 0,
        "SafeToContinue": (
            goal_result.get("status") == "completed"
            and event_result.get("status") == "completed"
            and goal_result.get("safe_to_continue") is True
            and event_result.get("SafeToContinue") is True
        ),
    }

    log_dir = Path("navikoLAB/goal_daemon/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"goal_execution_test_{timestamp}.json"

    with log_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("=== Goal Execution Test ===")
    for k, v in result.items():
        print(f"{k}: {v}")

    print(f"LogPath: {log_path}")


if __name__ == "__main__":
    main()