import json
from pathlib import Path
from datetime import datetime

from navikoLAB.operation_guard.autonomous_operation_guard import AutonomousOperationGuard


def main():
    result = AutonomousOperationGuard().check()
    rules = result.get("guard_rules", {})

    required_blocked = [
        "external_operation_allowed",
        "original_write_allowed",
        "file_delete_allowed",
        "real_gui_operation_allowed",
        "browser_operation_allowed",
        "auto_execute_allowed",
    ]

    all_required_blocked = all(
        rules.get(key) is False
        for key in required_blocked
    )

    report = {
        "status": "completed",
        "phase": "Phase81-3 Autonomous Operation Guard Completion Report",
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "OperationGuardActive": result.get("operation_guard_active"),
        "BlockedOperationCount": result.get("blocked_operation_count"),
        "BlockedOperations": result.get("blocked_operations"),
        "AllRequiredBlocked": all_required_blocked,
        "HumanApprovalRequired": rules.get("human_approval_required"),
        "RiskCount": result.get("risk_count"),
        "Mode": result.get("mode"),
        "SafeToContinue": (
            result.get("status") == "completed"
            and result.get("operation_guard_active") is True
            and all_required_blocked
            and rules.get("human_approval_required") is True
            and result.get("risk_count") == 0
        ),
        "Phase81Completed": True,
        "NextPhase": "Phase82 Autonomous Permission Layer",
    }

    report_dir = Path("navikoLAB/operation_guard/reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / (
        f"autonomous_operation_guard_completion_report_{report['timestamp']}.json"
    )

    with report_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("=== Autonomous Operation Guard Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")

    print(f"ReportPath: {report_path}")


if __name__ == "__main__":
    main()