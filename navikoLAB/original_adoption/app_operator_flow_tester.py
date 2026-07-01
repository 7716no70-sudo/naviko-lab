from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "navikoLAB" / "original_adoption" / "app_operator_tests"


def make_json_safe(value, seen=None):
    if seen is None:
        seen = set()

    value_id = id(value)

    if isinstance(value, dict):
        if value_id in seen:
            return "[Circular Reference]"
        seen.add(value_id)
        return {
            str(key): make_json_safe(item, seen)
            for key, item in value.items()
        }

    if isinstance(value, list):
        if value_id in seen:
            return "[Circular Reference]"
        seen.add(value_id)
        return [
            make_json_safe(item, seen)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_safe(item, seen)
            for item in value
        ]

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    return str(value)


def run_test() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    mission = {
        "id": f"app_operator_test_mission_{now}",
        "title": "TODOアプリを作りたい",
        "purpose": "TODOアプリを作りたい",
        "status": "active",
        "created_at": now,
        "source": "app_operator_flow_tester",
    }

    flow = AutonomousCapabilityFlow(root_dir=ROOT)
    result = flow.run(mission)

    execution_result = result.get("execution_result", {})
    executions = execution_result.get("executions", [])

    app_operator_execution = None
    for execution in executions:
        if execution.get("agent_id") == "app_operator":
            app_operator_execution = execution
            break

    return {
        "test_id": f"app_operator_flow_test_{now}",
        "status": "passed" if app_operator_execution else "failed",
        "mission": mission,
        "required_capabilities": result.get("required_capabilities", []),
        "missing_capabilities": result.get("missing_capabilities", []),
        "recommended_agents": result.get("recommended_agents", []),
        "execution_count": execution_result.get("execution_count", 0),
        "executions": executions,
        "app_operator_execution": app_operator_execution,
        "flow_result_status": result.get("status"),
        "flow_result": result,
    }


def save_result(result: dict) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = LOG_DIR / f"{result['test_id']}.json"

    safe_result = make_json_safe(result)

    output_path.write_text(
        json.dumps(safe_result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    result = run_test()
    output_path = save_result(result)

    print("=== AppOperator Flow 確認 ===")
    print(f"状態: {result['status']}")
    print(f"Flow状態: {result['flow_result_status']}")
    print(f"必要能力: {result['required_capabilities']}")
    print(f"不足能力: {result['missing_capabilities']}")
    print(f"推奨Agent: {result['recommended_agents']}")
    print(f"実行数: {result['execution_count']}")
    print("実行Agent:")
    for execution in result["executions"]:
        print(
            f"- {execution.get('agent_id')} / "
            f"{execution.get('status')} / "
            f"{execution.get('mode')} / "
            f"{execution.get('connector')}"
        )
    print(f"app_operator実行あり: {result['app_operator_execution'] is not None}")
    print(f"保存先: {output_path}")


if __name__ == "__main__":
    main()