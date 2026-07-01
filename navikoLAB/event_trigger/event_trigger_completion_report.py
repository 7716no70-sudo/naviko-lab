import json
from pathlib import Path
from datetime import datetime

from navikoLAB.event_trigger.event_trigger_manager import EventTriggerManager
from navikoLAB.event_trigger.event_trigger_router import EventTriggerRouter


def main():
    manager_result = EventTriggerManager().scan_events()
    router_result = EventTriggerRouter().route()

    safe_to_continue = (
        manager_result.get("status") == "completed"
        and router_result.get("status") == "completed"
        and manager_result.get("event_directory_exists") is True
        and router_result.get("safe_to_continue") is True
    )

    report = {
        "status": "completed",
        "phase": "Phase75-4 Event Trigger Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "EventDirectoryExists": manager_result.get("event_directory_exists"),
        "EventCount": manager_result.get("event_count"),
        "SafeEventCount": manager_result.get("safe_event_count"),
        "TriggerAllowed": manager_result.get("trigger_allowed"),
        "RouterStatus": router_result.get("status"),
        "RoutedCount": router_result.get("routed_count"),
        "ExecutedCount": router_result.get("executed_count"),
        "Mode": router_result.get("mode"),
        "ExternalOperationAllowed": router_result.get("external_operation_allowed"),
        "OriginalWriteAllowed": router_result.get("original_write_allowed"),
        "FileDeleteAllowed": router_result.get("file_delete_allowed"),
        "SafeToContinue": safe_to_continue,
        "Phase75Completed": True,
        "NextPhase": "Phase76 Event Test Generator",
    }

    report_dir = Path("navikoLAB/event_trigger/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / (
        f"event_trigger_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Event Trigger Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()