class DecisionStabilizer:

    def __init__(self, identity_core):

        self.identity = identity_core

        self.last_decision = None

    # ■ メイン判断
    def decide(self, goals, evolution_result, memory):

        identity = self.identity.get_identity()
        personality = identity["personality"]

        stability = personality["stability"]
        curiosity = personality["curiosity"]
        adaptability = personality["adaptability"]
        risk_aversion = personality["risk_aversion"]

        # ■ スコア計算
        evolution_score = 0
        goal_score = len(goals)

        if evolution_result.get("action") == "FORCE_EVOLUTION":
            evolution_score += 2

        if evolution_result.get("action") == "EVOLUTION":
            evolution_score += 1

        # ■ 人格影響
        decision_strength = (
            (curiosity * 2.0) +
            (adaptability * 1.5) -
            (risk_aversion * 1.2) +
            (evolution_score * 1.0)
        )

        # ■ 安定補正
        if stability > 0.7:
            decision_strength *= 0.8

        # ■ ゴール安定化
        stabilized_goals = self._stabilize_goals(goals, stability)

        # ■ 最終判断
        decision = {
            "goals": stabilized_goals,
            "strength": decision_strength,
            "action_mode": self._select_mode(decision_strength),
            "stability": stability
        }

        self.last_decision = decision

        return decision

    # ■ ゴール安定化
    def _stabilize_goals(self, goals, stability):

        if stability > 0.7:
            return goals[:3]  # 上位固定

        return goals

    # ■ モード選択
    def _select_mode(self, score):

        if score > 3.0:
            return "EXPAND"

        if score > 2.0:
            return "NORMAL"

        return "STABLE"