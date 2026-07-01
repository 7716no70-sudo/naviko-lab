import json
from pathlib import Path
from datetime import datetime

from navikoLAB.event_trigger.event_trigger_router import EventTriggerRouter


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    router_result = EventTriggerRouter().route()

    executed = router_result.get("executed_count", 0) > 0
    routed = router_result.get("routed_count", 0) > 0

    result = {
        "status": "completed",
        "phase": "Phase76-2 Event Execution Test",
        "timestamp": timestamp,
        "RouterStatus": router_result.get("status"),
        "SafeEventCount": router_result.get("safe_event_count"),
        "RoutedCount": router_result.get("routed_count"),
        "ExecutedCount": router_result.get("executed_count"),
        "DaemonResultCount": router_result.get("daemon_result_count"),
        "EventRouted": routed,
        "EventExecuted": executed,
        "Mode": router_result.get("mode"),
        "ExternalOperationAllowed": router_result.get("external_operation_allowed"),
        "OriginalWriteAllowed": router_result.get("original_write_allowed"),
        "FileDeleteAllowed": router_result.get("file_delete_allowed"),
        "SafeToContinue": router_result.get("safe_to_continue"),
    }

    log_dir = Path("navikoLAB/event_trigger/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"event_execution_test_{timestamp}.json"

    with log_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("=== Event Execution Test ===")
    for k, v in result.items():
        print(f"{k}: {v}")

    print(f"LogPath: {log_path}")


if __name__ == "__main__":
    main()