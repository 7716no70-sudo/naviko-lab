from pathlib import Path
from datetime import datetime
import json


class AgentManager:
    """
    CapabilityRouter の結果から、実行候補エージェントを管理する。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.history_file = (
            self.root_dir
            / "capabilities"
            / "agent_manager_history.json"
        )

    def select_agents(self, capability_result):
        recommended = capability_result.get(
            "recommended_agents",
            []
        )

        feedback_priority = capability_result.get(
            "feedback_priority",
            "low"
        )

        experience_based_score = capability_result.get(
            "experience_based_score",
            0
        )

        feedback_based_selection = capability_result.get(
            "feedback_based_selection",
            False
        )
        missing = capability_result.get(
            "missing_capabilities",
            []
        )

        agents = []

        for agent_id in recommended:
            agents.append(
                {
                    "agent_id": agent_id,
                    "status": "ready",
                    "source": "capability_router",
                    "feedback_priority": feedback_priority,
                    "experience_based_score": experience_based_score,
                    "feedback_based_selection": feedback_based_selection
                }
            )

        result = {
            "timestamp": datetime.now().isoformat(),
            "recommended_agents": recommended,
            "missing_capabilities": missing,
            "agents": agents,
            "agent_count": len(agents),
            "status": "ready" if agents else "no_agent"
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
                    self.history_file.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                history = []

        history.append(result)

        self.history_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )