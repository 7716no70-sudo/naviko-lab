from pathlib import Path

from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge


def main():
    root_dir = Path(__file__).resolve().parents[2]

    bridge = MissionCapabilityBridge(root_dir=root_dir)

    mission = {
        "id": "test_mission_capability_001",
        "title": "YouTube用の短い紹介動画を作りたい",
        "description": "画像と動画AIを使って短い紹介動画を作成する",
        "status": "active"
    }

    result = bridge.attach_capability_result(mission)

    print("=== Mission × CapabilityRouter 接続テスト ===")
    print("Mission ID:", result.get("id"))
    print("タイトル:", result.get("title"))
    print("説明:", result.get("description"))
    print("必要能力:", result.get("required_capabilities"))
    print("不足能力:", result.get("missing_capabilities"))
    print("推奨エージェント:", result.get("recommended_agents"))
    print("能力判定:", result.get("capability_result"))
    print("保存結果: OK")


if __name__ == "__main__":
    main()