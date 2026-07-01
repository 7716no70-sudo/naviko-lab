class GoalStabilizer:

    def __init__(self):
        self.dream_goal = "self_evolving_ai_system"

        self.long_goals = [
            "improve_learning_efficiency",
            "optimize_execution_loop",
            "enhance_self_model"
        ]

        self.active_goals = []

    # ■ 安定化処理
    def stabilize(self, memory):

        latest = memory.latest()

        # ■ 長期ゴールをベースに生成
        self.active_goals = self.long_goals.copy()

        # ■ メモリから補正
        if latest["evolution"] and latest["evolution"].get("action") == "FORCE_EVOLUTION":
            self.active_goals.append("stability_recovery")

        return {
            "dream": self.dream_goal,
            "long": self.long_goals,
            "active": self.active_goals
        }