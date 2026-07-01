# priority_scorer.py


class PriorityScorer:

    def score(self, intents, snapshot):

        scored = []

        for intent in intents:

            score = 0

            if intent == "safety_reinforcement":
                score += 10

            if intent == "evolution_preparation":
                score += 8

            if intent == "stability_improvement":
                score += 6

            if snapshot.get("risk_level", 0) > 0:
                score += 2

            scored.append((intent, score))

        return sorted(scored, key=lambda x: x[1], reverse=True)