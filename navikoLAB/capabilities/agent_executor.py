from __future__ import annotations

from pathlib import Path
from datetime import datetime
import json

from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


class AgentExecutor:
    """
    AgentManager が選択したエージェントを ConnectorDispatcher 経由で実行する。
    現段階では外部API接続は行わず、各Connectorのmock実行を使う。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.history_file = (
            self.root_dir
            / "capabilities"
            / "agent_executor_history.json"
        )
        self.dispatcher = ConnectorDispatcher(
            root_dir=self.root_dir.parent
        )

    def execute_agents(self, agent_result, mission=None):
        mission = mission or {}
        goal = (
            mission.get("purpose")
            or mission.get("title")
            or agent_result.get("purpose")
            or "目的未指定"
        )

        executions = []

        for agent in agent_result.get("agents", []):
            agent_id = agent.get("agent_id", "unknown")

            execution = self.dispatcher.run(
                agent_id,
                goal,
                context={
                    "mission": mission,
                    "agent": agent,
                    "source": "AgentExecutor",
                },
            )

            executions.append(
                {
                    "agent_id": agent_id,
                    "status": execution.get("status", "unknown"),
                    "mode": execution.get("mode", "mock"),
                    "message": execution.get("message") or execution.get("content", ""),
                    "connector": execution.get("connector"),
                    "dispatcher_log": execution.get("dispatcher_log"),
                    "raw_result": execution,
                }
            )

        result = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "execution_count": len(executions),
            "executions": executions,
            "source": "AgentExecutor",
            "dispatcher": "ConnectorDispatcher",
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

        history.append(result)

        self.history_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )