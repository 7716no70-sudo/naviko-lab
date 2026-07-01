from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.connectors.app_operator_connector import AppOperatorConnector
from navikoLAB.connectors.chatgpt_connector import ChatGPTConnector
from navikoLAB.connectors.claude_connector import ClaudeConnector
from navikoLAB.connectors.gemini_connector import GeminiConnector
from navikoLAB.connectors.grok_connector import GrokConnector
from navikoLAB.connectors.browser_connector import BrowserConnector
from navikoLAB.connectors.ai_connector_selector import select_ai_connector
from navikoLAB.connectors.real_app_operator_connector import RealAppOperatorConnector

class ConnectorDispatcher:
    """
    agent_id に応じて各 Connector へ処理を振り分ける。
    今後 Claude / Gemini / Browser / Image / Video などをここに追加する。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.log_dir = self.root_dir / "navikoLAB" / "connectors" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.connector_map = {
            "chatgpt": ChatGPTConnector,
            "claude": ClaudeConnector,
            "gemini": GeminiConnector,
            "grok": GrokConnector,
            "browser": BrowserConnector,
            "app_operator": AppOperatorConnector,
            "real_app_operator": RealAppOperatorConnector,
        }

    def run(self, agent_id: str, goal: str, context: dict | None = None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        original_agent_id = agent_id

        context = context or {}

        feedback_priority = context.get(
            "feedback_priority",
            "low",
        )

        experience_based_score = context.get(
            "experience_based_score",
            0,
        )

        feedback_based_selection = context.get(
            "feedback_based_selection",
            False,
        )

        if agent_id in {"text_ai", "auto_ai", "ai"}:
            selection = select_ai_connector(
                task_type=(context or {}).get("task_type", "general"),
                preferred=(context or {}).get("preferred_ai"),
            )

            selected = selection.get("selected")

            if selected:
                agent_id = selected
            else:
                result = {
                    "agent_id": original_agent_id,
                    "connector": "ai_selector",
                    "status": "safe_skipped",
                    "mode": "selector",
                    "goal": goal,
                    "reason": selection.get("reason", "no configured AI connector"),
                    "selection": selection,
                    "content": None,
                    "context": context or {},
                }

                result.setdefault("created_at", now)
                result["dispatcher"] = "ConnectorDispatcher"

                log_path = self.log_dir / f"connector_dispatcher_{original_agent_id}_{now}.json"
                log_path.write_text(
                    json.dumps(result, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                result["dispatcher_log"] = str(log_path)

                return result

        connector_class = self.connector_map.get(agent_id)

        if connector_class:
            if agent_id == "app_operator":
                connector = connector_class(root_dir=self.root_dir)
                result = connector.run(goal, context=context)

            elif agent_id == "real_app_operator":
                connector = connector_class(dry_run=True)

                task = {
                    "purpose": goal,
                    **(context or {}),
                }

                result = connector.run(task)

            elif agent_id == "browser":
                connector = connector_class()
                result = connector.run({
                    "action": "search",
                    "query": goal,
                    "context": context or {},
                })

            else:
                connector = connector_class()
                result = connector.run(goal)

        else:
            result = self.run_default_mock(agent_id, goal, context=context)     

        result.setdefault("agent_id", agent_id)
        result.setdefault("created_at", now)
        result["dispatcher"] = "ConnectorDispatcher"

        if original_agent_id != agent_id:
            result["requested_agent_id"] = original_agent_id
            result["selected_agent_id"] = agent_id

        log_path = self.log_dir / f"connector_dispatcher_{agent_id}_{now}.json"
        log_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        result["dispatcher_log"] = str(log_path)

        result["feedback_priority"] = feedback_priority
        result["experience_based_score"] = experience_based_score
        result["feedback_based_selection"] = feedback_based_selection
        result["connector_feedback_connected"] = True

        return result

    def run_default_mock(self, agent_id: str, goal: str, context: dict | None = None) -> dict:
        return {
            "agent_id": agent_id,
            "connector": agent_id,
            "status": "completed",
            "mode": "mock",
            "goal": goal,
            "content": f"{agent_id} が {goal} のためのmock成果を作成しました。",
            "context": context or {},
        }


def main() -> None:
    dispatcher = ConnectorDispatcher()

    print("=== ConnectorDispatcher 診断 ===")

    for agent_id in ["chatgpt", "browser", "app_operator"]:
        result = dispatcher.run(
            agent_id,
            "TODOアプリを作りたい",
            context={"source": "dispatcher_test"},
        )

        print(f"- {agent_id}")
        print(f"  状態: {result.get('status')}")
        print(f"  モード: {result.get('mode')}")
        print(f"  内容: {result.get('content')}")
        print(f"  保存先: {result.get('dispatcher_log')}")


if __name__ == "__main__":
    main()