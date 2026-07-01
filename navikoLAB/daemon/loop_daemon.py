from navikoLAB.background_loop.background_loop_manager import BackgroundLoopManager
from navikoLAB.daemon.watchdog import Watchdog
from navikoLAB.daemon.auto_recovery import AutoRecovery
from navikoLAB.daemon.loop_guard import LoopGuard
from navikoLAB.daemon.health_monitor import HealthMonitor
from navikoLAB.daemon.state_seeder import StateSeeder


class LoopDaemon:

    def __init__(self):
        self.loop = BackgroundLoopManager()
        self.watchdog = Watchdog()
        self.recovery = AutoRecovery()
        self.guard = LoopGuard()
        self.health = HealthMonitor()
        self.seeder = StateSeeder()

        self.running = False

    def start(self):
        self.seeder.seed_if_missing()

        self.running = True
        print("[Daemon A2] Started")

        while self.running:

            snapshot = self.loop.scanner.scan()
            phase_report = self.loop.watcher.check(snapshot)
            decision = self.loop.engine.evaluate(snapshot, phase_report)

            # ■ ガード層（追加）
            guard_result = self.guard.check(snapshot)
            if guard_result == "BLOCK":
                print("[Daemon A2] BLOCKED by Guard")
                break

            # ■ ヘルスチェック
            health = self.health.analyze(snapshot)

            # ■ Watchdog判定
            wd = self.watchdog.tick(decision)

            if wd == "RECOVER":
                self.recovery.recover()
                continue

            if wd == "STOP":
                print("[Daemon A2] STOPPED by Watchdog")
                break

            self.loop.logger.log(snapshot, phase_report, decision)

            print("[Daemon A2 LOOP]", decision, health)

            self._sleep()

    def _sleep(self):
        import time
        time.sleep(self.loop.scheduler.get_interval())

    def loop_iteration(self):

        snapshot = self.loop.scanner.scan()
        phase_report = self.loop.watcher.check(snapshot)
        decision = self.loop.engine.evaluate(snapshot, phase_report)
 
        self.loop.logger.log(snapshot, phase_report, decision)
   
        print("[Daemon LOOP]", decision, snapshot.get("phase"))

        if decision == "BLOCK":
            print("[Daemon] STOP")
            self.stop()

    def cognition_step(self, cognition_result):

        missions = cognition_result.get("missions", [])
        goals = cognition_result.get("goals", [])

        print("[Cognition]", missions)
        print("[Goals]", goals)