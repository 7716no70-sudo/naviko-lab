# navikoLAB/planner_engine.py


class PlannerEngine:
    """
    PlannerEngine v2.0

    役割:
    - ユーザーの目的を小さな工程に分解する
    - 成長改善案を実行可能な計画へ変換する
    - ExecutionEngine が扱いやすい plan dict を返す
    """

    def create_plan(self, goal_text):
        goal = (goal_text or "").strip()

        if not goal:
            return {
                "goal": "",
                "steps": [],
                "status": "empty",
                "mode": "safe_plan",
            }

        steps = [
            "目的を確認する",
            "現在の状態を確認する",
            "必要な作業を小さな工程に分解する",
            "安全に実行できる範囲を判断する",
            "結果を保存し、次の改善につなげる",
        ]

        return {
            "goal": goal,
            "steps": steps,
            "status": "planned",
            "mode": "safe_plan",
        }

    def create_growth_plan(self, suggestion):
        return self.create_plan(suggestion)