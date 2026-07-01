import json
import time
from pathlib import Path
from datetime import datetime

from navikoLAB.autonomous_cycle.autonomous_cycle_manager import AutonomousCycleManager
from navikoLAB.autonomous_cycle.autonomous_cycle_integration import AutonomousCycleIntegration


class AutonomousCycleScheduler:
    def __init__(self, interval_seconds=1, max_cycles=3):
        self.interval_seconds = interval_seconds
        self.max_cycles = max_cycles
        self.log_dir = Path("navikoLAB/autonomous_cycle/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        cycle_results = []

        for cycle in range(1, self.max_cycles + 1):
            manager_result = AutonomousCycleManager().run_cycle()
            integration_result = AutonomousCycleIntegration().run_integrated_cycle()

            cycle_results.append({
                "cycle": cycle,
                "manager_status": manager_result.get("status"),
                "integration_status": integration_result.get("status"),
                "autonomous_cycle_completed": manager_result.get("AutonomousCycleCompleted"),
                "integrated_cycle_completed": integration_result.get("IntegratedCycleCompleted"),
                "risk_count": integration_result.get("RiskCount"),
                "safe_to_continue": (
                    manager_result.get("SafeToContinue") is True
                    and integration_result.get("SafeToContinue") is True
                ),
            })

            if cycle < self.max_cycles:
                time.sleep(self.interval_seconds)

        result = {
            "status": "completed",
            "phase": "Phase80-1 Autonomous Cycle Scheduler",
            "timestamp": timestamp,
            "mode": "dry_run",
            "interval_seconds": self.interval_seconds,
            "max_cycles": self.max_cycles,
            "cycle_results": cycle_results,
            "completed_cycle_count": len([
                c for c in cycle_results
                if c.get("safe_to_continue") is True
            ]),
            "ExternalOperationAllowed": False,
            "OriginalWriteAllowed": False,
            "FileDeleteAllowed": False,
            "SafeToContinue": all(
                c.get("safe_to_continue") is True
                for c in cycle_results
            ),
        }

        log_path = self.log_dir / f"autonomous_cycle_scheduler_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    scheduler = AutonomousCycleScheduler(interval_seconds=1, max_cycles=3)
    report = scheduler.run()

    print("=== Autonomous Cycle Scheduler ===")
    for k, v in report.items():
        print(f"{k}: {v}")