import json
from pathlib import Path
from datetime import datetime

from navikoLAB.autonomous_cycle.autonomous_cycle_manager import AutonomousCycleManager
from navikoLAB.autonomous_cycle.autonomous_cycle_integration import AutonomousCycleIntegration


def main():
    manager_result = AutonomousCycleManager().run_cycle()
    integration_result = AutonomousCycleIntegration().run_integrated_cycle()

    safe_to_continue = (
        manager_result.get("status") == "completed"
        and integration_result.get("status") == "completed"
        and manager_result.get("SafeToContinue") is True
        and integration_result.get("SafeToContinue") is True
    )

    report = {
        "status": "completed",
        "phase": "Phase79-4 Autonomous Cycle Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "AutonomousCycleCompleted": manager_result.get("AutonomousCycleCompleted"),
        "IntegratedCycleCompleted": integration_result.get("IntegratedCycleCompleted"),
        "HealthMonitorChecked": integration_result.get("HealthMonitorChecked"),
        "StabilityKernelChecked": integration_result.get("StabilityKernelChecked"),
        "BackupManagerChecked": integration_result.get("BackupManagerChecked"),
        "RecoveryPolicyChecked": integration_result.get("RecoveryPolicyChecked"),
        "GoalDaemonChecked": integration_result.get("GoalDaemonChecked"),
        "EventDaemonChecked": integration_result.get("EventDaemonChecked"),
        "AutonomousDaemonChecked": integration_result.get("AutonomousDaemonChecked"),
        "AuditChecked": integration_result.get("AuditChecked"),
        "RiskCount": integration_result.get("RiskCount"),
        "Mode": "dry_run",
        "SafeToContinue": safe_to_continue,
        "Phase79Completed": True,
        "NextPhase": "Phase80 Autonomous Cycle Scheduler",
    }

    report_dir = Path("navikoLAB/autonomous_cycle/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / (
        f"autonomous_cycle_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Autonomous Cycle Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()