from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

from navikoLAB.capabilities.capability_router import CapabilityRouter
from navikoLAB.capabilities.agent_manager import AgentManager
from navikoLAB.capabilities.agent_executor import AgentExecutor


def make_json_safe(value, seen=None):
    if seen is None:
        seen = set()

    value_id = id(value)

    if isinstance(value, dict):
        if value_id in seen:
            return "[Circular Reference]"
        seen.add(value_id)
        return {
            str(k): make_json_safe(v, seen)
            for k, v in value.items()
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


def normalize_capability_result(capability_result: dict) -> dict:
    required = capability_result.get("required_ids", [])
    selected = capability_result.get("selected", [])
    missing = capability_result.get("missing", [])

    recommended_agents = []

    for capability in selected:
        capability_id = capability.get("id")
        if capability_id:
            recommended_agents.append(capability_id)

    return {
        **capability_result,
        "required_capabilities": required,
        "missing_capabilities": missing,
        "recommended_agents": recommended_agents,
    }


class MissionCapabilityBridge:
    """
    MissionManager と CapabilityRouter を接続する。
    Mission作成時に必要能力・不足能力・推奨エージェントを付与する。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.history_file = (
            self.root_dir
            / "navikoLAB"
            / "core"
            / "mission_capability_bridge_history.json"
        )

        self.router = CapabilityRouter(
            self.root_dir / "navikoLAB"
        )
        self.agent_manager = AgentManager(
            self.root_dir / "navikoLAB"
        )
        self.agent_executor = AgentExecutor(
            self.root_dir / "navikoLAB"
        )

    def attach_capability_result(self, mission):
        purpose = (
            mission.get("purpose")
            or mission.get("title")
            or mission.get("goal")
            or ""
        )

        raw_capability_result = self.router.route(purpose)
        capability_result = normalize_capability_result(raw_capability_result)

        agent_result = self.agent_manager.select_agents(capability_result)
        execution_result = self.agent_executor.execute_agents(
            agent_result,
            mission=mission,
        )

        mission["capability_result"] = capability_result
        mission["agent_result"] = agent_result
        mission["execution_result"] = execution_result

        self.save_history(
            {
                "timestamp": datetime.now().isoformat(),
                "mission_id": mission.get("id"),
                "mission_title": mission.get("title"),
                "purpose": purpose,
                "capability_result": capability_result,
                "agent_result": agent_result,
                "execution_result": execution_result,
            }
        )

        return mission

    def start_reflection(self, mission_id):
        return {
            "mission_id": mission_id,
            "status": "reflection_started",
            "timestamp": datetime.now().isoformat(),
        }

    def save_history(self, result):
        self.history_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        history = []

        if self.history_file.exists():
            try:
                history = json.loads(
                    self.history_file.read_text(encoding="utf-8")
                )
            except Exception:
                history = []

        history.append(make_json_safe(result))

        self.history_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )