import json
import time
from pathlib import Path
from datetime import datetime

from navikoLAB.daemon.autonomous_daemon_loop import AutonomousDaemonLoop


class DaemonScheduler:
    def __init__(self, interval_seconds=5, max_cycles=3):
        self.interval_seconds = interval_seconds
        self.max_cycles = max_cycles
        self.log_dir = Path("navikoLAB/daemon/logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = {
            "status": "completed",
            "phase": "Phase74-2 Daemon Scheduler",
            "timestamp": timestamp,
            "mode": "dry_run",
            "interval_seconds": self.interval_seconds,
            "max_cycles": self.max_cycles,
            "cycle_results": [],
            "autonomous_execution_allowed": False,
            "external_operation_allowed": False,
            "original_write_allowed": False,
            "file_delete_allowed": False,
            "safe_to_continue": True,
        }

        daemon = AutonomousDaemonLoop()

        for cycle in range(1, self.max_cycles + 1):
            cycle_result = daemon.run_once()
            result["cycle_results"].append({
                "cycle": cycle,
                "status": cycle_result.get("status"),
                "safe_to_continue": cycle_result.get("safe_to_continue"),
                "log_path": cycle_result.get("log_path"),
            })

            if cycle < self.max_cycles:
                time.sleep(self.interval_seconds)

        log_path = self.log_dir / f"daemon_scheduler_{timestamp}.json"

        with log_path.open("w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        result["log_path"] = str(log_path)
        return result


if __name__ == "__main__":
    scheduler = DaemonScheduler(interval_seconds=1, max_cycles=3)
    report = scheduler.run()

    print("=== Daemon Scheduler ===")
    for k, v in report.items():
        print(f"{k}: {v}")