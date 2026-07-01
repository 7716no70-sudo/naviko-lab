from navikoLAB.connectors.real_app_operator_connector import RealAppOperatorConnector


def main():
    print("=== Real App Operator Diagnostics ===")

    connector = RealAppOperatorConnector(dry_run=True)
    result = connector.run({
        "purpose": "Phase2 Real App Operator dry_run diagnostics",
        "action": "inspect_windows",
    })

    print("状態:", result["status"])
    print("Connector:", result["connector"])
    print("dry_run:", result["dry_run"])
    print("外部操作実行:", result["external_operation_executed"])
    print("OS:", result["os"])
    print("対応予定Action:")
    for action in result["supported_actions"]:
        print("-", action)


if __name__ == "__main__":
    main()