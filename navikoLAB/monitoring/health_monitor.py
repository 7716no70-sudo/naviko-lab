# ============================================================
# Phase66-1 HealthMonitor
# 安定監視ログ / System Health Monitor
# ============================================================

class HealthMonitor:

    def __init__(self):
        self.health_log = []
        self.max_log_size = 100

    def evaluate(
        self,
        stability_result,
        memory,
        identity_state,
        decision_result,
        evolution_result,
        execution_result=None
    ):
        stability_score = stability_result.get("stability", 0.5)

        memory_size = len(getattr(memory, "goal_memory", []))
        identity_score = identity_state.get("stability", 0.5)
        action_mode = decision_result.get("action_mode", "NORMAL")
        evolution_action = evolution_result.get("action", "NORMAL")

        warnings = []

        if stability_score < 0.3:
            warnings.append("low_stability")

        if memory_size > 20:
            warnings.append("memory_growth_high")

        if identity_score < 0.4:
            warnings.append("identity_unstable")

        if action_mode == "EXPAND" and not stability_result.get("expand_allowed", False):
            warnings.append("expand_suppressed")

        if execution_result and execution_result.get("status") in ["error", "failed"]:
            warnings.append("execution_failed")

        health_score = 1.0

        health_score -= len(warnings) * 0.15

        if stability_score < 0.5:
            health_score -= 0.2

        if identity_score < 0.5:
            health_score -= 0.2

        health_score = max(0.0, min(1.0, health_score))

        if health_score >= 0.75:
            system_health = "stable"
        elif health_score >= 0.45:
            system_health = "caution"
        else:
            system_health = "critical"

        result = {
            "system_health": system_health,
            "health_score": round(health_score, 3),
            "stability_score": stability_score,
            "memory_size": memory_size,
            "identity_score": identity_score,
            "action_mode": action_mode,
            "evolution_action": evolution_action,
            "warnings": warnings
        }

        self.health_log.append(result)

        if len(self.health_log) > self.max_log_size:
            self.health_log.pop(0)

        return result

    def latest(self):
        if not self.health_log:
            return {
                "system_health": "unknown",
                "health_score": 0.5,
                "warnings": []
            }

        return self.health_log[-1]

    def summary(self):
        return {
            "log_count": len(self.health_log),
            "latest": self.latest()
        }