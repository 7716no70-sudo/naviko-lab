from .connector_router import ConnectorRouter


class KnowledgeRouter:

    def __init__(self):

        self.connector_router = ConnectorRouter()

    def execute(self, mission):

        connector_result = self.connector_router.execute(mission)

        if connector_result["status"] != "dry_run":
            return connector_result

        knowledge_payload = {

            "knowledge_update": False,

            "knowledge_saved": False,

            "dry_run": True

        }

        return {

            "status": "dry_run",

            "mission_routed": True,

            "connector_routed": True,

            "knowledge_routed": True,

            "knowledge": knowledge_payload

        }