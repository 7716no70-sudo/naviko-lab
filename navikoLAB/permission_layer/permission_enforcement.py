import json
from pathlib import Path
from datetime import datetime

from navikoLAB.permission_layer.autonomous_permission_layer import (
    AutonomousPermissionLayer,
)


class PermissionEnforcement:
    def __init__(self):
        self.log_dir = Path("navikoLAB/permission_layer/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def request(self, operation_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        permission = AutonomousPermissionLayer().evaluate(operation_name)

        allowed = permission.get("allowed") is True

        result = {
            "status": "completed",
            "phase": "Phase82-2 Permission Enforcement",
            "timestamp": timestamp,
            "operation_name": operation_name,
            "permission_checked": True,
            "allowed": allowed,
            "enforced": True,
            "executed": allowed,
            "blocked": not allowed,
            "permission_risk_count": permission.get("risk_count"),
            "guard_active": permission.get("operation_guard_active"),
            "human_approval_required": permission.get("human_approval_required"),
            "mode": "permission_enforced_dry_run",
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"permission_enforcement_{operation_name}_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    enforcement = PermissionEnforcement()

    tests = [
        "dry_run_cycle",
        "health_check",
        "external_operation",
        "original_write",
        "file_delete",
        "real_gui_operation",
        "browser_operation",
        "auto_execute",
    ]

    print("=== Permission Enforcement ===")

    for test in tests:
        report = enforcement.request(test)
        print("---")
        for k, v in report.items():
            print(f"{k}: {v}")