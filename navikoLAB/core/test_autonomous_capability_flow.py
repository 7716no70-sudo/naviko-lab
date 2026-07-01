from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow


def main():
    root_dir = Path(__file__).resolve().parents[2]

    mission = {
        "id": "test_autonomous_capability_001",
        "title": "YouTube用の短い紹介動画を作りたい",
        "description": "画像AIと動画AIを使って短い紹介動画を作成する",
        "status": "active"
    }

    flow = AutonomousCapabilityFlow(
        root_dir=root_dir
    )

    result = flow.run(
        mission
    )

    print("=== AutonomousCapabilityFlow 統合テスト ===")
    print("Mission ID:", result.get("mission_id"))
    print("タイトル:", result.get("mission_title"))
    print("必要能力:", result.get("required_capabilities"))
    print("不足能力:", result.get("missing_capabilities"))
    print("推奨Agent:", result.get("recommended_agents"))
    print("Agent状態:", result.get("agent_result", {}).get("status"))
    print("実行状態:", result.get("execution_result", {}).get("status"))
    print("MultiAI状態:", result.get("multi_ai_result", {}).get("status"))
    print("MultiAI出力数:", result.get("multi_ai_result", {}).get("output_count"))
    print("MultiAI統合成果:")
    print(result.get("multi_ai_result", {}).get("merged_output"))
    reflection = result.get("multi_ai_reflection", {})

    print("MultiAI評価状態:", reflection.get("status"))
    print("MultiAI評価スコア:", reflection.get("score"))
    print("MultiAI評価 良かった点:", reflection.get("good_points"))
    print("MultiAI評価 改善点:", reflection.get("improvement_points"))
    improvement_request = result.get(
        "multi_ai_improvement_request",
        {}
    )

    print("Improvement要求状態:", improvement_request.get("status"))
    print("Improvement優先度:", improvement_request.get("priority"))
    print("Improvement保存先:", improvement_request.get("file_path"))
    print("")
    print("=== 成果物 ===")
    print(result.get("artifacts", {}).get("merged_output"))
    print("実行数:", result.get("execution_result", {}).get("execution_count"))
    print("保存結果: OK")


if __name__ == "__main__":
    main()