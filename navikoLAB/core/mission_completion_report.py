from pathlib import Path
import json

from mission_bridge import MissionBridge


def count_history(history_file):

    if not history_file.exists():
        return 0

    try:
        history = json.loads(
            history_file.read_text(
                encoding="utf-8"
            )
        )
        return len(history)

    except Exception:
        return 0


def main():

    root_dir = Path(__file__).resolve().parent.parent

    bridge = MissionBridge(root_dir)

    diagnosis = bridge.diagnose()
    resume = bridge.get_resume()

    history_count = count_history(
        bridge.mission_manager.history_file
    )

    required_keys = [
        "mission_count",
        "active_count",
        "completed_count",
        "task_count",
        "done_task_count",
        "goal_type_count",
        "status_count",
        "mission_file",
        "history_file"
    ]

    missing_keys = []

    for key in required_keys:
        if key not in diagnosis:
            missing_keys.append(key)

    completion_checks = {
        "Mission作成": diagnosis["mission_count"] > 0,
        "Task生成": diagnosis["task_count"] > 0,
        "GoalType分類": len(diagnosis.get("goal_type_count", {})) > 0,
        "Status管理": len(diagnosis.get("status_count", {})) > 0,
        "履歴保存": history_count > 0,
        "途中再開": resume is not None,
        "診断項目": len(missing_keys) == 0
    }

    completed_count = 0

    for result in completion_checks.values():
        if result:
            completed_count += 1

    completion_rate = int(
        completed_count / len(completion_checks) * 100
    )

    print("=== MissionManager v1 完成診断 ===")

    for name, result in completion_checks.items():
        print(name + ":", "OK" if result else "NG")

    print("---------------")
    print("完成率:", str(completion_rate) + "%")
    print("Mission総数:", diagnosis["mission_count"])
    print("Task総数:", diagnosis["task_count"])
    print("Status別:", diagnosis.get("status_count", {}))
    print("GoalType別:", diagnosis.get("goal_type_count", {}))
    print("履歴件数:", history_count)

    if resume:
        print("再開対象:", resume["title"])
        print("再開状態:", resume["status"])
    else:
        print("再開対象: なし")

    if missing_keys:
        print("不足診断項目:", missing_keys)
    else:
        print("不足診断項目: なし")

    if completion_rate >= 100:
        print("判定: MissionManager v1 完成")
    else:
        print("判定: MissionManager v1 要改善")

    print("=== MissionManager v1 完成診断完了 ===")


if __name__ == "__main__":
    main()