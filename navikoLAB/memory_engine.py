# navikoLAB/memory_engine.py

import json
from pathlib import Path
from datetime import datetime


class MemoryEngine:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.memory_dir = self.base_dir / "memory"
        self.short_memory_path = self.memory_dir / "short_memory.json"
        self.long_memory_path = self.memory_dir / "long_memory.json"

        self.short_memory = []
        self.long_memory = []
        self.session_memory = []

        self.load()

    def load_json(self, path, default):
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            return default
        return default

    def save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        self.short_memory = self.load_json(self.short_memory_path, [])
        self.long_memory = self.load_json(self.long_memory_path, [])

    def remember(self, user_text, reply, personality):
        entry = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "user": user_text,
            "naviko": reply,
            "personality": personality.copy(),
        }

        self.session_memory.append(entry)
        self.short_memory.append(entry)

        if len(self.session_memory) > 20:
            self.session_memory = self.session_memory[-20:]

        if len(self.short_memory) > 50:
            self.short_memory = self.short_memory[-50:]

    def save(self):
        self.save_json(self.short_memory_path, self.short_memory)

    def session_recent(self, limit=3):
        return self.session_memory[-limit:]

    def saved_recent(self, limit=5):
        return self.short_memory[-limit:]

    def short_count(self):
        return len(self.short_memory)