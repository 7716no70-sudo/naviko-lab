from pathlib import Path

from mission_bridge import MissionBridge


def main():

    root_dir = Path(__file__).resolve().parent.parent

    bridge = MissionBridge(root_dir)

    print("=== MissionBridge 単体テスト ===")

    mission = bridge.create_from_goal(
        "AIアプリを作りたい",
        "MissionBridge経由でMissionManagerへ接続するテスト"
    )

    print("作成Mission:", mission["title"])
    print("種類:", mission["goal_type"])
    print("初期状態:", mission["status"])

    refreshed = bridge.get_resume()

    if refreshed:
        print("再開対象:", refreshed["title"])
        print("再開状態:", refreshed["status"])
        print("進捗:", str(refreshed["progress"]) + "%")

        bridge.start_build(refreshed["id"])
        print("buildingへ変更:", bridge.get_resume()["status"])

        bridge.start_reflection(refreshed["id"])
        print("reflectionへ変更:", bridge.get_resume()["status"])

        bridge.start_improvement(refreshed["id"])
        print("improvingへ変更:", bridge.get_resume()["status"])

        bridge.complete(refreshed["id"])
        print("completedへ変更完了")

    diagnosis = bridge.diagnose()

    print("=== MissionBridge診断 ===")
    print("Mission総数:", diagnosis["mission_count"])
    print("Status別:", diagnosis.get("status_count", {}))
    print("GoalType別:", diagnosis.get("goal_type_count", {}))

    print("=== MissionBridge 単体テスト完了 ===")


if __name__ == "__main__":
    main()