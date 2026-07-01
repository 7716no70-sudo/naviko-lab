from pathlib import Path

from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge
from navikoLAB.capabilities.multi_ai_orchestrator import MultiAIOrchestrator


def main():
    root_dir = Path(__file__).resolve().parents[1]

    mission = {
        "id": "test_multi_ai_001",
        "title": "YouTube用の短い紹介動画を作りたい",
        "description": "画像AIと動画AIとChatGPTで紹介動画を作る",
        "status": "active"
    }

    bridge = MissionCapabilityBridge(
        root_dir=root_dir.parent
    )

    mission = bridge.attach_capability_result(
        mission
    )

    orchestrator = MultiAIOrchestrator(
        root_dir
    )

    result = orchestrator.run(
        mission,
        mission.get("capability_result", {})
    )

    print("=== MultiAIOrchestrator テスト ===")
    print("Mission ID:", result.get("mission_id"))
    print("タイトル:", result.get("mission_title"))
    print("推奨AI:", result.get("recommended_agents"))
    print("出力数:", result.get("output_count"))
    print("状態:", result.get("status"))
    print("")
    print(result.get("merged_output"))


if __name__ == "__main__":
    main()