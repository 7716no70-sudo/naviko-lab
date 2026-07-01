# evolution_analyzer.py


class EvolutionAnalyzer:

    def analyze(self, history):

        if not history:
            return "initial_stage"

        failure_rate = history.count("WAIT_HUMAN") / len(history)

        if failure_rate > 0.5:
            return "conservative_mode"

        if failure_rate < 0.1:
            return "aggressive_evolution"

        return "balanced_growth"