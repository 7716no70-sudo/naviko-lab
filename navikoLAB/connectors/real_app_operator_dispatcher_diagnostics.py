from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


def main():
    print("=== Real App Operator Dispatcher Diagnostics ===")

    dispatcher = ConnectorDispatcher()

    result = dispatcher.run(
        agent_id="real_app_operator",
        goal="Dispatcher経由 Real App Operator dry_run",
        context={
            "action": "inspect_windows",
            "phase": "Post-v2.0 Phase2",
        },
    )

    print("状態:", result.get("status"))
    print("Connector:", result.get("connector"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("Message:", result.get("message"))
    print("Dispatcher:", result.get("dispatcher"))
    print("Log:", result.get("dispatcher_log"))


if __name__ == "__main__":
    main()