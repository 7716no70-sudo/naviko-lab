from navikoLAB.daemon.loop_daemon import LoopDaemon
from navikoLAB.autonomy.autonomy_core import AutonomyCore
import time


class NavikoServiceRunner:

    def __init__(self):

        self.daemon = LoopDaemon()
        self.autonomy = AutonomyCore(self.daemon)

        self.history = []

    def start(self):

        print("[Service] TRUE AUTONOMOUS AI OS STARTED")

        while True:

            result = self.autonomy.step(self.daemon)

            self._print_state(result)

            self.history.append(result["evolution"].get("action", "NORMAL"))

            self.daemon.loop_iteration()

            time.sleep(1)

    def _print_state(self, result):

        print("\n[GOALS]", result["goals"])
        print("[PLANNING]", result["planning"]["next_phases"])
        print("[EVOLUTION]", result["evolution"].get("action"))
        print("[BEHAVIOR]", result["behavior"])