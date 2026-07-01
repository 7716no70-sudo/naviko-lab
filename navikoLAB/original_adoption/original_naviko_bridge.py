from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow


ROOT = Path(__file__).resolve().parents[2]
BRIDGE_LOG_DIR = ROOT / "navikoLAB" / "original_adoption" / "bridge_logs"


def run_original_autonomous_bridge(user_goal: str) -> dict:
    """
    オリジナル naviko.py から呼び出すための安全な入口。
    Mission Dashboard / naviko.py から受け取った目的を
    AutonomousCapabilityFlow へ渡す。
    """

    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    mission = {
        "id": f"original_bridge_mission_{now}",
        "title": user_goal,
        "purpose": user_goal,
        "status": "active",
        "created_at": now,
        "source": "original_naviko_bridge",
    }

    result = {
        "status": "not_started",
        "created_at": now,
        "user_goal": user_goal,
        "mode": "safe_simulation",
        "mission": mission,
        "flow_result": None,
        "flow": [
            "Original naviko.py",
            "Mission Dashboard",
            "original_naviko_bridge",
            "AutonomousCapabilityFlow",
            "MissionCapabilityBridge",
            "CapabilityRouter",
            "AgentManager",
            "AgentExecutor",
            "MultiAIOrchestrator",
            "MultiAIReflection",
            "MultiAIImprovementRequest",
        ],
        "message": "",
    }

    try:
        flow = AutonomousCapabilityFlow(root_dir=ROOT)
        flow_result = flow.run(mission)

        result["flow_result"] = flow_result
        result["status"] = flow_result.get("status", "unknown")
        result["required_capabilities"] = flow_result.get("required_capabilities", [])
        result["missing_capabilities"] = flow_result.get("missing_capabilities", [])
        result["recommended_agents"] = flow_result.get("recommended_agents", [])
        result["artifacts"] = flow_result.get("artifacts", {})
        result["multi_ai_reflection"] = flow_result.get("multi_ai_reflection", {})
        result["multi_ai_improvement_request"] = flow_result.get("multi_ai_improvement_request", {})
        result["message"] = "AutonomousCapabilityFlow の実行が完了しました。"

    except Exception as error:
        result["status"] = "bridge_runtime_error"
        result["message"] = str(error)

    BRIDGE_LOG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = BRIDGE_LOG_DIR / f"original_naviko_bridge_{now}.json"

    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result["log_file"] = str(output_path)
    return result


def main() -> None:
    result = run_original_autonomous_bridge("TODOアプリを作りたい")

    print("=== Original Naviko Bridge 実フロー診断 ===")
    print(f"状態: {result['status']}")
    print(f"モード: {result['mode']}")
    print(f"目的: {result['user_goal']}")
    print(f"必要能力: {result.get('required_capabilities')}")
    print(f"不足能力: {result.get('missing_capabilities')}")
    print(f"推奨AI: {result.get('recommended_agents')}")
    print(f"成果物あり: {bool(result.get('artifacts'))}")
    print(f"Reflectionあり: {bool(result.get('multi_ai_reflection'))}")
    print(f"Improvementあり: {bool(result.get('multi_ai_improvement_request'))}")
    print(f"保存先: {result['log_file']}")


if __name__ == "__main__":
    main()