class AdaptiveTriggerEngine:

    def __init__(self):
        self.counter = 0

    def update(self, evaluation_result):

        self.counter += 1

        score = evaluation_result.get("score", 1.0)

        # 停滞 or 低スコアなら強制進化
        if score < 0.5 or self.counter > 5:
            self.counter = 0
            return "FORCE_EVOLUTION"

        return "NORMAL"