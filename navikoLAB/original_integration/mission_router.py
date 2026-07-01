from .adapter_request import AdapterRequest
from .adapter_validator import AdapterValidator
from .original_integration_adapter import OriginalIntegrationAdapter


class MissionRouter:

    def __init__(self):

        self.validator = AdapterValidator()

        self.adapter = OriginalIntegrationAdapter()

    def execute(self, mission: str):

        request = AdapterRequest(

            mission=mission

        )

        validation = self.validator.validate(request)

        if not validation["valid"]:

            return {

                "status": "validation_failed",

                "errors": validation["errors"]

            }

        response = self.adapter.execute(request)

        return {

            "status": response.status,

            "routed": response.routed,

            "app_operator_called": response.app_operator_called,

            "payload": response.payload

        }