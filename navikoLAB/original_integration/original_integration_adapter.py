from .adapter_request import AdapterRequest
from .adapter_response import AdapterResponse


class OriginalIntegrationAdapter:

    def __init__(self):

        self.dry_run = True

        self.external_operation = False

        self.real_gui_operation = False

        self.original_write = False

    def execute(self, request: AdapterRequest):

        payload = {

            "mission": request.mission,

            "planner_result": request.planner_result,

            "capability_result": request.capability_result,

            "connector_result": request.connector_result,

            "metadata": request.metadata

        }

        return AdapterResponse(

            status="dry_run",

            routed=True,

            dry_run=True,

            app_operator_called=False,

            payload=payload

        )