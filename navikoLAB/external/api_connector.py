class APIConnector:

    def call(self, endpoint: str):

        return {
            "endpoint": endpoint,
            "status": "mock_success",
            "data": {"message": "External API simulated response"}
        }