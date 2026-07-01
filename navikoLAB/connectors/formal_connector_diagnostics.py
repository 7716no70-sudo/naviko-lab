from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


FORMAL_CONNECTORS = [
    "chatgpt",
    "claude",
    "gemini",
    "grok",
]


def run_formal_connector_diagnostics():
    dispatcher = ConnectorDispatcher()

    results = []

    for connector_id in FORMAL_CONNECTORS:
        result = dispatcher.run(
            connector_id,
            f"{connector_id} 正式Connector Dispatcher診断テスト",
            context={
                "source": "formal_connector_diagnostics",
                "safe_test": True,
            },
        )

        results.append(result)

    return results


def main():
    print("=== 正式Connector まとめ診断 ===")

    results = run_formal_connector_diagnostics()

    completed = 0
    skipped = 0
    failed = 0

    for result in results:
        connector = result.get("connector", result.get("agent_id"))
        status = result.get("status")
        reason = result.get("reason")
        log_path = result.get("dispatcher_log")

        if status == "completed":
            completed += 1
        elif status == "skipped":
            skipped += 1
        else:
            failed += 1

        print("---------------")
        print(f"connector: {connector}")
        print(f"status: {status}")

        if reason:
            print(f"reason: {reason}")

        if result.get("error"):
            print(f"error: {result.get('error')}")

        print(f"dispatcher_log: {log_path}")

    print("===============")
    print(f"診断数: {len(results)}")
    print(f"completed: {completed}")
    print(f"skipped: {skipped}")
    print(f"failed_or_warning: {failed}")

    if failed == 0:
        print("診断結果: passed")
    else:
        print("診断結果: warning")


if __name__ == "__main__":
    main()