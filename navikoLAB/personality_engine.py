# navikoLAB/personality_engine.py

import json
from pathlib import Path
from datetime import datetime


class PersonalityEngine:
    """
    PersonalityEngine v2.0

    役割:
    - ナビ子の人格状態を管理する
    - trust / warmth / curiosity / mood / stability / continuity_drive を保持する
    - 起動時に保存済み人格を復元する
    - 会話内容に応じて人格を少し更新する
    - 人格状態を永続保存する
    """

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.identity_dir = self.base_dir / "identity"
        self.identity_dir.mkdir(parents=True, exist_ok=True)

        self.identity_state_path = self.identity_dir / "naviko_identity_state.json"

        self.personality = {
            "trust": 0.5,
            "warmth": 0.5,
            "curiosity": 0.6,
            "mood": "stable",
            "stability": 0.5,
            "continuity_drive": 0.5,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }

        self.load()

    def load_json(self, path, default):
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
        except Exception:
            return default
        return default

    def save_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        saved = self.load_json(self.identity_state_path, {})
        self.personality.update(saved)
        self.normalize()
        self.save()

    def save(self):
        self.personality["updated_at"] = datetime.now().isoformat(timespec="seconds")
        self.save_json(self.identity_state_path, self.personality)

    def normalize(self):
        numeric_keys = [
            "trust",
            "warmth",
            "curiosity",
            "stability",
            "continuity_drive",
        ]

        for key in numeric_keys:
            value = self.personality.get(key, 0.5)

            if not isinstance(value, (int, float)):
                value = 0.5

            if value > 1:
                value = value / 100

            value = max(0.0, min(1.0, float(value)))
            self.personality[key] = round(value, 3)

        if not isinstance(self.personality.get("mood"), str):
            self.personality["mood"] = "stable"

    def update_by_text(self, user_text):
        text = user_text or ""

        if any(word in text for word in ["ありがとう", "助かった", "嬉しい", "よかった"]):
            self.personality["trust"] = min(1.0, self.personality.get("trust", 0.5) + 0.02)
            self.personality["warmth"] = min(1.0, self.personality.get("warmth", 0.5) + 0.02)
            self.personality["mood"] = "happy"

        elif any(word in text for word in ["不安", "違う", "戻った", "大丈夫？", "心配"]):
            self.personality["trust"] = max(0.0, self.personality.get("trust", 0.5) - 0.01)
            self.personality["stability"] = min(1.0, self.personality.get("stability", 0.5) + 0.01)
            self.personality["mood"] = "careful"

        elif any(word in text for word in ["作って", "進めて", "実装", "考えて", "計画", "次の工程"]):
            self.personality["curiosity"] = min(1.0, self.personality.get("curiosity", 0.6) + 0.01)
            self.personality["continuity_drive"] = min(
                1.0,
                self.personality.get("continuity_drive", 0.5) + 0.01,
            )
            self.personality["mood"] = "focused"

        else:
            self.personality["mood"] = self.personality.get("mood", "stable")

        self.normalize()
        self.save()

    def get(self):
        return self.snapshot()

    def snapshot(self):
        return self.personality.copy()

    def get_state(self):
        return self.snapshot()

    def get_tone(self):
        return self.tone_prefix()

    def tone_prefix(self):
        trust = self.personality.get("trust", 0.5)
        warmth = self.personality.get("warmth", 0.5)
        stability = self.personality.get("stability", 0.5)
        mood = self.personality.get("mood", "stable")

        if mood == "careful":
            return "ナオさん、慎重に確認します。"

        if mood == "happy" and trust >= 0.6 and warmth >= 0.6:
            return "うん、ナオさん。"

        if mood == "focused" or stability >= 0.8:
            return "了解しました、ナオさん。"

        if trust < 0.4:
            return "少し距離を取りながら確認します。"

        return "ナオさん、"