# self_modify_bridge.py

from navikoLAB.self_modify.self_modify_core import SelfModifyCore


class SelfModifyBridge:

    def __init__(self):
        self.self_modify = SelfModifyCore()

    def step(self, cognition_result, evolution_state):

        behavior = self.self_modify.run(
            cognition_result,
            evolution_state
        )

        return behavior