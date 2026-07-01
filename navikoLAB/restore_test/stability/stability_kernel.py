# ============================================================
# Phase65 Stability Kernel
# 完全安定カーネル
# ============================================================


class StabilityKernel:

    def __init__(self):
        self.expand_history = []
        self.max_expand_window = 10
        self.expand_limit = 3

    def check_expand_limit(self, decision_result, evolution_result):
        if decision_result.get("action_mode") != "EXPAND":
            return True

        self.expand_history.append(1)

        if len(self.expand_history) > self.max_expand_window:
            self.expand_history.pop(0)

        if sum(self.expand_history) > self.expand_limit:
            return False

        return True

    def compute_stability(self, memory, identity_state):
        memory_size = len(getattr(memory, "goal_memory", []))
        identity_score = identity_state.get("stability", 0.5)

        stability = 0.5

        if memory_size > 20:
            stability -= 0.2

        if identity_score < 0.4:
            stability -= 0.3

        return max(0.0, min(1.0, stability))

    def stabilize(self, decision_result, stability_score):
        if stability_score < 0.3:
            decision_result["action_mode"] = "NORMAL"
            decision_result["reason"] = "forced_stability_mode"

        return decision_result

    def run(self, decision_result, memory, identity_state, evolution_result):
        expand_allowed = self.check_expand_limit(
            decision_result,
            evolution_result
        )

        if not expand_allowed:
            decision_result["action_mode"] = "NORMAL"
            decision_result["reason"] = "expand_limit_exceeded"

        stability_score = self.compute_stability(
            memory,
            identity_state
        )

        decision_result = self.stabilize(
            decision_result,
            stability_score
        )

        return {
            "decision": decision_result,
            "stability": stability_score,
            "expand_allowed": decision_result.get("action_mode") == "EXPAND"
        }