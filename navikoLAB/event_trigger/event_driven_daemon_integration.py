import json
from pathlib import Path
from datetime import datetime

from navikoLAB.event_trigger.event_trigger_router import EventTriggerRouter
from navikoLAB.event_trigger.event_processed_marker import EventProcessedMarker


class EventDrivenDaemonIntegration:
    def __init__(self):
        self.log_dir = Path("navikoLAB/event_trigger/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run_once(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        router_result = EventTriggerRouter().route()
        marker_result = EventProcessedMarker().mark_processed()

        result = {
            "status": "completed",
            "phase": "Phase77-1 Event Driven Daemon Integration",
            "timestamp": timestamp,
            "RouterStatus": router_result.get("status"),
            "SafeEventCount": router_result.get("safe_event_count"),
            "RoutedCount": router_result.get("routed_count"),
            "ExecutedCount": router_result.get("executed_count"),
            "MarkerStatus": marker_result.get("status"),
            "MarkedCount": marker_result.get("marked_count"),
            "Mode": router_result.get("mode"),
            "ExternalOperationAllowed": router_result.get("external_operation_allowed"),
            "OriginalWriteAllowed": router_result.get("original_write_allowed"),
            "FileDeleteAllowed": router_result.get("file_delete_allowed"),
            "SafeToContinue": (
                router_result.get("status") == "completed"
                and marker_result.get("status") == "completed"
                and router_result.get("safe_to_continue") is True
            ),
        }

        log_path = self.log_dir / f"event_driven_daemon_integration_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    integration = EventDrivenDaemonIntegration()
    report = integration.run_once()

    print("=== Event Driven Daemon Integration ===")
    for k, v in report.items():
        print(f"{k}: {v}")