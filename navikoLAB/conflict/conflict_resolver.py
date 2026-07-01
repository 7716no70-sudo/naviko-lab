class ConflictResolver:

    def __init__(self):

        self.conflict_history = []

    # ■ メイン処理
    def resolve(self, goals, identity, evolution, decision, memory):

        conflicts = self._detect_conflicts(
            goals,
            identity,
            evolution,
            decision,
            memory
        )

        if not conflicts:
            return {
                "status": "stable",
                "conflicts": []
            }

        resolved_goals = goals
        resolved_mode = "NORMAL"

        for conflict in conflicts:

            if conflict["type"] == "GOAL_IDENTITY_CONFLICT":
                resolved_goals = self._fix_goal_identity(goals, identity)

            if conflict["type"] == "EVOLUTION_STABILITY_CONFLICT":
                resolved_mode = "STABLE"

            if conflict["type"] == "DECISION_MEMORY_CONFLICT":
                resolved_mode = "RECALIBRATE"

        result = {
            "status": "resolved",
            "conflicts": conflicts,
            "goals": resolved_goals,
            "mode": resolved_mode
        }

        self.conflict_history.append(result)

        return result

    # ■ 矛盾検知
    def _detect_conflicts(self, goals, identity, evolution, decision, memory):

        conflicts = []

        # ■ Goal vs Identity
        if identity["personality"]["risk_aversion"] > 0.7 and len(goals) > 4:
            conflicts.append({
                "type": "GOAL_IDENTITY_CONFLICT",
                "severity": "medium"
            })

        # ■ Evolution vs Stability
        if evolution.get("action") == "FORCE_EVOLUTION" and identity["personality"]["stability"] > 0.8:
            conflicts.append({
                "type": "EVOLUTION_STABILITY_CONFLICT",
                "severity": "high"
            })

        # ■ Decision vs Memory
        if memory.latest().get("execution") == "skipped" and decision.get("action_mode") == "EXPAND":
            conflicts.append({
                "type": "DECISION_MEMORY_CONFLICT",
                "severity": "low"
            })

        return conflicts

    # ■ 修正① Goal調整
    def _fix_goal_identity(self, goals, identity):

        if identity["personality"]["risk_aversion"] > 0.7:
            return goals[:3]  # 制限

        return goals