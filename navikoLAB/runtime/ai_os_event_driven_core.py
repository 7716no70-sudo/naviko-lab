# navikoLAB/runtime/ai_os_event_driven_core.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import queue
import threading
import time


PHASE = "Phase105-2 AI OS Event Driven Persistent Core"

ROOT = Path(__file__).resolve().parents[2]

EVENT_DIR = ROOT / "runtime" / "event_core"
EVENT_DIR.mkdir(parents=True, exist_ok=True)

EVENT_LOG_FILE = EVENT_DIR / "event_log.json"


# -----------------------------
# Event Bus (in-memory)
# -----------------------------

class EventBus:

    def __init__(self):
        self.q = queue.Queue()
        self.running = True
        self.log = []

    def emit(self, event: dict):
        self.q.put(event)

    def save_log(self):

        EVENT_LOG_FILE.write_text(
            json.dumps(self.log, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# Event Driven OS Core
# -----------------------------

class EventDrivenOS:

    def __init__(self):

        self.bus = EventBus()

    def event_loop(self):

        while self.bus.running:

            try:
                event = self.bus.q.get(timeout=0.5)

            except Exception:
                continue

            result = self.handle_event(event)

            self.bus.log.append({
                "event": event,
                "result": result,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            })

            print(f"[EVENT] {event['type']} -> {result['status']}")

            if event.get("type") == "shutdown":
                self.bus.running = False

    def handle_event(self, event: dict):

        # -----------------------------
        # SAFE DRY RUN EXECUTION ONLY
        # -----------------------------

        if event["type"] == "goal":

            return {
                "status": "goal_processed",
                "output": f"[DRY RUN] processing goal: {event['data']}"
            }

        elif event["type"] == "task":

            return {
                "status": "task_processed",
                "output": f"[DRY RUN] executing task: {event['data']}"
            }

        else:

            return {
                "status": "unknown_event",
                "output": "[DRY RUN] ignored"
            }

    def start(self):

        thread = threading.Thread(target=self.event_loop, daemon=True)
        thread.start()

        # -----------------------------
        # simulate external events
        # -----------------------------

        self.bus.emit({"type": "goal", "data": "initialize system"})
        self.bus.emit({"type": "task", "data": "run diagnostics"})
        self.bus.emit({"type": "task", "data": "optimize loop"})
        self.bus.emit({"type": "shutdown", "data": "stop system"})

        while self.bus.running:
            time.sleep(0.2)

        self.bus.save_log()


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    os = EventDrivenOS()

    os.start()

    print("=== AI OS Event Driven Core ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("status: completed")
    print("safe: True")
    print("saved:", EVENT_LOG_FILE)


if __name__ == "__main__":
    main()