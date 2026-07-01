from __future__ import annotations


class MemorySystem:
    def __init__(self):
        self.short_term = []
        self.long_term = []

    def add(self, text: str):
        self.short_term.append(text)
        if len(self.short_term) > 5:
            moved = self.short_term.pop(0)
            self.long_term.append(moved)

    def recall(self):
        return {
            "short_term": self.short_term,
            "long_term": self.long_term
        }


class PersonalitySystem:
    def __init__(self):
        # Phase148ベース人格
        self.traits = {
            "warmth": 0.6,
            "curiosity": 0.7,
            "caution": 0.4,
            "friendliness": 0.65,
            "stability": 0.7
        }

        self.trust = 0.5
        self.mood = "neutral"

    def update_trust(self, delta: float):
        self.trust = max(0.0, min(1.0, self.trust + delta))

    def update_mood(self, mood: str):
        self.mood = mood

    def describe(self):
        return {
            "traits": self.traits,
            "trust": self.trust,
            "mood": self.mood
        }


class NavikoCore:
    def __init__(self):
        self.memory = MemorySystem()
        self.personality = PersonalitySystem()
        self.state = "Phase221_personality_restored"

    def process(self, text: str) -> str:
        self.memory.add(text)

        # 簡易感情反応（復元版）
        if "ありがとう" in text:
            self.personality.update_trust(+0.05)
            self.personality.update_mood("happy")

        elif "ごめん" in text:
            self.personality.update_mood("concerned")

        else:
            self.personality.update_mood("thinking")

        return f"ナビ子（人格復元版）: {text} を受け取ったよ"


def run_demo():
    naviko = NavikoCore()

    naviko.process("こんにちはナビ子")
    naviko.process("ありがとう")

    return {
        "status": "personality_restored",
        "memory": naviko.memory.recall(),
        "personality": naviko.personality.describe(),
        "state": naviko.state
    }


def main():
    result = run_demo()

    print("=== Phase221 Memory & Personality Restore ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()