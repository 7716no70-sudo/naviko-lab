# mission_generator.py


class MissionGenerator:

    def generate(self, top_intents):

        missions = []

        for intent, score in top_intents:

            if intent == "safety_reinforcement":
                missions.append("Improve system safety layers")

            if intent == "evolution_preparation":
                missions.append("Prepare next phase evolution structure")

            if intent == "stability_improvement":
                missions.append("Stabilize runtime loop behavior")

            if intent == "monitor_enhancement":
                missions.append("Enhance monitoring visibility")

        return missions