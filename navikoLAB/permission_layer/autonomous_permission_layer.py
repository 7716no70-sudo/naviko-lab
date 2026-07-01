import json
from pathlib import Path
from datetime import datetime

from navikoLAB.operation_guard.autonomous_operation_guard import AutonomousOperationGuard


class AutonomousPermissionLayer:
    def __init__(self):
        self.log_dir = Path("navikoLAB/permission_layer/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(self, requested_operation="dry_run_cycle"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        guard_result = AutonomousOperationGuard().check()
        rules = guard_result.get("guard_rules", {})

        permission_map = {
            "dry_run_cycle": True,
            "health_check": True,
            "stability_check": True,
            "backup_check": True,
            "recovery_check": True,
            "goal_check": True,
            "event_check": True,

            "external_operation": rules.get("external_operation_allowed") is True,
            "original_write": rules.get("original_write_allowed") is True,
            "file_delete": rules.get("file_delete_allowed") is True,
            "real_gui_operation": rules.get("real_gui_operation_allowed") is True,
            "browser_operation": rules.get("browser_operation_allowed") is True,
            "auto_execute": rules.get("auto_execute_allowed") is True,
        }

        allowed = permission_map.get(requested_operation, False)

        result = {
            "status": "completed",
            "phase": "Phase82-1 Autonomous Permission Layer",
            "timestamp": timestamp,
            "requested_operation": requested_operation,
            "allowed": allowed,
            "guard_status": guard_result.get("status"),
            "operation_guard_active": guard_result.get("operation_guard_active"),
            "human_approval_required": rules.get("human_approval_required"),
            "mode": "dry_run_permission",
            "permission_map": permission_map,
            "risk_count": 0 if allowed else 1,
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"autonomous_permission_layer_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    layer = AutonomousPermissionLayer()
    report = layer.evaluate("dry_run_cycle")

    print("=== Autonomous Permission Layer ===")
    for k, v in report.items():
        print(f"{k}: {v}")