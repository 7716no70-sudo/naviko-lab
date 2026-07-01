from __future__ import annotations


class DecisionEngine:
    def decide(self, goal: str, context: str) -> str:
        # Phase148ベース簡易意思決定
        if "危険" in context:
            return "avoid"
        if "重要" in context:
            return "prioritize"
        return "proceed"


class Planner:
    def plan(self, goal: str) -> list:
        return [
            f"goal分析: {goal}",
            "必要情報収集",
            "行動手順生成",
            "実行準備"
        ]


class AutonomousCore:
    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.planner = Planner()
        self.state = "Phase222_autonomous_restored"

    def execute(self, goal: str, context: str) -> dict:
        decision = self.decision_engine.decide(goal, context)
        plan = self.planner.plan(goal)

        return {
            "goal": goal,
            "context": context,
            "decision": decision,
            "plan": plan,
            "state": self.state
        }


def run_demo():
    core = AutonomousCore()

    result1 = core.execute("タスク整理", "重要な作業")
    result2 = core.execute("安全確認", "危険な可能性あり")

    return {
        "status": "autonomy_restored",
        "sample1": result1,
        "sample2": result2
    }


def main():
    result = run_demo()

    print("=== Phase222 Autonomous Intelligence Restoration ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()