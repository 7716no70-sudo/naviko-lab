from pathlib import Path

from navikoLAB.autonomous_core import AutonomousCore
from navikoLAB.memory_manager import MemoryManager
from navikoLAB.goal_manager import GoalManager
from navikoLAB.agent_registry import AgentRegistry
from navikoLAB.task_planner import TaskPlanner
from navikoLAB.plan_executor import PlanExecutor
from navikoLAB.autonomy_controller import AutonomyController
from navikoLAB.core.mission_bridge import MissionBridge


def main():
    root_dir = Path(__file__).resolve().parent

    core = AutonomousCore(
        root_dir,
        memory_manager=MemoryManager(root_dir),
        goal_manager=GoalManager(root_dir),
        agent_registry=AgentRegistry(root_dir),
        task_planner=TaskPlanner(root_dir),
        plan_executor=PlanExecutor(root_dir),
        autonomy_controller=AutonomyController(root_dir),
        mission_bridge=MissionBridge(root_dir)
    )

    result = core.process_purpose(
        "YouTube用の短い紹介動画を作りたい"
    )

    print("=== AutonomousCore × CapabilityFlow 接続テスト ===")
    print("状態:", result.get("status"))
    print("Mission:", "OK" if result.get("mission") else "NG")
    print("CapabilityFlow:", "OK" if result.get("capability_flow") else "NG")

    flow = result.get("capability_flow", {})

    print("必要能力:", flow.get("required_capabilities"))
    print("不足能力:", flow.get("missing_capabilities"))
    print("推奨Agent:", flow.get("recommended_agents"))
    print("Agent状態:", flow.get("agent_result", {}).get("status"))
    print("実行状態:", flow.get("execution_result", {}).get("status"))
    print("実行数:", flow.get("execution_result", {}).get("execution_count"))

    multi_ai = flow.get("multi_ai_result", {})

    print("MultiAI状態:", multi_ai.get("status"))
    print("MultiAI出力数:", multi_ai.get("output_count"))
    print("MultiAI統合成果:")
    print(multi_ai.get("merged_output"))
    reflection = flow.get(
        "multi_ai_reflection",
        {}
    )

    print("MultiAI評価状態:", reflection.get("status"))
    print("MultiAI評価スコア:", reflection.get("score"))
    print("MultiAI評価 良かった点:", reflection.get("good_points"))
    print("MultiAI評価 改善点:", reflection.get("improvement_points"))

    improvement_request = flow.get(
        "multi_ai_improvement_request",
        {}
    )

    print("Improvement要求状態:", improvement_request.get("status"))
    print("Improvement優先度:", improvement_request.get("priority"))
    print("Improvement保存先:", improvement_request.get("file_path"))

    print("Messages:")
    for message in result.get("messages", []):
        print("-", message)


if __name__ == "__main__":
    main()