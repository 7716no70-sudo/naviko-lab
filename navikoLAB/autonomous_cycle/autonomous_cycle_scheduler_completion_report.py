import json
from pathlib import Path
from datetime import datetime

from navikoLAB.autonomous_cycle.autonomous_cycle_scheduler import AutonomousCycleScheduler


def main():
    result = AutonomousCycleScheduler(interval_seconds=1, max_cycles=3).run()

    safe_cycles = [
        c for c in result.get("cycle_results", [])
        if c.get("safe_to_continue") is True
    ]

    report = {
        "status": "completed",
        "phase": "Phase80-3 Autonomous Cycle Scheduler Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "Mode": result.get("mode"),
        "MaxCycles": result.get("max_cycles"),
        "CompletedCycleCount": result.get("completed_cycle_count"),
        "SafeCycleCount": len(safe_cycles),
        "AllCyclesSafe": len(safe_cycles) == result.get("max_cycles"),
        "ExternalOperationAllowed": result.get("ExternalOperationAllowed"),
        "OriginalWriteAllowed": result.get("OriginalWriteAllowed"),
        "FileDeleteAllowed": result.get("FileDeleteAllowed"),
        "SafeToContinue": result.get("SafeToContinue"),
        "Phase80Completed": True,
        "NextPhase": "Phase81 Autonomous Operation Guard",
    }

    report_dir = Path("navikoLAB/autonomous_cycle/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / (
        f"autonomous_cycle_scheduler_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Autonomous Cycle Scheduler Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()