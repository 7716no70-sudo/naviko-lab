from .original_integration_pipeline import OriginalIntegrationPipeline


class OriginalIntegrationValidator:

    def __init__(self):
        self.pipeline = OriginalIntegrationPipeline()

    def validate(self, mission):

        result = self.pipeline.execute(mission)

        checks = {

            "pipeline_completed": result.get("pipeline_completed", False),

            "dry_run": result.get("status") == "dry_run",

            "external_operation_disabled": (
                result.get("external_operation") is False
            ),

            "real_gui_operation_disabled": (
                result.get("real_gui_operation") is False
            ),

            "original_write_disabled": (
                result.get("original_write") is False
            ),

        }

        return {

            "status": "completed",

            "valid": all(checks.values()),

            "checks": checks

        }