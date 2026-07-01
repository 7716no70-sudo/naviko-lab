from navikoLAB.multi_agent.cognition_agent import CognitionAgent
from navikoLAB.multi_agent.evolution_agent import EvolutionAgent
from navikoLAB.multi_agent.selfmodify_agent import SelfModifyAgent


class Orchestrator:

    def __init__(self):

        self.cognition = CognitionAgent()
        self.evolution = EvolutionAgent()
        self.selfmodify = SelfModifyAgent()

    def run(self, snapshot):

        c = self.cognition.run(snapshot)
        e = self.evolution.run(c)
        s = self.selfmodify.run(e)

        return {
            "cognition": c,
            "evolution": e,
            "selfmodify": s
        }