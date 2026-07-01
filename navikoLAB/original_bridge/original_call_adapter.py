from .facade import OriginalBridgeFacade


def call_mission(mission: str):

    facade = OriginalBridgeFacade()

    return facade.call_mission(mission)