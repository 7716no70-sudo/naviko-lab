# watchdog.py

import time


class Watchdog:

    def __init__(self, max_cycles=1000, max_wait_human=5):
        self.max_cycles = max_cycles
        self.max_wait_human = max_wait_human
        self.cycle_count = 0
        self.wait_human_count = 0

    def tick(self, decision):
        self.cycle_count += 1

        if decision == "WAIT_HUMAN":
            self.wait_human_count += 1
        else:
            self.wait_human_count = 0

        # ■ 暴走判定①：長時間WAIT_HUMAN
        if self.wait_human_count > self.max_wait_human:
            print("[Watchdog] WAIT_HUMAN STUCK → RECOVERY TRIGGER")
            return "RECOVER"

        # ■ 暴走判定②：過負荷
        if self.cycle_count > self.max_cycles:
            print("[Watchdog] MAX CYCLE REACHED → STOP")
            return "STOP"

        return "OK"