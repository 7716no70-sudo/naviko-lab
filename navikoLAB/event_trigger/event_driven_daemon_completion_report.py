import json
from pathlib import Path
from datetime import datetime

from navikoLAB.event_trigger.event_driven_daemon_integration import (
    EventDrivenDaemonIntegration,
)


def main():
    integration = EventDrivenDaemonIntegration()
    result = integration.run_once()

    safe_to_continue = (
        result.get("status") == "completed"
        and result.get("SafeToContinue") is True
    )

    report = {
        "status": "completed",
        "phase": "Phase77-3 Event Driven Daemon Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "RouterStatus": result.get("RouterStatus"),
        "MarkerStatus": result.get("MarkerStatus"),
        "SafeEventCount": result.get("SafeEventCount"),
        "RoutedCount": result.get("RoutedCount"),
        "ExecutedCount": result.get("ExecutedCount"),
        "MarkedCount": result.get("MarkedCount"),
        "Mode": result.get("Mode"),
        "ExternalOperationAllowed": result.get("ExternalOperationAllowed"),
        "OriginalWriteAllowed": result.get("OriginalWriteAllowed"),
        "FileDeleteAllowed": result.get("FileDeleteAllowed"),
        "SafeToContinue": safe_to_continue,
        "Phase77Completed": True,
        "NextPhase": "Phase78 Goal Driven Daemon",
    }

    report_dir = Path("navikoLAB/event_trigger/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = (
        report_dir
        / f"event_driven_daemon_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Event Driven Daemon Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()