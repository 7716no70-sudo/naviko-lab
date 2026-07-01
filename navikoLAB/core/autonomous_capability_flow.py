from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json

from navikoLAB.core.mission_capability_bridge import MissionCapabilityBridge
from navikoLAB.capabilities.multi_ai_orchestrator import MultiAIOrchestrator
from navikoLAB.reflection.multi_ai_reflection import MultiAIReflection
from navikoLAB.improvements.multi_ai_improvement_request import MultiAIImprovementRequest


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


class AutonomousCapabilityFlow:
    """
    AutonomousCore から呼び出すための
    Mission → CapabilityRouter → AgentManager → AgentExecutor → MultiAI →
    Reflection → ImprovementRequest 統合フロー。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.history_file = (
            self.root_dir
            / "navikoLAB"
            / "core"
            / "autonomous_capability_flow_history.json"
        )

        self.bridge = MissionCapabilityBridge(
            root_dir=self.root_dir
        )

        self.multi_ai_orchestrator = MultiAIOrchestrator(
            self.root_dir / "navikoLAB"
        )

        self.multi_ai_reflection = MultiAIReflection(
            root_dir=self.root_dir
        )

        self.multi_ai_improvement_request = MultiAIImprovementRequest(
            root_dir=self.root_dir
        )

    def run(self, mission):
        mission = self.bridge.attach_capability_result(
            mission
        )

        capability_result = mission.get(
            "capability_result",
            {}
        )
        agent_result = mission.get(
            "agent_result",
            {}
        )
        execution_result = mission.get(
            "execution_result",
            {}
        )

        multi_ai_result = self.multi_ai_orchestrator.run(
            mission,
            capability_result
        )

        artifacts = {
            "merged_output": multi_ai_result.get(
                "merged_output",
                ""
            ),
            "outputs": multi_ai_result.get(
                "outputs",
                []
            )
        }

        reflection = self.multi_ai_reflection.evaluate(
            mission,
            artifacts
        )

        improvement_request = self.multi_ai_improvement_request.create_request(            
            mission,
            reflection
        )

        result = {
            "timestamp": datetime.now().isoformat(),
            "mission_id": mission.get("id"),
            "mission_title": mission.get("title"),
            "required_capabilities": capability_result.get(
                "required_capabilities",
                []
            ),
            "missing_capabilities": capability_result.get(
                "missing_capabilities",
                []
            ),
            "recommended_agents": capability_result.get(
                "recommended_agents",
                []
            ),
            "agent_result": agent_result,
            "execution_result": execution_result,
            "multi_ai_result": multi_ai_result,
            "multi_ai_reflection": reflection,
            "multi_ai_improvement_request": improvement_request,
            "artifacts": artifacts,
            "status": "completed"
        }

        self.save_history(result)

        return result

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