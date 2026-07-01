# navikoLAB/multi_agent/agent_route_logger.py

import json
from pathlib import Path
from datetime import datetime


class AgentRouteLogger:
    """
    AgentRouteLogger v1.0

    役割:
    - AgentRouter の判定結果を保存する
    - 後から安全監査・自己改善に使えるようにする
    """

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.log_dir = self.base_dir / "multi_agent" / "route_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.log_dir / "agent_route_log.json"

    def load_logs(self):
        try:
            if self.log_path.exists():
                with open(self.log_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
        except Exception:
            return []
        return []

    def save_logs(self, logs):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def record(self, user_text, decision, route):
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "input": user_text,
            "intent": decision.get("intent"),
            "risk": decision.get("risk"),
            "action": decision.get("action"),
            "agent": route.get("agent"),
            "reason": route.get("reason"),
            "safe_mode": route.get("safe_mode"),
            "external_ai": route.get("external_ai"),
            "real_pc_operation": route.get("real_pc_operation"),
        }

        logs = self.load_logs()
        logs.append(entry)

        if len(logs) > 200:
            logs = logs[-200:]

        self.save_logs(logs)
        return entry

    def recent(self, limit=5):
        logs = self.load_logs()
        return logs[-limit:]