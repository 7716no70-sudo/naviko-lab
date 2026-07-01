import json
from pathlib import Path
from datetime import datetime
from navikoLAB.planner_feedback.planner_feedback_adapter import (
    build_task_planner_feedback,
)
from navikoLAB.planner_feedback.experience_based_planning_scorer import (
    score_plan_with_experience,
)

class TaskPlanner:
    def __init__(self, root_dir, agent_registry=None):
        self.root = Path(root_dir)
        self.agent_registry = agent_registry

        self.plan_dir = self.root / "plans"
        self.plan_dir.mkdir(parents=True, exist_ok=True)

        self.plan_log_file = self.plan_dir / "task_plan_log.json"

        if not self.plan_log_file.exists():
            self.plan_log_file.write_text("[]", encoding="utf-8")

    def _load_log(self):
        try:
            return json.loads(self.plan_log_file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save_log(self, data):
        self.plan_log_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def analyze_purpose(self, purpose):
        text = str(purpose).lower()

        capability_keywords = {
            "code": [
                "コード", "python", "アプリ", "プログラム", "修正",
                "エラー", "実装", "開発", "debug", "app", "code"
            ],
            "image": [
                "画像", "イラスト", "絵", "デザイン", "ロゴ",
                "サムネ", "image", "illustration", "design"
            ],
            "video": [
                "動画", "映像", "編集", "youtube", "ショート",
                "video", "movie", "editing"
            ],
            "research": [
                "調査", "比較", "分析", "情報収集", "deep research",
                "research", "search", "まとめ"
            ],
            "browser": [
                "web", "ブラウザ", "サイト", "オンライン", "検索",
                "browser", "internet"
            ],
            "desktop": [
                "pc操作", "パソコン操作", "画面操作", "自動操作",
                "desktop", "operation"
            ],
            "file": [
                "ファイル", "保存", "読み込み", "変換", "整理",
                "zip", "pdf", "csv", "json", "document", "file"
            ],
            "voice": [
                "音声", "読み上げ", "ナレーション", "声",
                "voice", "audio", "speech"
            ],
            "plan": [
                "計画", "手順", "工程", "段取り", "目標",
                "plan", "task", "strategy"
            ]
        }

        required_capabilities = []

        for capability, keywords in capability_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    required_capabilities.append(capability)
                    break

        if not required_capabilities:
            required_capabilities.append("plan")

        return required_capabilities

    def select_agents(self, capabilities):
        selected = []

        if not self.agent_registry:
            return selected

        for capability in capabilities:
            matches = self.agent_registry.find_agents_by_capability(capability)

            for agent_id in matches:
                if agent_id not in selected:
                    selected.append(agent_id)

        if "planner" not in selected:
            selected.insert(0, "planner")

        return selected

    def create_plan(self, purpose):
        planner_feedback = build_task_planner_feedback(purpose)

        planner_recommendations = planner_feedback.get(
            "planner_recommendations",
            [],
        )

        planner_hints = planner_feedback.get(
            "planner_hints",
            {},
        )
        capabilities = self.analyze_purpose(purpose)
        agents = self.select_agents(capabilities)

        steps = []

        steps.append("目的を確認する")
        steps.append("必要な能力を分類する")

        for agent_id in agents:
            steps.append(f"{agent_id} エージェントを使う準備をする")

        steps.append("小さな単位で実行する")
        steps.append("結果を確認する")
        steps.append("必要なら改善案を作る")

        plan = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "purpose": purpose,
            "required_capabilities": capabilities,
            "selected_agents": agents,
            "steps": steps,
            "status": "planned"
        }

        log = self._load_log()
        log.append(plan)
        self._save_log(log)

        plan["planner_feedback"] = {
            "recommendations": planner_recommendations,
            "planner_hints": planner_hints,
            "success_count": planner_feedback.get("success_count", 0),
            "failure_count": planner_feedback.get("failure_count", 0),
        }

        plan["experience_based_planning"] = True

        plan = score_plan_with_experience(plan)

        return plan

    def diagnose_planner(self):
        log = self._load_log()

        return {
            "plan_count": len(log),
            "plan_log_file": str(self.plan_log_file),
            "agent_registry_connected": self.agent_registry is not None
        }

    def format_plan(self, plan):
        lines = []
        lines.append("=== ナビ子 v1.2 TaskPlanner 実行計画 ===")
        lines.append(f"目的: {plan.get('purpose')}")
        lines.append("")
        lines.append("必要能力:")
        for cap in plan.get("required_capabilities", []):
            lines.append(f"- {cap}")

        lines.append("")
        lines.append("選択エージェント:")
        for agent in plan.get("selected_agents", []):
            lines.append(f"- {agent}")

        lines.append("")
        lines.append("実行手順:")
        for i, step in enumerate(plan.get("steps", []), start=1):
            lines.append(f"{i}. {step}")

        return "\n".join(lines)