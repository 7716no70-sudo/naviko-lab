# self_modify_core.py

from navikoLAB.self_modify.rule_analyzer import RuleAnalyzer
from navikoLAB.self_modify.behavior_modifier import BehaviorModifier
from navikoLAB.self_modify.safety_gate import SafetyGate
from navikoLAB.self_modify.mutation_engine import MutationEngine


class SelfModifyCore:

    def __init__(self):

        self.analyzer = RuleAnalyzer()
        self.modifier = BehaviorModifier()
        self.safety = SafetyGate()
        self.mutation = MutationEngine()

        self.current_behavior = {
            "loop_speed": 1,
            "risk_threshold": 2
        }

    def run(self, cognition_result, evolution_state):

        rules = self.analyzer.analyze(cognition_result, evolution_state)

        behavior = self.modifier.modify(rules)

        mutated = self.mutation.mutate(behavior)

        if self.safety.validate(mutated):
            self.current_behavior = mutated

        return self.current_behavior