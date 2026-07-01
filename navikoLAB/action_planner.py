import json
from pathlib import Path
from datetime import datetime


class ActionPlanner:
    def __init__(self, root_dir):
        self.root = Path(root_dir)

        self.action_dir = self.root / "actions"
        self.action_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.action_log_file = (
            self.action_dir /
            "action_plan_log.json"
        )

        if not self.action_log_file.exists():
            self.action_log_file.write_text(
                "[]",
                encoding="utf-8"
            )

    def _load_log(self):
        try:
            return json.loads(
                self.action_log_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return []

    def _save_log(self, data):
        self.action_log_file.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def create_action_plan(
        self,
        purpose,
        plan=None
    ):
        actions = []

        text = str(purpose).lower()

        if (
            "アプリ" in text
            or "app" in text
            or "python" in text
        ):
            actions.extend([
                "requirements.txtを整理する",
                "プロジェクトフォルダを作成する",
                "main.pyを作成する",
                "テストコードを準備する",
                "成果物を保存する"
            ])

        elif (
            "動画" in text
            or "youtube" in text
            or "video" in text
        ):
            actions.extend([
                "動画構成を作成する",
                "必要画像を整理する",
                "音声原稿を作成する",
                "編集工程を作成する",
                "成果物を保存する"
            ])

        elif (
            "画像" in text
            or "image" in text
        ):
            actions.extend([
                "画像仕様を整理する",
                "参考情報を集める",
                "生成プロンプトを作成する",
                "成果物を保存する"
            ])

        else:
            actions.extend([
                "目的を分析する",
                "作業を分解する",
                "必要情報を整理する",
                "成果物を保存する"
            ])

        result = {
            "created_at":
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            "purpose": purpose,
            "actions": actions,
            "status": "planned"
        }

        log = self._load_log()
        log.append(result)
        self._save_log(log)

        return result

    def diagnose_action_planner(self):
        log = self._load_log()

        return {
            "action_plan_count": len(log),
            "action_log_file":
                str(self.action_log_file)
        }

    def format_action_plan(
        self,
        result
    ):
        lines = []

        lines.append(
            "=== ナビ子 v1.3 ActionPlanner ==="
        )

        lines.append(
            f"目的: {result.get('purpose')}"
        )

        lines.append("")
        lines.append("具体的作業:")

        for i, action in enumerate(
            result.get("actions", []),
            start=1
        ):
            lines.append(
                f"{i}. {action}"
            )

        return "\n".join(lines)