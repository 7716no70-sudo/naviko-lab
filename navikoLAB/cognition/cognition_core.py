# cognition_core.py

from navikoLAB.cognition.intent_engine import IntentEngine
from navikoLAB.cognition.priority_scorer import PriorityScorer
from navikoLAB.cognition.mission_generator import MissionGenerator
from navikoLAB.cognition.evolution_analyzer import EvolutionAnalyzer
from navikoLAB.cognition.self_goal_manager import SelfGoalManager


class CognitionCore:

    def __init__(self):
        self.intent = IntentEngine()
        self.scorer = PriorityScorer()
        self.mission = MissionGenerator()
        self.analyzer = EvolutionAnalyzer()
        self.goal_manager = SelfGoalManager()

    def run(self, snapshot, history):

        intents = self.intent.generate_intents(snapshot)
        scored = self.scorer.score(intents, snapshot)
        missions = self.mission.generate(scored)
        evolution = self.analyzer.analyze(history)
        goals = self.goal_manager.update_goals(missions, evolution)

        return {
            "intents": intents,
            "missions": missions,
            "evolution_state": evolution,
            "goals": goals
        }