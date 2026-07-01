try:
    from .base_ai_connector import BaseAIConnector
except ImportError:
    from base_ai_connector import BaseAIConnector


class DummyAIConnector(BaseAIConnector):
    connector_name = "dummy_ai"
    default_model = "dummy-model"
    provider_key = "DUMMY_API_KEY"


def main():
    connector = DummyAIConnector()

    print("=== BaseAIConnector Test ===")
    print("connector:", connector.connector_name)
    print("model:", connector.model)
    print("available:", connector.is_available())

    skipped = connector.skipped_result()
    completed = connector.completed_result("dummy output")
    failed = connector.failed_result(Exception("dummy error"))

    connector.write_log("dummy prompt", skipped)

    print("skipped:", skipped["status"])
    print("completed:", completed["status"])
    print("failed:", failed["status"])
    print("=== BaseAIConnector Test Completed ===")


if __name__ == "__main__":
    main()