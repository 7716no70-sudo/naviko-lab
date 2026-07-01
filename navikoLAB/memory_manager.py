import json
from pathlib import Path
from datetime import datetime

class MemoryManager:
    def __init__(self, root_dir):
        self.root = Path(root_dir)
        self.memory_dir = self.root / "memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)

        self.short_file = self.memory_dir / "short_memory.json"
        self.mid_file = self.memory_dir / "mid_memory.json"
        self.long_file = self.memory_dir / "long_memory.json"

        for file in [self.short_file, self.mid_file, self.long_file]:
            if not file.exists():
                file.write_text("[]", encoding="utf-8")

    def _load(self, file):
        try:
            return json.loads(file.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _save(self, file, data):
        file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def add_memory(self, text, importance=1, memory_type="short"):
        item = {
            "text": text,
            "importance": importance,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "access_count": 0
        }

        file = self.short_file
        if memory_type == "mid":
            file = self.mid_file
        elif memory_type == "long":
            file = self.long_file

        data = self._load(file)
        data.append(item)
        self._save(file, data)

        return True

    def get_memories(self, memory_type="short", limit=20):
        file = self.short_file
        if memory_type == "mid":
            file = self.mid_file
        elif memory_type == "long":
            file = self.long_file

        data = self._load(file)
        return data[-limit:]

    def promote_important_memories(self):
        short = self._load(self.short_file)
        mid = self._load(self.mid_file)
        long = self._load(self.long_file)

        remaining_short = []

        for item in short:
            if item.get("importance", 1) >= 8:
                long.append(item)
            elif item.get("importance", 1) >= 4:
                mid.append(item)
            else:
                remaining_short.append(item)

        self._save(self.short_file, remaining_short)
        self._save(self.mid_file, mid)
        self._save(self.long_file, long)

        return {
            "short": len(remaining_short),
            "mid": len(mid),
            "long": len(long)
        }

    def diagnose_memory(self):
        return {
            "short_count": len(self._load(self.short_file)),
            "mid_count": len(self._load(self.mid_file)),
            "long_count": len(self._load(self.long_file)),
            "memory_dir": str(self.memory_dir)
        }