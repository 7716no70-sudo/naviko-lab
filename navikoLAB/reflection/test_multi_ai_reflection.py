from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow
from navikoLAB.reflection.multi_ai_reflection import MultiAIReflection


def main():
    root_dir = Path(__file__).resolve().parents[1]

    mission = {
        "id": "test_multi_ai_reflection_001",
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

    reflector = MultiAIReflection(
        root_dir=root_dir
    )

    reflection = reflector.evaluate(
        mission,
        flow_result.get("artifacts", {})
    )

    print("=== MultiAI Reflection テスト ===")
    print("Mission ID:", reflection.get("mission_id"))
    print("タイトル:", reflection.get("mission_title"))
    print("状態:", reflection.get("status"))
    print("スコア:", reflection.get("score"))
    print("成果物文字数:", reflection.get("artifact_length"))
    print("出力数:", reflection.get("output_count"))

    print("")
    print("良かった点:")
    for item in reflection.get("good_points", []):
        print("-", item)

    print("")
    print("改善点:")
    for item in reflection.get("improvement_points", []):
        print("-", item)


if __name__ == "__main__":
    main()