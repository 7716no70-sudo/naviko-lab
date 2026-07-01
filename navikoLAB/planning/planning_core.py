from navikoLAB.planning.proposal_engine import ProposalEngine
from navikoLAB.planning.phase_analyzer import PhaseAnalyzer
from navikoLAB.planning.risk_assessor import RiskAssessor
from navikoLAB.planning.next_phase_generator import NextPhaseGenerator


class PlanningCore:

    def __init__(self):
        self.proposal = ProposalEngine()
        self.analyzer = PhaseAnalyzer()
        self.risk = RiskAssessor()
        self.generator = NextPhaseGenerator()

    def run(self, state):

        proposals = self.proposal.generate(state)
        analysis = self.analyzer.analyze(proposals)
        risk = self.risk.assess(analysis)
        next_phases = self.generator.generate(risk)

        return {
            "proposals": proposals,
            "analysis": analysis,
            "risk": risk,
            "next_phases": next_phases
        }