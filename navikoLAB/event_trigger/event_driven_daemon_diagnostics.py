from navikoLAB.event_trigger.event_driven_daemon_integration import EventDrivenDaemonIntegration


def main():
    result = EventDrivenDaemonIntegration().run_once()

    safe_to_continue = (
        result.get("status") == "completed"
        and result.get("RouterStatus") == "completed"
        and result.get("MarkerStatus") == "completed"
        and result.get("ExternalOperationAllowed") is False
        and result.get("OriginalWriteAllowed") is False
        and result.get("FileDeleteAllowed") is False
        and result.get("SafeToContinue") is True
    )

    print("=== Event Driven Daemon Diagnostics ===")
    print("phase: Phase77-2 Event Driven Daemon Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"RouterStatus: {result.get('RouterStatus')}")
    print(f"SafeEventCount: {result.get('SafeEventCount')}")
    print(f"RoutedCount: {result.get('RoutedCount')}")
    print(f"ExecutedCount: {result.get('ExecutedCount')}")
    print(f"MarkerStatus: {result.get('MarkerStatus')}")
    print(f"MarkedCount: {result.get('MarkedCount')}")
    print(f"Mode: {result.get('Mode')}")
    print(f"ExternalOperationAllowed: {result.get('ExternalOperationAllowed')}")
    print(f"OriginalWriteAllowed: {result.get('OriginalWriteAllowed')}")
    print(f"FileDeleteAllowed: {result.get('FileDeleteAllowed')}")
    print(f"SafeToContinue: {safe_to_continue}")
    print(f"LogPath: {result.get('log_path')}")


if __name__ == "__main__":
    main()