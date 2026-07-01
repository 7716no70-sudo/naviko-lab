# self_goal_manager.py


class SelfGoalManager:

    def update_goals(self, missions, evolution_state):

        goals = []

        if evolution_state == "aggressive_evolution":
            goals.append("Increase autonomy level")

        if evolution_state == "balanced_growth":
            goals.append("Maintain stable improvement")

        if evolution_state == "conservative_mode":
            goals.append("Reduce system risk and stabilize")

        goals.extend(missions)

        return goals