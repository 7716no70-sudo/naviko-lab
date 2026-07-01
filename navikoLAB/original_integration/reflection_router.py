from .knowledge_router import KnowledgeRouter


class ReflectionRouter:

    def __init__(self):

        self.knowledge_router = KnowledgeRouter()

    def execute(self, mission):

        knowledge_result = self.knowledge_router.execute(mission)

        if knowledge_result["status"] != "dry_run":
            return knowledge_result

        reflection_payload = {

            "reflection_created": False,

            "reflection_saved": False,

            "dry_run": True

        }

        return {

            "status": "dry_run",

            "mission_routed": True,

            "connector_routed": True,

            "knowledge_routed": True,

            "reflection_routed": True,

            "reflection": reflection_payload

        }