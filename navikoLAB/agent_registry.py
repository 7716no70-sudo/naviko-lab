import json
from pathlib import Path
from datetime import datetime


class AgentRegistry:
    def __init__(self, root_dir):
        self.root = Path(root_dir)
        self.agent_dir = self.root / "agents"
        self.agent_dir.mkdir(parents=True, exist_ok=True)

        self.agent_file = self.agent_dir / "agent_registry.json"

        if not self.agent_file.exists():
            self._save(self._default_agents())

    def _default_agents(self):
        return {
            "coder": {
                "name": "コーディングAI",
                "description": "Pythonやアプリ開発、コード修正を担当する。",
                "capabilities": ["code", "debug", "app", "automation"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            },
            "image": {
                "name": "画像生成AI",
                "description": "画像生成、イラスト作成、ビジュアル案を担当する。",
                "capabilities": ["image", "illustration", "design"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            },
            "video": {
                "name": "動画生成AI",
                "description": "動画生成、動画構成、映像制作を担当する。",
                "capabilities": ["video", "movie", "editing"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            },
            "research": {
                "name": "Deep Research AI",
                "description": "調査、情報収集、比較、要約を担当する。",
                "capabilities": ["research", "search", "summary", "compare"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            },
            "browser": {
                "name": "Web操作AI",
                "description": "Web閲覧、ブラウザ操作、オンライン情報確認を担当する。",
                "capabilities": ["web", "browser", "online"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            },
            "desktop": {
                "name": "PC操作AI",
                "description": "ローカルPC操作、ファイル起動、画面操作の計画を担当する。",
                "capabilities": ["desktop", "pc", "operation"],
                "enabled": False,
                "success_count": 0,
                "failure_count": 0
            },
            "file": {
                "name": "ファイル処理AI",
                "description": "ファイル作成、整理、変換、読み書きを担当する。",
                "capabilities": ["file", "document", "convert", "organize"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            },
            "voice": {
                "name": "音声AI",
                "description": "音声生成、読み上げ、会話音声化を担当する。",
                "capabilities": ["voice", "speech", "audio"],
                "enabled": False,
                "success_count": 0,
                "failure_count": 0
            },
            "planner": {
                "name": "計画AI",
                "description": "目的分解、手順作成、優先順位づけを担当する。",
                "capabilities": ["plan", "goal", "task", "strategy"],
                "enabled": True,
                "success_count": 0,
                "failure_count": 0
            }
        }

    def _load(self):
        try:
            return json.loads(self.agent_file.read_text(encoding="utf-8"))
        except Exception:
            return self._default_agents()

    def _save(self, data):
        wrapper = {
            "updated_at": datetime.now().isoformat(timespec="seconds"),
            "agents": data
        }

        self.agent_file.write_text(
            json.dumps(wrapper, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def _load_agents(self):
        data = self._load()

        if "agents" in data:
            return data.get("agents", {})

        return data

    def list_agents(self):
        return self._load_agents()

    def get_agent(self, agent_id):
        agents = self._load_agents()
        return agents.get(agent_id)

    def enable_agent(self, agent_id):
        agents = self._load_agents()

        if agent_id not in agents:
            return False, "指定されたエージェントがありません。"

        agents[agent_id]["enabled"] = True
        self._save(agents)
        return True, "エージェントを有効化しました。"

    def disable_agent(self, agent_id):
        agents = self._load_agents()

        if agent_id not in agents:
            return False, "指定されたエージェントがありません。"

        agents[agent_id]["enabled"] = False
        self._save(agents)
        return True, "エージェントを無効化しました。"

    def record_result(self, agent_id, success=True):
        agents = self._load_agents()

        if agent_id not in agents:
            return False, "指定されたエージェントがありません。"

        if success:
            agents[agent_id]["success_count"] += 1
        else:
            agents[agent_id]["failure_count"] += 1

        self._save(agents)
        return True, "実行結果を記録しました。"

    def find_agents_by_capability(self, keyword):
        agents = self._load_agents()
        matches = []

        keyword = str(keyword).lower()

        for agent_id, info in agents.items():
            if not info.get("enabled", False):
                continue

            capabilities = [
                str(cap).lower()
                for cap in info.get("capabilities", [])
            ]

            description = str(info.get("description", "")).lower()
            name = str(info.get("name", "")).lower()

            if (
                keyword in capabilities
                or keyword in description
                or keyword in name
            ):
                matches.append(agent_id)

        return matches

    def diagnose_agents(self):
        agents = self._load_agents()

        enabled_count = 0
        disabled_count = 0

        for info in agents.values():
            if info.get("enabled"):
                enabled_count += 1
            else:
                disabled_count += 1

        return {
            "agent_count": len(agents),
            "enabled_count": enabled_count,
            "disabled_count": disabled_count,
            "agent_file": str(self.agent_file)
        }

    def format_agents(self):
        agents = self._load_agents()

        lines = []
        lines.append("=== ナビ子 v1.2 AgentRegistry ===")

        for agent_id, info in agents.items():
            status = "有効" if info.get("enabled") else "無効"
            lines.append("")
            lines.append(f"[{agent_id}] {info.get('name')} / {status}")
            lines.append(f"説明: {info.get('description')}")
            lines.append(
                "能力: " + ", ".join(info.get("capabilities", []))
            )
            lines.append(
                f"成功: {info.get('success_count', 0)} / "
                f"失敗: {info.get('failure_count', 0)}"
            )

        return "\n".join(lines)