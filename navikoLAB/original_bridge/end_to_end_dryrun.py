from .original_call_adapter import call_mission


class EndToEndDryRun:

    def execute(self, mission: str):

        result = call_mission(mission)

        return {

            "status": result["status"],

            "end_to_end_completed": True,

            "pipeline_completed": result["pipeline_completed"],

            "external_operation": result["external_operation"],

            "real_gui_operation": result["real_gui_operation"],

            "original_write": result["original_write"]

        }