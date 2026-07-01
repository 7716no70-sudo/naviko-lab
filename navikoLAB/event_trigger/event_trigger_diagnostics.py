from navikoLAB.event_trigger.event_trigger_manager import EventTriggerManager


def main():
    manager = EventTriggerManager()
    result = manager.scan_events()

    safe_to_continue = (
        result.get("status") == "completed"
        and result.get("event_directory_exists") is True
    )

    print("=== Event Trigger Diagnostics ===")
    print("phase: Phase75-2 Event Trigger Diagnostics")
    print(f"status: {result.get('status')}")
    print(f"EventDirectoryExists: {result.get('event_directory_exists')}")
    print(f"EventCount: {result.get('event_count')}")
    print(f"SafeEventCount: {result.get('safe_event_count')}")
    print(f"TriggerAllowed: {result.get('trigger_allowed')}")
    print(f"SafeToContinue: {safe_to_continue}")
    print(f"LogPath: {result.get('log_path')}")


if __name__ == "__main__":
    main()