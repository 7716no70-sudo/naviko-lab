from .mission_router import MissionRouter


class ConnectorRouter:

    def __init__(self):

        self.mission_router = MissionRouter()

    def execute(self, mission):

        mission_result = self.mission_router.execute(mission)

        if mission_result["status"] != "dry_run":

            return mission_result

        connector_payload = {

            "connector_selected": False,

            "connector_name": None,

            "connector_called": False,

            "dry_run": True

        }

        return {

            "status": "dry_run",

            "mission_routed": True,

            "connector_routed": True,

            "connector": connector_payload

        }