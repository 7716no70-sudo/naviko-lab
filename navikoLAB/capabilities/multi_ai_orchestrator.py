from pathlib import Path
from datetime import datetime
import json


class MultiAIOrchestrator:
    """
    複数AIの実行結果をまとめる統合オーケストレーター。
    現段階では安全のため mock 実行のみ。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        self.history_file = (
            self.root_dir
            / "capabilities"
            / "multi_ai_orchestrator_history.json"
        )

    def run(self, mission, capability_result):
        recommended_agents = capability_result.get(
            "recommended_agents",
            []
        )

        outputs = []

        for agent_id in recommended_agents:
            outputs.append(
                self.mock_agent_output(
                    agent_id,
                    mission
                )
            )

        result = {
            "timestamp": datetime.now().isoformat(),
            "mission_id": mission.get("id", "unknown"),
            "mission_title": mission.get("title", ""),
            "recommended_agents": recommended_agents,
            "output_count": len(outputs),
            "outputs": outputs,
            "merged_output": self.merge_outputs(outputs),
            "status": "completed" if outputs else "no_output"
        }

        self.save_history(result)

        return result

    def mock_agent_output(self, agent_id, mission):
        title = mission.get("title", "")

        if agent_id == "chatgpt":
            content = f"{title} の構成案・台本案を作成しました。"

        elif agent_id == "image_ai":
            content = f"{title} に必要な画像素材案を作成しました。"

        elif agent_id == "video_ai":
            content = f"{title} の動画構成・編集案を作成しました。"

        elif agent_id == "voice_ai":
            content = f"{title} のナレーション案を作成しました。"

        elif agent_id == "browser":
            content = f"{title} に必要な調査結果をまとめました。"

        elif agent_id == "app_operator":
            content = f"{title} に必要なアプリ操作手順を作成しました。"

        else:
            content = f"{agent_id} のmock成果物を作成しました。"

        return {
            "agent_id": agent_id,
            "status": "completed",
            "mode": "mock",
            "content": content
        }

    def merge_outputs(self, outputs):
        lines = []
        lines.append("=== MultiAI 統合成果 ===")

        for item in outputs:
            lines.append("")
            lines.append(f"[{item.get('agent_id')}]")
            lines.append(item.get("content", ""))

        return "\n".join(lines)

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