from navikoLAB.original_integration.original_integration_pipeline import (
    OriginalIntegrationPipeline,
)


class OriginalBridgeInterface:

    def __init__(self):

        self.pipeline = OriginalIntegrationPipeline()

    def execute(self, mission: str):

        return self.pipeline.execute(mission)