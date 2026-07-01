# navikoLAB/runtime/ai_os_self_running_daemon.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import time


PHASE = "Phase105-1 AI OS Self-Running Daemon"

ROOT = Path(__file__).resolve().parents[2]

DAEMON_DIR = ROOT / "runtime" / "daemon"
DAEMON_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = DAEMON_DIR / "self_running_daemon_state.json"


# -----------------------------
# SIMPLE AUTONOMOUS LOOP CORE
# -----------------------------

class SelfRunningDaemon:

    def __init__(self, max_cycles: int = 5):

        self.max_cycles = max_cycles
        self.cycle = 0
        self.running = True

        self.state = {
            "phase": PHASE,
            "mode": "dry_run",
            "running": True,
            "risk": 0,
            "safe": True,
        }

        self.log = []

    def tick(self):

        event = {
            "cycle": self.cycle,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "action": "autonomous_tick",
            "status": "dry_run_ok",
        }

        self.log.append(event)

        print(f"[DAEMON CYCLE {self.cycle}] {event['action']} -> {event['status']}")

    def run(self):

        while self.running:

            self.tick()

            self.cycle += 1

            time.sleep(0.2)

            # safe stop condition (prevent infinite runaway)
            if self.cycle >= self.max_cycles:
                self.running = False

        self.state["running"] = False

    def save(self):

        data = {
            "phase": PHASE,
            "mode": "dry_run",
            "cycles": self.cycle,
            "log": self.log,
            "state": self.state,
        }

        STATE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    daemon = SelfRunningDaemon(max_cycles=5)

    daemon.run()
    daemon.save()

    print("=== AI OS Self-Running Daemon ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("cycles:", daemon.cycle)
    print("safe:", True)
    print("risk:", 0)
    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()