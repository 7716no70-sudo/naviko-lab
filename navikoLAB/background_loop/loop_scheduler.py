# loop_scheduler.py

import time


class LoopScheduler:

    def __init__(self):
        self.mode = "normal"

    def get_interval(self):
        if self.mode == "risk_high":
            return 300
        if self.mode == "idle":
            return 120
        return 60

    def sleep(self):
        time.sleep(self.get_interval())