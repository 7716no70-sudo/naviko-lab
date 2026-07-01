import json
import shutil
from pathlib import Path
from datetime import datetime


class MaintenanceManager:
    def __init__(self, root_dir):
        self.root = Path(root_dir)
        self.maintenance_dir = self.root / "maintenance"
        self.maintenance_dir.mkdir(parents=True, exist_ok=True)

        self.backup_dir = self.maintenance_dir / "backups"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def _load_json(self, path, default):
        try:
            path = Path(path)
            if not path.exists():
                return default
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _save_json(self, path, data):
        Path(path).write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def backup_file(self, path):
        path = Path(path)

        if not path.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = self.backup_dir / f"{path.stem}_{timestamp}{path.suffix}"

        shutil.copy2(path, dst)
        return str(dst)

    def cleanup_goal_duplicates(self):
        goal_file = self.root / "goals" / "goal_tree.json"

        if not goal_file.exists():
            return {
                "target": str(goal_file),
                "status": "missing"
            }

        backup = self.backup_file(goal_file)
        data = self._load_json(goal_file, {})

        removed = 0

        for key in [
            "long_goals",
            "mid_goals",
            "short_goals",
            "today_tasks"
        ]:
            items = data.get(key, [])
            seen = set()
            cleaned = []

            for item in items:
                text = item.get("text", "")

                if text in seen:
                    removed += 1
                    continue

                seen.add(text)
                cleaned.append(item)

            data[key] = cleaned

        self._save_json(goal_file, data)

        return {
            "target": str(goal_file),
            "backup": backup,
            "removed": removed,
            "status": "ok"
        }

    def cleanup_memory_duplicates(self):
        memory_dir = self.root / "memory"

        targets = [
            memory_dir / "short_memory.json",
            memory_dir / "mid_memory.json",
            memory_dir / "long_memory.json"
        ]

        results = []
        total_removed = 0

        for file in targets:
            if not file.exists():
                results.append({
                    "target": str(file),
                    "status": "missing"
                })
                continue

            backup = self.backup_file(file)
            data = self._load_json(file, [])

            seen = set()
            cleaned = []
            removed = 0

            for item in data:
                text = item.get("text", "")

                if text in seen:
                    removed += 1
                    continue

                seen.add(text)
                cleaned.append(item)

            self._save_json(file, cleaned)

            total_removed += removed

            results.append({
                "target": str(file),
                "backup": backup,
                "removed": removed,
                "status": "ok"
            })

        return {
            "total_removed": total_removed,
            "results": results
        }

    def trim_log_file(self, file_path, keep_last=30):
        file_path = Path(file_path)

        if not file_path.exists():
            return {
                "target": str(file_path),
                "status": "missing"
            }

        backup = self.backup_file(file_path)
        data = self._load_json(file_path, [])

        if not isinstance(data, list):
            return {
                "target": str(file_path),
                "backup": backup,
                "status": "not_list"
            }

        original_count = len(data)
        trimmed = data[-keep_last:]

        self._save_json(file_path, trimmed)

        return {
            "target": str(file_path),
            "backup": backup,
            "original_count": original_count,
            "kept": len(trimmed),
            "removed": max(0, original_count - len(trimmed)),
            "status": "ok"
        }

    def cleanup_v12_test_data(self):
        results = []

        results.append(
            self.cleanup_goal_duplicates()
        )

        results.append(
            self.cleanup_memory_duplicates()
        )

        results.append(
            self.trim_log_file(
                self.root / "plans" / "task_plan_log.json",
                keep_last=20
            )
        )

        results.append(
            self.trim_log_file(
                self.root / "executions" / "execution_log.json",
                keep_last=20
            )
        )

        results.append(
            self.trim_log_file(
                self.root / "autonomous_core" / "autonomous_core_log.json",
                keep_last=20
            )
        )

        return results

    def format_cleanup_report(self, results):
        lines = []
        lines.append("=== ナビ子 v1.2 メンテナンス結果 ===")

        for item in results:
            lines.append("")
            lines.append(str(item))

        return "\n".join(lines)