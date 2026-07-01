# evolution_core.py

from navikoLAB.evolution.repetition_detector import RepetitionDetector
from navikoLAB.evolution.abstraction_engine import AbstractionEngine
from navikoLAB.evolution.evolution_memory import EvolutionMemory
from navikoLAB.evolution.evolution_controller import EvolutionController
from navikoLAB.evolution.adaptive_trigger_engine import AdaptiveTriggerEngine
from navikoLAB.evolution.semantic_analyzer import SemanticAnalyzer
from navikoLAB.evolution.forced_evolution_gate import ForcedEvolutionGate
from navikoLAB.evolution.evolution_balancer import EvolutionBalancer


class EvolutionCore:

    def __init__(self):
        self.detector = RepetitionDetector()
        self.abstraction = AbstractionEngine()
        self.memory = EvolutionMemory()
        self.controller = EvolutionController()
        self.trigger = AdaptiveTriggerEngine()
        self.semantic = SemanticAnalyzer()
        self.gate = ForcedEvolutionGate()
        self.balancer = EvolutionBalancer()

    def run(self, missions, history, snapshot):

        trigger_result = self.trigger.update({
            "snapshot": snapshot,
            "history": history
        })

        should = trigger_result

        action = self.gate.open(should)

        action = self.balancer.balance(action)

        evolution_type = self.semantic.analyze(missions)
    
        # ★追加：進化の多様性補正
        if action == "FORCE_EVOLUTION":

            import random

            evolution_type = random.choice([
                "stability_evolution",
                "expansion_evolution",
                "optimization_evolution",
                "learning_evolution"
            ])

        return {
            "action": action,
            "type": evolution_type
        }