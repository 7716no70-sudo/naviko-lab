class RepetitionDetector:

    def __init__(self):
        self.history = []

    def reset(self):
        self.history = []

    def check(self, data):
        """
        直近の繰り返しを検知するシンプル版
        """

        self.history.append(data)

        # 履歴が少ない場合は判定しない
        if len(self.history) < 2:
            return {
                "repetition": False,
                "reason": "insufficient_data"
            }

        # 直近2つ比較
        if self.history[-1] == self.history[-2]:
            return {
                "repetition": True,
                "reason": "same_as_previous"
            }

        # 安定状態
        return {
            "repetition": False,
            "reason": "stable"
        }