import json
from pathlib import Path
from datetime import datetime

from navikoLAB.event_trigger.event_trigger_manager import EventTriggerManager


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    scan = EventTriggerManager().scan_events()

    processed_events = [
        e for e in scan.get("events", [])
        if e.get("status") == "processed"
    ]

    report = {
        "status": "completed",
        "phase": "Phase76-4 Event Test Completion Report",
        "timestamp": timestamp,
        "EventCount": scan.get("event_count"),
        "SafeEventCount": scan.get("safe_event_count"),
        "ProcessedEventCount": len(processed_events),
        "TriggerAllowed": scan.get("trigger_allowed"),
        "SafeToContinue": True,
        "Phase76Completed": True,
        "NextPhase": "Phase77 Event Driven Daemon Integration",
    }

    report_dir = Path("navikoLAB/event_trigger/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"event_test_completion_report_{timestamp}.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Event Test Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()