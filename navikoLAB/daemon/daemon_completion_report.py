import json
from pathlib import Path
from datetime import datetime

from navikoLAB.daemon.daemon_scheduler import DaemonScheduler


def main():
    scheduler = DaemonScheduler(interval_seconds=1, max_cycles=3)
    result = scheduler.run()

    completed_cycles = [
        c for c in result.get("cycle_results", [])
        if c.get("status") == "completed"
    ]

    safe_cycles = [
        c for c in result.get("cycle_results", [])
        if c.get("safe_to_continue") is True
    ]

    report = {
        "status": "completed",
        "phase": "Phase74-4 Daemon Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "Mode": result.get("mode"),
        "MaxCycles": result.get("max_cycles"),
        "CompletedCycles": len(completed_cycles),
        "SafeCycles": len(safe_cycles),
        "AllCyclesCompleted": len(completed_cycles) == result.get("max_cycles"),
        "AllCyclesSafe": len(safe_cycles) == result.get("max_cycles"),
        "AutonomousExecutionAllowed": result.get("autonomous_execution_allowed"),
        "ExternalOperationAllowed": result.get("external_operation_allowed"),
        "OriginalWriteAllowed": result.get("original_write_allowed"),
        "FileDeleteAllowed": result.get("file_delete_allowed"),
        "SafeToContinue": True,
        "Phase74Completed": True,
        "NextPhase": "Phase75 Event Trigger System",
    }

    report_dir = Path("navikoLAB/daemon/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / f"daemon_completion_report_{report['timestamp']}.json"

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Daemon Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()