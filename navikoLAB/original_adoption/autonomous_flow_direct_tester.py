from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "navikoLAB" / "original_adoption" / "autonomous_flow_tests"


def run_direct_test() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    mission = {
        "id": f"dashboard_test_mission_{now}",
        "title": "TODOアプリを作りたい",
        "purpose": "TODOアプリを作りたい",
        "status": "active",
        "created_at": now,
        "source": "mission_dashboard_direct_test",
    }

    flow = AutonomousCapabilityFlow(root_dir=ROOT)
    result = flow.run(mission)

    return {
        "test_id": f"autonomous_flow_direct_test_{now}",
        "status": result.get("status", "unknown"),
        "mission": mission,
        "flow_result": result,
    }


def save_result(result: dict) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = LOG_DIR / f"{result['test_id']}.json"
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    result = run_direct_test()
    output_path = save_result(result)

    flow_result = result.get("flow_result", {})

    print("=== AutonomousCapabilityFlow 直接実行テスト ===")
    print(f"状態: {result['status']}")
    print(f"Mission ID: {flow_result.get('mission_id')}")
    print(f"タイトル: {flow_result.get('mission_title')}")
    print(f"必要能力: {flow_result.get('required_capabilities')}")
    print(f"推奨AI: {flow_result.get('recommended_agents')}")
    print(f"成果物: {flow_result.get('artifacts')}")
    print(f"Reflection: {flow_result.get('reflection') is not None}")
    print(f"Improvement: {flow_result.get('improvement_request') is not None}")
    print(f"保存先: {output_path}")


if __name__ == "__main__":
    main()