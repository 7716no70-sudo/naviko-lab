from pathlib import Path

from mission_bridge import MissionBridge


def main():

    root_dir = Path(__file__).resolve().parent.parent

    bridge = MissionBridge(root_dir)

    diagnosis = bridge.diagnose()
    resume = bridge.get_resume()

    print("=== MissionBridge 診断 ===")

    print("Mission総数:", diagnosis["mission_count"])
    print("Status別:", diagnosis.get("status_count", {}))
    print("GoalType別:", diagnosis.get("goal_type_count", {}))

    if resume:
        print("再開対象:", resume["title"])
        print("再開状態:", resume["status"])
        print("再開進捗:", str(resume["progress"]) + "%")
    else:
        print("再開対象: なし")

    print("Mission保存先:", diagnosis["mission_file"])
    print("履歴保存先:", diagnosis["history_file"])

    print("=== MissionBridge 診断完了 ===")


if __name__ == "__main__":
    main()