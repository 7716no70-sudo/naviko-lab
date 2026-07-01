# state_scanner.py

import json
import os
from datetime import datetime


class StateScanner:

    def __init__(self, context_path=None):
        self.context_path = context_path or "naviko_state.json"

    def scan(self):
        state = self._load_state()

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "phase": state.get("phase", "unknown"),
            "risk_level": state.get("risk_level", 0),
            "workspace_only": state.get("WorkspaceOnly", True),
            "original_write": state.get("OriginalWrite", False),
            "external_operation": state.get("ExternalOperation", False),
            "pending_adoption": state.get("pending_adoption", 0)
        }

        return snapshot

    def _load_state(self):
        if not os.path.exists(self.context_path):
            return {}
        with open(self.context_path, "r", encoding="utf-8") as f:
            return json.load(f)