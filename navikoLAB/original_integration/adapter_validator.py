from .adapter_request import AdapterRequest


class AdapterValidator:

    def validate(self, request: AdapterRequest):

        errors = []

        if not request.mission:
            errors.append("mission is empty")

        if not isinstance(request.planner_result, dict):
            errors.append("planner_result invalid")

        if not isinstance(request.capability_result, dict):
            errors.append("capability_result invalid")

        if not isinstance(request.connector_result, dict):
            errors.append("connector_result invalid")

        return {

            "valid": len(errors) == 0,

            "errors": errors

        }