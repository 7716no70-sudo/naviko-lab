# ============================================================
# Phase70-1 RecoveryPolicy
# Safe Restore Gate 用 復旧許可ポリシー
# ============================================================


class RecoveryPolicy:

    def __init__(self):
        self.min_health_score = 0.3
        self.max_stability_score = 0.25
        self.required_warnings = [
            "low_stability"
        ]

    def evaluate(self, health_result, stability_result, snapshot_result=None):
        system_health = health_result.get("system_health", "unknown")
        health_score = health_result.get("health_score", 0.5)
        warnings = health_result.get("warnings", [])

        stability_score = 0.5
        if stability_result:
            stability_score = stability_result.get("stability", 0.5)

        reasons = []

        if system_health == "critical":
            reasons.append("critical_health")

        if health_score < self.min_health_score:
            reasons.append("low_health_score")

        if stability_score < self.max_stability_score:
            reasons.append("low_stability_score")

        for warning in self.required_warnings:
            if warning in warnings:
                reasons.append(f"warning:{warning}")

        snapshot_ok = True

        if snapshot_result is not None:
            snapshot_ok = snapshot_result.get("status") == "found"

            if not snapshot_ok:
                reasons.append("snapshot_not_found")

        allowed = (
            "critical_health" in reasons
            and "low_health_score" in reasons
            and (
                "low_stability_score" in reasons
                or "warning:low_stability" in reasons
            )
            and snapshot_ok
        )

        return {
            "status": "allowed" if allowed else "blocked",
            "allowed": allowed,
            "reasons": reasons,
            "system_health": system_health,
            "health_score": health_score,
            "stability_score": stability_score,
            "snapshot_ok": snapshot_ok
        }