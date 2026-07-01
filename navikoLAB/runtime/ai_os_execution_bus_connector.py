# navikoLAB/runtime/ai_os_execution_bus_connector.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase101-2 AI OS Execution Bus Connector"

ROOT = Path(__file__).resolve().parents[2]

BUS_DIR = ROOT / "runtime" / "bus"
BUS_DIR.mkdir(parents=True, exist_ok=True)

BUS_FILE = BUS_DIR / "execution_bus_state.json"


class ExecutionBus:

    def __init__(self):
        self.mode = "dry_run"
        self.queue = []
        self.executed = []

    def submit(self, task: dict):

        packet = {
            "task_id": task["id"],
            "payload": task["description"],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": "queued"
        }

        self.queue.append(packet)
        return packet

    def route(self):

        for item in self.queue:

            result = {
                "task_id": item["task_id"],
                "status": "routed_dry_run",
                "output": f"[DRY RUN BUS] {item['payload']}"
            }

            self.executed.append(result)
            item["status"] = "processed"

    def save(self):

        state = {
            "phase": PHASE,
            "mode": self.mode,
            "queue": self.queue,
            "executed": self.executed,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SafeToContinue": True,
            "RiskCount": 0,
        }

        BUS_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main():

    bus = ExecutionBus()

    # dry_run sample injection
    bus.submit({"id": "task_1", "description": "sample execution"})
    bus.route()
    bus.save()

    print("=== AI OS Execution Bus Connector ===")
    print("phase:", PHASE)
    print("mode:", bus.mode)
    print("queue:", len(bus.queue))
    print("executed:", len(bus.executed))
    print("risk:", 0)
    print("saved:", BUS_FILE)


if __name__ == "__main__":
    main()