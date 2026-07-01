class MemoryCore:

    def __init__(self):
        self.goal_memory = []
        self.execution_memory = []
        self.evolution_memory = []

    # ■ Goal保存
    def save_goal(self, goals):
        self.goal_memory.append(goals)

    # ■ 実行保存
    def save_execution(self, result):
        self.execution_memory.append(result)

    # ■ 進化保存
    def save_evolution(self, evo):
        self.evolution_memory.append(evo)

    # ■ 最新取得
    def latest(self):
        return {
            "goal": self.goal_memory[-1] if self.goal_memory else None,
            "execution": self.execution_memory[-1] if self.execution_memory else None,
            "evolution": self.evolution_memory[-1] if self.evolution_memory else None
        }