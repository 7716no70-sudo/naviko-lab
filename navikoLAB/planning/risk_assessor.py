class RiskAssessor:

    def assess(self, analysis):

        scored = []

        for item, level in analysis:

            risk = 1

            if level == "HIGH_IMPACT":
                risk = 3

            if level == "MEDIUM_IMPACT":
                risk = 2

            scored.append((item, risk))

        return scored