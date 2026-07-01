from .reflection_router import ReflectionRouter


class ExperienceRouter:

    def __init__(self):

        self.reflection_router = ReflectionRouter()

    def execute(self, mission):

        reflection_result = self.reflection_router.execute(mission)

        if reflection_result["status"] != "dry_run":
            return reflection_result

        experience_payload = {

            "experience_created": False,

            "experience_saved": False,

            "dry_run": True

        }

        return {

            "status": "dry_run",

            "mission_routed": True,

            "connector_routed": True,

            "knowledge_routed": True,

            "reflection_routed": True,

            "experience_routed": True,

            "experience": experience_payload

        }