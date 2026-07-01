from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
LAB_DIR = ROOT_DIR / "navikoLAB"

sys.path.append(str(LAB_DIR))
sys.path.append(str(LAB_DIR / "core"))

from autonomous_core import AutonomousCore
from task_planner import TaskPlanner
from plan_executor import PlanExecutor
from autonomy_controller import AutonomyController
from mission_bridge import MissionBridge


def main():

    print("=== AutonomousCore Mission接続テスト ===")

    task_planner = TaskPlanner(LAB_DIR)
    plan_executor = PlanExecutor(LAB_DIR)
    autonomy_controller = AutonomyController(LAB_DIR)
    mission_bridge = MissionBridge(LAB_DIR)

    core = AutonomousCore(
        LAB_DIR,
        task_planner=task_planner,
        plan_executor=plan_executor,
        autonomy_controller=autonomy_controller,
        mission_bridge=mission_bridge
    )

    result = core.process_purpose(
        "AIアプリを作りたい"
    )

    print("Status:", result["status"])

    if result.get("mission"):
        print("Mission:", result["mission"]["title"])
        print("Mission種類:", result["mission"]["goal_type"])
        print("Mission状態:", result["mission"]["status"])
    else:
        print("Mission: なし")

    print("Messages:")

    for message in result.get("messages", []):
        print("-", message)

    diagnosis = core.diagnose_core()

    print("=== Core診断 ===")

    for key, value in diagnosis.items():
        print(key + ":", value)

    bridge_diagnosis = mission_bridge.diagnose()

    print("=== Mission診断 ===")
    print("Status別:", bridge_diagnosis.get("status_count", {}))
    print("GoalType別:", bridge_diagnosis.get("goal_type_count", {}))

    print("=== AutonomousCore Mission接続テスト完了 ===")


if __name__ == "__main__":
    main()