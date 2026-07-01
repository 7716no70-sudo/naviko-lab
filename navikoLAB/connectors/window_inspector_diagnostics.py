from navikoLAB.connectors.window_inspector import WindowInspector


def main():
    print("=== WindowInspector Diagnostics ===")

    inspector = WindowInspector(dry_run=True)
    result = inspector.inspect()

    print("状態:", result.get("status"))
    print("Component:", result.get("component"))
    print("dry_run:", result.get("dry_run"))
    print("外部操作実行:", result.get("external_operation_executed"))
    print("OS:", result.get("os"))
    print("対応予定Check:")
    for check in result.get("supported_checks", []):
        print("-", check)


if __name__ == "__main__":
    main()