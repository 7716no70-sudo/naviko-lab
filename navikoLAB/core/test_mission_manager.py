from pathlib import Path
from mission_manager import MissionManager


def test_goal(manager, title, description=""):

    mission = manager.create_mission(
        title,
        description
    )

    tasks = manager.generate_tasks_by_goal(
        mission["id"]
    )

    print("---------------")
    print("ミッション:", mission["title"])
    print("種類:", mission["goal_type"])
    print("タスク数:", len(tasks))

    for index, task in enumerate(tasks, start=1):
        print(str(index) + ".", task["title"])


def main():

    root_dir = Path(__file__).resolve().parent.parent

    manager = MissionManager(root_dir)

    print("=== MissionManager 目的別タスク分解テスト ===")

    test_goal(manager, "TODOアプリを作りたい")
    test_goal(manager, "簡単なゲームを作りたい")
    test_goal(manager, "YouTube用の短い紹介動画を作りたい")
    test_goal(manager, "画像生成ツールを作りたい")
    test_goal(manager, "AIエージェント管理ツールを作りたい")
    test_goal(manager, "新しい企画を進めたい")

    diagnosis = manager.diagnose()

    print("===============")
    print("=== 診断 ===")

    for key, value in diagnosis.items():
        print(key + ":", value)


if __name__ == "__main__":
    main()