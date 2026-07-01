# background_loop_manager.py

from navikoLAB.background_loop.state_scanner import StateScanner
from navikoLAB.background_loop.phase_watcher import PhaseWatcher
from navikoLAB.background_loop.safe_trigger_engine import SafeTriggerEngine
from navikoLAB.background_loop.experience_logger import ExperienceLogger
from navikoLAB.background_loop.loop_scheduler import LoopScheduler


class BackgroundLoopManager:

    def __init__(self):
        self.scanner = StateScanner()
        self.watcher = PhaseWatcher()
        self.engine = SafeTriggerEngine()
        self.logger = ExperienceLogger()
        self.scheduler = LoopScheduler()

        self.running = False

    def start(self):
        self.running = True
        print("Background Loop Started")

        while self.running:

            snapshot = self.scanner.scan()
            phase_report = self.watcher.check(snapshot)
            decision = self.engine.evaluate(snapshot, phase_report)

            self.logger.log(snapshot, phase_report, decision)

            print("[Loop]", decision, snapshot.get("phase"))

            if decision == "BLOCK":
                print("STOPPED: unsafe condition detected")
                break

            self.scheduler.sleep()

    def stop(self):
        self.running = False