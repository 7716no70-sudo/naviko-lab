from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow
from navikoLAB.improvements.multi_ai_improvement_request import MultiAIImprovementRequest


def main():
    root_dir = Path(__file__).resolve().parents[1]

    mission = {
        "id": "test_multi_ai_improvement_001",
        "title": "YouTube用の短い紹介動画を作りたい",
        "description": "画像AIと動画AIとChatGPTで紹介動画を作る",
        "status": "active"
    }

    flow = AutonomousCapabilityFlow(
        root_dir=root_dir.parent
    )

    flow_result = flow.run(
        mission
    )

    reflection = flow_result.get(
        "multi_ai_reflection",
        {}
    )

    requester = MultiAIImprovementRequest(
        root_dir=root_dir
    )

    request = requester.create_request(
        mission,
        reflection
    )

    print("=== MultiAI Improvement Request テスト ===")
    print("Mission ID:", request.get("mission_id"))
    print("タイトル:", request.get("mission_title"))
    print("Reflection状態:", request.get("reflection_status"))
    print("Reflectionスコア:", request.get("reflection_score"))
    print("優先度:", request.get("priority"))
    print("状態:", request.get("status"))
    print("保存先:", request.get("file_path"))

    print("")
    print("改善点:")
    for item in request.get("improvement_points", []):
        print("-", item)

    print("")
    print("次アクション:")
    for item in request.get("suggested_next_actions", []):
        print("-", item.get("action"))


if __name__ == "__main__":
    main()