from pathlib import Path
import json

from mission_manager import MissionManager


def count_history(manager):

    if not manager.history_file.exists():
        return 0

    try:
        history = json.loads(
            manager.history_file.read_text(
                encoding="utf-8"
            )
        )
        return len(history)

    except Exception:
        return 0


def main():

    root_dir = Path(__file__).resolve().parent.parent

    manager = MissionManager(root_dir)

    diagnosis = manager.diagnose()
    resume = manager.get_resume_mission()
    history_count = count_history(manager)

    print("=== MissionManager 診断 ===")

    print("Mission総数:", diagnosis["mission_count"])
    print("Active:", diagnosis["active_count"])
    print("Completed:", diagnosis["completed_count"])

    print("Task総数:", diagnosis["task_count"])
    print("Task完了数:", diagnosis["done_task_count"])

    print("GoalType別:", diagnosis["goal_type_count"])
    
    if "status_count" in diagnosis:
        print("Status別:", diagnosis["status_count"])

    if diagnosis["task_count"] > 0:
        average_done_rate = int(
            diagnosis["done_task_count"] / diagnosis["task_count"] * 100
        )
    else:
        average_done_rate = 0

    print("全体タスク完了率:", str(average_done_rate) + "%")

    if resume:
        print("途中再開Mission:", resume["title"])
        print("途中再開進捗:", str(resume["progress"]) + "%")
    else:
        print("途中再開Mission: なし")

    print("履歴件数:", history_count)

    print("Mission保存先:", diagnosis["mission_file"])
    print("履歴保存先:", diagnosis["history_file"])

    print("=== MissionManager 診断完了 ===")


if __name__ == "__main__":
    main()