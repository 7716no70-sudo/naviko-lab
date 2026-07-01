from .original_bridge_interface import OriginalBridgeInterface


class OriginalBridgeFacade:

    def __init__(self):

        self.bridge = OriginalBridgeInterface()

    def call_mission(self, mission: str):

        return self.bridge.execute(mission)