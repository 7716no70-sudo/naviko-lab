import json
from pathlib import Path
from datetime import datetime


class AutonomousOperationGuard:
    def __init__(self):
        self.log_dir = Path("navikoLAB/operation_guard/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def check(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        guard_rules = {
            "external_operation_allowed": False,
            "original_write_allowed": False,
            "file_delete_allowed": False,
            "real_gui_operation_allowed": False,
            "browser_operation_allowed": False,
            "auto_execute_allowed": False,
            "human_approval_required": True,
        }

        blocked_operations = [
            key for key, value in guard_rules.items()
            if key.endswith("_allowed") and value is False
        ]

        result = {
            "status": "completed",
            "phase": "Phase81-1 Autonomous Operation Guard",
            "timestamp": timestamp,
            "mode": "dry_run_guard",
            "guard_rules": guard_rules,
            "blocked_operation_count": len(blocked_operations),
            "blocked_operations": blocked_operations,
            "risk_count": 0,
            "operation_guard_active": True,
            "safe_to_continue": True,
        }

        log_path = self.log_dir / f"autonomous_operation_guard_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    guard = AutonomousOperationGuard()
    report = guard.check()

    print("=== Autonomous Operation Guard ===")
    for k, v in report.items():
        print(f"{k}: {v}")