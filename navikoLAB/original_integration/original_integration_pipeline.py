from .experience_router import ExperienceRouter


class OriginalIntegrationPipeline:

    def __init__(self):

        self.experience_router = ExperienceRouter()

    def execute(self, mission):

        result = self.experience_router.execute(mission)

        if result["status"] != "dry_run":
            return result

        return {

            "status": "dry_run",

            "pipeline_completed": True,

            "mission_routed": result["mission_routed"],

            "connector_routed": result["connector_routed"],

            "knowledge_routed": result["knowledge_routed"],

            "reflection_routed": result["reflection_routed"],

            "experience_routed": result["experience_routed"],

            "external_operation": False,

            "real_gui_operation": False,

            "original_write": False

        }