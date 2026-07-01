# adaptive_trigger_engine.py

import time


class AdaptiveTriggerEngine:

    def __init__(self):
        self.last_trigger_time = time.time()
        self.counter = 0

    def should_evolve(self, snapshot, history):

        self.counter += 1

        # ■ ① 時間強制進化（短周期化）
        if time.time() - self.last_trigger_time > 3:
            self.last_trigger_time = time.time()
            return True

        # ■ ② 連続安定でも進化（重要強化）
        if len(history) >= 2:
            if history[-1] == history[-2]:
                return True

        # ■ ③ 軽微変化でも進化
        if len(history) >= 3:
            diff = len(set(history[-3:]))
            if diff <= 2:
                return True

        # ■ ④ カウンタ強制進化（新規）
        if self.counter % 5 == 0:
            return True

        # ■ ⑤ Phase固定でも進化
        if snapshot.get("phase") == "Phase43_STABLE":
            return True

        return False