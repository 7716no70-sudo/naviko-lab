import json
from pathlib import Path
from datetime import datetime
from navikoLAB.memory_engine import MemoryEngine
from navikoLAB.personality_engine import PersonalityEngine
from navikoLAB.growth_engine import GrowthEngine
from navikoLAB.decision_engine import DecisionEngine
from navikoLAB.conversation_engine import ConversationEngine

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
IDENTITY_DIR = BASE_DIR / "identity"
CHAT_LOG_DIR = BASE_DIR / "chat_logs"

class Naviko:
    def __init__(self):
        self.name = "ナビ子"
        self.personality_engine = PersonalityEngine(BASE_DIR)
        self.personality = self.personality_engine.get()        
        self.memory = MemoryEngine(BASE_DIR)
        self.load_memory()
        self.growth_engine = GrowthEngine()
        self.growth_identity = self.growth_engine.get_identity()
        self.decision_engine = DecisionEngine()
        self.conversation_engine = ConversationEngine()

    def get_tone_prefix(self):
        return self.personality_engine.tone_prefix()

    def get_startup_message(self):
        mood = self.personality.get("mood", "stable")
        trust = self.personality.get("trust", 0.5)
        warmth = self.personality.get("warmth", 0.5)
        stability = self.personality.get("stability", 0.5)
        memory_count = self.memory.short_count()

        if mood == "happy" and trust >= 0.6:
            return (
                "うん、ナオさん。ナビ子です。"
                f"前回までの会話を {memory_count} 件覚えています。"
                "今日も目標をぶらさず、一緒に進めます。"
            )

        if mood == "focused" or stability >= 0.8:
            return (
                "了解しました、ナオさん。ナビ子です。"
                f"保存済みの会話記憶は {memory_count} 件あります。"
                "今日は実装を安定して進められる状態です。"
            )

        if warmth >= 0.7:
            return (
                "こんにちは、ナオさん。ナビ子です。"
                f"これまでの会話を {memory_count} 件覚えています。"
                "少しずつ、ナオさんの相棒として安定していきます。"
            )

        return (
            "こんにちは、ナオさん。私はナビ子です。"
            f"保存済みの会話記憶は {memory_count} 件です。"
            "今日も会話しながら状態を整えます。"
        )

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

    def load_memory(self):
        self.short_memory = self.load_json(MEMORY_DIR / "short_memory.json", [])
        self.long_memory = self.load_json(MEMORY_DIR / "long_memory.json", [])

        stable_personality_path = BASE_DIR / "stable_life" / "personality" / "stable_personality.json"
        stable_personality = self.load_json(stable_personality_path, {})

        identity_state_path = IDENTITY_DIR / "naviko_identity_state.json"
        current_state = self.load_json(identity_state_path, {})

        self.personality.update(stable_personality)
        self.personality.update(current_state)
        
    def save_state(self):
        self.personality_engine.save()
        self.memory.save()

    def update_personality(self, user_text):
        self.personality_engine.update_by_text(user_text)
        self.personality = self.personality_engine.get()

    def remember(self, user_text, reply):
        self.memory.remember(user_text, reply, self.personality)

    def think_reply(self, user_text, decision=None):
        if decision is None:
            decision = self.decision_engine.decide(user_text)

        tone = self.get_tone_prefix()

        return self.conversation_engine.build_reply(
            user_text=user_text,
            decision=decision,
            personality=self.personality,
            memory=self.memory,
            growth_engine=self.growth_engine,
            growth_identity=self.growth_identity,
            tone=tone,
        )

    def chat(self, user_text):
        decision = self.decision_engine.decide(user_text)

        if decision["action"] == "ignore":
            return ""

        if decision["action"] == "defer":
            tone = self.get_tone_prefix()
            reply = (
                f"{tone}その機能は最終目標には含まれていますが、"
                "今の第一目標である「成長できるAI OSとして起動・会話・記憶・判断できる状態」からは少し先の工程です。"
                "今はナビ子本体の判断コアと自己成長ループの接続を優先します。"
            )
            self.remember(user_text, reply)
            self.save_state()
            return reply

        self.update_personality(user_text)
        reply = self.think_reply(user_text, decision)

        self.remember(user_text, reply)
        self.save_state()
        return reply

   
    def get_next_growth_step(self):
        memory_count = self.memory.short_count()
        return self.growth_engine.next_growth_step(memory_count, self.personality)

        return "判断コアと自己成長ループを接続する"