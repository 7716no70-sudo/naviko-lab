class EvaluationEngine:

    def evaluate(self, history, goals):

        if not history:
            return {
                "score": 1.0,
                "status": "stable"
            }

        last = history[-1]

        # シンプル評価（まずは動作確認用）
        return {
            "score": 0.8,
            "status": "stable",
            "last": last,
            "goal_count": len(goals)
        }