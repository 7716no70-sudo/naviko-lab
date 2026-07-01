import json
from pathlib import Path
from datetime import datetime

from navikoLAB.event_trigger.event_trigger_manager import EventTriggerManager
from navikoLAB.daemon.autonomous_daemon_loop import AutonomousDaemonLoop


class EventTriggerRouter:
    def __init__(self):
        self.log_dir = Path("navikoLAB/event_trigger/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def route(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        scan = EventTriggerManager().scan_events()

        safe_events = [
            e for e in scan.get("events", [])
            if e.get("status") == "pending" and e.get("safe") is True
        ]

        routed_events = []
        daemon_results = []

        for event in safe_events:
            event_type = event.get("type")

            route_target = self._resolve_route_target(event_type)

            routed = {
                "event_path": event.get("path"),
                "event_type": event_type,
                "route_target": route_target,
                "routed": route_target is not None,
                "executed": False,
                "mode": "dry_run",
            }

            if route_target == "daemon":
                daemon_result = AutonomousDaemonLoop().run_once()
                routed["executed"] = True
                routed["daemon_log_path"] = daemon_result.get("log_path")
                daemon_results.append(daemon_result)

            routed_events.append(routed)

        result = {
            "status": "completed",
            "phase": "Phase75-3 Event Trigger Router",
            "timestamp": timestamp,
            "scan_status": scan.get("status"),
            "event_count": scan.get("event_count"),
            "safe_event_count": len(safe_events),
            "routed_count": len([e for e in routed_events if e.get("routed")]),
            "executed_count": len([e for e in routed_events if e.get("executed")]),
            "mode": "dry_run",
            "routed_events": routed_events,
            "daemon_result_count": len(daemon_results),
            "external_operation_allowed": False,
            "original_write_allowed": False,
            "file_delete_allowed": False,
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"event_trigger_router_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result

    def _resolve_route_target(self, event_type):
        route_map = {
            "daemon": "daemon",
            "health_check": "daemon",
            "stability_check": "daemon",
            "backup_check": "daemon",
            "recovery_check": "daemon",
            "planning_check": "daemon",
        }

        return route_map.get(event_type)


if __name__ == "__main__":
    router = EventTriggerRouter()
    report = router.route()

    print("=== Event Trigger Router ===")
    for k, v in report.items():
        print(f"{k}: {v}")