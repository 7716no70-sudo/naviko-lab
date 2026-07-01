# navikoLAB/runtime/persistent_background_runtime.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import time
import threading


PHASE = "Phase108-2 Persistent Background Runtime (Safe Daemon Mode)"

ROOT = Path(__file__).resolve().parents[2]

BG_DIR = ROOT / "runtime" / "background_runtime"
BG_DIR.mkdir(parents=True, exist_ok=True)

STATE_FILE = BG_DIR / "background_runtime_state.json"


# -----------------------------
# BACKGROUND RUNTIME CORE
# -----------------------------

class PersistentBackgroundRuntime:

    def __init__(self):

        self.running = True
        self.cycle = 0
        self.max_cycles = 8  # safety cap

        self.memory = []

        self.thread = threading.Thread(target=self.loop, daemon=True)

    # -----------------------------
    # SAFE THOUGHT PROCESS
    # -----------------------------

    def think(self):

        thoughts = [
            "monitor system health",
            "check scheduler state",
            "review tool gateway safety",
            "simulate improvement ideas",
            "evaluate memory growth",
        ]

        return thoughts[self.cycle % len(thoughts)]

    # -----------------------------
    # LOOP (BACKGROUND)
    # -----------------------------

    def loop(self):

        while self.running:

            thought = self.think()

            record = {
                "cycle": self.cycle,
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "thought": thought,
                "status": "background_thinking_dry_run",
            }

            self.memory.append(record)

            print(f"[BG LOOP {self.cycle}] {thought}")

            self.cycle += 1

            time.sleep(0.25)

            if self.cycle >= self.max_cycles:
                self.running = False

        self.save()

    # -----------------------------
    # START
    # -----------------------------

    def start(self):

        self.thread.start()

        # wait until finish
        while self.thread.is_alive():
            time.sleep(0.1)

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save(self):

        STATE_FILE.write_text(
            json.dumps({
                "phase": PHASE,
                "mode": "dry_run",
                "cycles": self.cycle,
                "memory": self.memory,
                "safe": True,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    runtime = PersistentBackgroundRuntime()

    print("=== Naviko Persistent Background Runtime ===")
    print("phase:", PHASE)
    print("mode: dry_run")

    runtime.start()

    print("saved:", STATE_FILE)


if __name__ == "__main__":
    main()