# semantic_analyzer.py


class SemanticAnalyzer:

    def analyze(self, missions):

        keywords = " ".join(missions).lower()

        if "stability" in keywords:
            return "stability_evolution"

        if "optimize" in keywords:
            return "optimization_evolution"

        if "enhance" in keywords:
            return "expansion_evolution"

        return "general_evolution"