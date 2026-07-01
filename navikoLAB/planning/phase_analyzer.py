class PhaseAnalyzer:

    def analyze(self, proposals):

        analysis = []

        for p in proposals:

            if "multi-agent" in p:
                analysis.append((p, "HIGH_IMPACT"))

            elif "memory" in p:
                analysis.append((p, "MEDIUM_IMPACT"))

            else:
                analysis.append((p, "LOW_IMPACT"))

        return analysis