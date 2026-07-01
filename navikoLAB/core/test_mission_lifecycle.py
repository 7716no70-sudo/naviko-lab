from pathlib import Path

from mission_manager import MissionManager


def main():

    root_dir = Path(__file__).resolve().parent.parent

    manager = MissionManager(root_dir)

    print("=== Mission状態遷移テスト ===")

    mission = manager.create_mission(
        "長期AIアプリ開発ミッション",
        "MissionManagerの状態遷移テスト"
    )

    print("作成:", mission["title"])
    print("初期状態:", mission["status"])

    states = [
        "planning",
        "waiting_agent",
        "building",
        "reflection",
        "improving",
        "completed"
    ]

    for state in states:

        result = manager.update_status(
            mission["id"],
            state
        )

        refreshed = manager.get_mission(
            mission["id"]
        )

        print(
            state,
            "=>",
            "OK" if result else "NG",
            "/ 現在:",
            refreshed["status"]
        )

    manager.complete_mission(
        mission["id"]
    )

    completed = manager.get_mission(
        mission["id"]
    )

    print("最終状態:", completed["status"])
    print("最終進捗:", str(completed["progress"]) + "%")

    diagnosis = manager.diagnose()

    print("=== 状態別診断 ===")
    print(diagnosis.get("status_count", {}))

    print("=== Mission状態遷移テスト完了 ===")


if __name__ == "__main__":
    main()