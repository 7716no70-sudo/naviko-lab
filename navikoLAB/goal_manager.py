import json
from pathlib import Path
from datetime import datetime


class GoalManager:
    def __init__(self, root_dir):
        self.root = Path(root_dir)
        self.goal_dir = self.root / "goals"
        self.goal_dir.mkdir(parents=True, exist_ok=True)

        self.goal_file = self.goal_dir / "goal_tree.json"

        if not self.goal_file.exists():
            self._save({
                "dream": "",
                "long_goals": [],
                "mid_goals": [],
                "short_goals": [],
                "today_tasks": [],
                "updated_at": datetime.now().isoformat(timespec="seconds")
            })

    def _load(self):
        try:
            return json.loads(self.goal_file.read_text(encoding="utf-8"))
        except Exception:
            return {
                "dream": "",
                "long_goals": [],
                "mid_goals": [],
                "short_goals": [],
                "today_tasks": [],
                "updated_at": datetime.now().isoformat(timespec="seconds")
            }

    def _save(self, data):
        data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.goal_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def set_dream(self, dream):
        data = self._load()
        data["dream"] = dream
        self._save(data)
        return True

    def add_goal(self, level, text):
        data = self._load()

        key_map = {
            "long": "long_goals",
            "mid": "mid_goals",
            "short": "short_goals",
            "today": "today_tasks"
        }

        key = key_map.get(level)

        if not key:
            return False, "level は long / mid / short / today のどれかにしてください。"

        data[key].append({
            "text": text,
            "done": False,
            "created_at": datetime.now().isoformat(timespec="seconds")
        })

        self._save(data)
        return True, "目標を追加しました。"

    def complete_goal(self, level, index):
        data = self._load()

        key_map = {
            "long": "long_goals",
            "mid": "mid_goals",
            "short": "short_goals",
            "today": "today_tasks"
        }

        key = key_map.get(level)

        if not key:
            return False, "level が不正です。"

        if index < 0 or index >= len(data[key]):
            return False, "指定された番号の目標がありません。"

        data[key][index]["done"] = True
        data[key][index]["completed_at"] = datetime.now().isoformat(timespec="seconds")

        self._save(data)
        return True, "完了にしました。"

    def get_goal_tree(self):
        return self._load()

    def diagnose_goals(self):
        data = self._load()

        return {
            "dream_exists": bool(data.get("dream")),
            "long_count": len(data.get("long_goals", [])),
            "mid_count": len(data.get("mid_goals", [])),
            "short_count": len(data.get("short_goals", [])),
            "today_count": len(data.get("today_tasks", [])),
            "goal_file": str(self.goal_file)
        }

    def format_goals(self):
        data = self._load()

        lines = []
        lines.append("=== ナビ子 v1.2 目標ツリー ===")
        lines.append(f"夢: {data.get('dream') or '未設定'}")
        lines.append("")

        sections = [
            ("長期目標", "long_goals"),
            ("中期目標", "mid_goals"),
            ("短期目標", "short_goals"),
            ("今日やること", "today_tasks"),
        ]

        for title, key in sections:
            lines.append(f"【{title}】")
            items = data.get(key, [])

            if not items:
                lines.append("- なし")
            else:
                for i, item in enumerate(items):
                    mark = "完了" if item.get("done") else "未完了"
                    lines.append(f"{i}. [{mark}] {item.get('text')}")

            lines.append("")

        return "\n".join(lines)