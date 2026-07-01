from pathlib import Path

from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge
from navikoLAB.capabilities.agent_manager import AgentManager
from navikoLAB.capabilities.agent_executor import AgentExecutor


def main():
    root_dir = Path(__file__).resolve().parents[1]

    mission = {
        "id": "test_agent_flow_001",
        "title": "YouTube用の短い紹介動画を作りたい",
        "description": "画像AIと動画AIを使って紹介動画を作る",
        "status": "active"
    }

    bridge = MissionCapabilityBridge(
        root_dir=root_dir.parent
    )

    mission = bridge.attach_capability_result(
        mission
    )

    agent_manager = AgentManager(
        root_dir=root_dir
    )

    agent_result = agent_manager.select_agents(
        mission.get("capability_result", {})
    )

    executor = AgentExecutor(
        root_dir=root_dir
    )

    execution_result = executor.execute_agents(
        agent_result,
        mission
    )

    print("=== AgentManager / AgentExecutor 接続テスト ===")
    print("Mission ID:", mission.get("id"))
    print("目的:", mission.get("title"))
    print("必要能力:", mission.get("required_capabilities"))
    print("不足能力:", mission.get("missing_capabilities"))
    print("選択Agent:", agent_result.get("recommended_agents"))
    print("Agent数:", agent_result.get("agent_count"))
    print("実行数:", execution_result.get("execution_count"))
    print("実行状態:", execution_result.get("status"))

    for item in execution_result.get("executions", []):
        print("-", item.get("agent_id"), "/", item.get("status"))


if __name__ == "__main__":
    main()