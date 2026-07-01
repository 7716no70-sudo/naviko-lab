# rule_analyzer.py


class RuleAnalyzer:

    def analyze(self, cognition_result, evolution_state):

        rules = []

        if evolution_state == "aggressive_evolution":
            rules.append("increase_autonomy")

        if "Stabilize" in str(cognition_result):
            rules.append("strengthen_stability")

        if "monitor" in str(cognition_result):
            rules.append("enhance_observation")

        return rules