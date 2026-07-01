# abstraction_engine.py


class AbstractionEngine:

    def abstract(self, missions):

        abstracted = []

        for m in missions:

            if "stabilize" in m.lower():
                abstracted.append("system_stability")

            elif "monitor" in m.lower():
                abstracted.append("system_observation")

            elif "evolution" in m.lower():
                abstracted.append("system_evolution")

            else:
                abstracted.append("general_improvement")

        return list(set(abstracted))