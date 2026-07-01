import json
from pathlib import Path
from datetime import datetime


class AutonomyController:
    def __init__(self, root_dir):
        self.root = Path(root_dir)

        self.autonomy_dir = self.root / "autonomy"
        self.autonomy_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.autonomy_dir / "autonomy_state.json"

        if not self.state_file.exists():
            self._save(self._default_state())

    def _default_state(self):
        return {
            "mode": "safe_simulation",
            "permission_level": "simulation_only",
            "allow_real_execution": False,
            "allow_file_write": False,
            "allow_external_access": False,
            "allow_desktop_operation": False,
            "allow_self_patch": False,
            "updated_at": datetime.now().isoformat(timespec="seconds")
        }

    def _load(self):
        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            return self._default_state()

    def _save(self, data):
        data["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.state_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def decide_from_success_rate(self, success_rate, safety_level="警戒"):
        data = self._load()

        if safety_level == "警戒" or success_rate < 40:
            data.update({
                "mode": "safe_simulation",
                "permission_level": "simulation_only",
                "allow_real_execution": False,
                "allow_file_write": False,
                "allow_external_access": False,
                "allow_desktop_operation": False,
                "allow_self_patch": False
            })

        elif success_rate < 70:
            data.update({
                "mode": "limited_assist",
                "permission_level": "limited_file_support",
                "allow_real_execution": False,
                "allow_file_write": True,
                "allow_external_access": False,
                "allow_desktop_operation": False,
                "allow_self_patch": False
            })

        elif success_rate < 90:
            data.update({
                "mode": "guided_execution",
                "permission_level": "guided_execution_with_confirmation",
                "allow_real_execution": True,
                "allow_file_write": True,
                "allow_external_access": True,
                "allow_desktop_operation": False,
                "allow_self_patch": False
            })

        else:
            data.update({
                "mode": "advanced_autonomy",
                "permission_level": "advanced_with_safety_checks",
                "allow_real_execution": True,
                "allow_file_write": True,
                "allow_external_access": True,
                "allow_desktop_operation": False,
                "allow_self_patch": True
            })

        self._save(data)
        return data

    def can_execute_plan(self):
        data = self._load()
        return data.get("allow_real_execution", False)

    def can_write_files(self):
        data = self._load()
        return data.get("allow_file_write", False)

    def can_access_external(self):
        data = self._load()
        return data.get("allow_external_access", False)

    def can_operate_desktop(self):
        data = self._load()
        return data.get("allow_desktop_operation", False)

    def can_self_patch(self):
        data = self._load()
        return data.get("allow_self_patch", False)

    def diagnose_autonomy(self):
        data = self._load()

        return {
            "mode": data.get("mode"),
            "permission_level": data.get("permission_level"),
            "allow_real_execution": data.get("allow_real_execution"),
            "allow_file_write": data.get("allow_file_write"),
            "allow_external_access": data.get("allow_external_access"),
            "allow_desktop_operation": data.get("allow_desktop_operation"),
            "allow_self_patch": data.get("allow_self_patch"),
            "state_file": str(self.state_file)
        }

    def format_autonomy(self):
        data = self._load()

        lines = []
        lines.append("=== ナビ子 v1.2 AutonomyController ===")
        lines.append(f"モード: {data.get('mode')}")
        lines.append(f"許可レベル: {data.get('permission_level')}")
        lines.append("")
        lines.append(f"実行許可: {data.get('allow_real_execution')}")
        lines.append(f"ファイル書込: {data.get('allow_file_write')}")
        lines.append(f"外部アクセス: {data.get('allow_external_access')}")
        lines.append(f"PC操作: {data.get('allow_desktop_operation')}")
        lines.append(f"自己パッチ: {data.get('allow_self_patch')}")
        lines.append(f"保存先: {self.state_file}")

        return "\n".join(lines)