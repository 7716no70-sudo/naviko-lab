# experience_logger.py

import json
import os
from datetime import datetime


class ExperienceLogger:

    def __init__(self, log_path="background_loop_log.json"):
        self.log_path = log_path

    def log(self, snapshot, phase_report, decision):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "snapshot": snapshot,
            "phase_report": phase_report,
            "decision": decision
        }

        data = self._load()
        data.append(entry)
        self._save(data)

    def _load(self):
        if not os.path.exists(self.log_path):
            return []
        with open(self.log_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)