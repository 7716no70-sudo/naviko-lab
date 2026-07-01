# state_seeder.py

import json
import os


class StateSeeder:

    def __init__(self, path="naviko_state.json"):
        self.path = path

    def seed_if_missing(self):
        if not os.path.exists(self.path):
            self._write_default()
            return

        with open(self.path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except:
                data = {}

        # ■ 必須キー補完
        changed = False

        if "phase" not in data:
            data["phase"] = "Phase43_STABLE"
            changed = True

        if "risk_level" not in data:
            data["risk_level"] = 0
            changed = True

        if "pending_adoption" not in data:
            data["pending_adoption"] = 0
            changed = True

        if "WorkspaceOnly" not in data:
            data["WorkspaceOnly"] = True
            changed = True

        if "ExternalOperation" not in data:
            data["ExternalOperation"] = False
            changed = True

        if changed:
            self._save(data)

    def _write_default(self):
        data = {
            "phase": "Phase43_STABLE",
            "risk_level": 0,
            "pending_adoption": 0,
            "WorkspaceOnly": True,
            "ExternalOperation": False,
            "OriginalWrite": False
        }

        self._save(data)

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)