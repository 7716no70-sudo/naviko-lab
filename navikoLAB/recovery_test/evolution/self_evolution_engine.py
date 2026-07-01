class SelfEvolutionEngine:

    def __init__(self):
        self.state = "NORMAL"

    def evolve(self, semantic_result, trigger_result, repetition_result):

        # ■ None防御（最重要）
        repetition_result = repetition_result or {"repetition": False}

        # ■ 再帰的に進化判定
        if repetition_result.get("repetition"):
            return {
                "action": "FORCE_EVOLUTION",
                "reason": "repetition_detected"
            }

        if trigger_result == "FORCE_EVOLUTION":
            return {
                "action": "FORCE_EVOLUTION",
                "reason": "adaptive_trigger"
            }

        if semantic_result in ["stability_evolution", "optimization_evolution"]:
            return {
                "action": "EVOLUTION",
                "reason": semantic_result
            }

        return {
            "action": "NORMAL",
            "reason": "no_change"
        }