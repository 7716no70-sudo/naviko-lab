from navikoLAB.evolution.evolution_core import EvolutionCore


class EvolutionBridge:

    def __init__(self):
        self.evolution = EvolutionCore()

    def step(self, cognition_result, history):

        missions = cognition_result.get("missions", [])

        snapshot = cognition_result.get("snapshot", {})

        evolved = self.evolution.run(
            missions,
            history,
            snapshot
        )

        return evolved