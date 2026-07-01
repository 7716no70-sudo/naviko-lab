from pathlib import Path

from mission_bridge import MissionBridge


def main():

    root_dir = Path(__file__).resolve().parent.parent

    bridge = MissionBridge(root_dir)

    print("=== Mission Autonomous Flow テスト ===")

    goal = "動画編集ツールを作りたい"

    mission = bridge.create_from_goal(
        goal,
        "AutonomousCore接続前の安全フローテスト"
    )

    print("目的:", goal)
    print("Mission作成:", mission["title"])
    print("種類:", mission["goal_type"])
    print("状態:", mission["status"])

    resume = bridge.get_resume()

    if not resume:
        print("再開対象がありません")
        return

    print("再開対象:", resume["title"])

    bridge.start_build(resume["id"])
    print("状態変更: building")

    bridge.start_reflection(resume["id"])
    print("状態変更: reflection")

    bridge.start_improvement(resume["id"])
    print("状態変更: improving")

    bridge.complete(resume["id"])
    print("状態変更: completed")

    diagnosis = bridge.diagnose()

    print("=== Flow診断 ===")
    print("Mission総数:", diagnosis["mission_count"])
    print("Status別:", diagnosis.get("status_count", {}))
    print("GoalType別:", diagnosis.get("goal_type_count", {}))

    print("=== Mission Autonomous Flow テスト完了 ===")


if __name__ == "__main__":
    main()