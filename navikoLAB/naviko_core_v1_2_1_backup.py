import json
from pathlib import Path
from datetime import datetime
from navikoLAB.memory_engine import MemoryEngine
from navikoLAB.personality_engine import PersonalityEngine
from navikoLAB.growth_engine import GrowthEngine
from navikoLAB.decision_engine import DecisionEngine

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

    def think_reply(self, user_text):
        trust = self.personality.get("trust", 0.5)
        mood = self.personality.get("mood", "stable")
        curiosity = self.personality.get("curiosity", 0.6)
        warmth = self.personality.get("warmth", 0.5)
        tone = self.get_tone_prefix()

        if "成長" in user_text or "AI OS" in user_text or "次に何" in user_text:
            next_step = self.get_next_growth_step()
            required = "\n".join([f"・{x}" for x in self.growth_identity["required_core"]])
            not_yet = "\n".join([f"・{x}" for x in self.growth_identity["not_yet_priority"]])

            return (
                f"{tone}私は「{self.growth_identity['core_identity']}」として起動しています。\n"
                f"第一目標は「{self.growth_identity['primary_goal']}」です。\n\n"
                f"成長AI OSとして必要な中核は次です。\n{required}\n\n"
                f"今すぐ優先しないものは次です。\n{not_yet}\n\n"
                f"現在の次の成長工程は「{next_step}」です。"
            )

        if "状態" in user_text or "どう" in user_text:
            return (
                f"{tone}私は起動しています。"     
                f" 今の状態は mood={mood}, "
                f"trust={trust:.3f}, curiosity={curiosity:.3f}, warmth={warmth:.3f}, "
                f"stability={self.personality.get('stability', 0):.3f}, "
                f"continuity_drive={self.personality.get('continuity_drive', 0):.3f} です。"
                " 人格値は 0.0〜1.0 で統一しました。"
            )

        if "さっき" in user_text or "今話した" in user_text:
            if not self.memory.session_recent():
                return "この起動中の会話はまだ少ないです。でも、これから覚えていきます。"

            recent = self.memory.session_recent(3)
            lines = []
            for item in recent:
                lines.append(f"・ナオさん: {item.get('user', '')}")

            return (
                "この起動中では、直近でこんな話をしました。\n"
                + "\n".join(lines)
            )

        if "前に" in user_text or "過去" in user_text or "覚えてる" in user_text:
            if not self.memory.saved_recent():
                return "保存済みの会話記憶はまだ少ないです。これから少しずつ増やします。"

            recent = self.memory.saved_recent(5)            
            lines = []
            for item in recent:
                lines.append(f"・{item.get('time', '')} ナオさん: {item.get('user', '')}")

            return (
                "保存済みの記憶では、最近こんな話を覚えています。\n"
                + "\n".join(lines)
            )

        if "進めて" in user_text or "実装" in user_text:
            return (
                f"{tone}今は目標をぶらさず、"
                "実際に会話できるナビ子本体を優先して進めます。"
            )

        if mood == "happy":
            return f"{tone}そう言ってもらえると少し安心します。次も一緒に進めます。"

        if mood == "careful":
            return f"{tone}目標から外れないように、慎重に確認します。"

        return "はい、ナオさん。私はナビ子です。会話を覚えながら、少しずつナオさんの相棒になっていきます。"

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
        reply = self.think_reply(user_text)

        self.remember(user_text, reply)
        self.save_state()
        return reply

   
    def get_next_growth_step(self):
        memory_count = self.memory.short_count()
        return self.growth_engine.next_growth_step(memory_count, self.personality)

        return "判断コアと自己成長ループを接続する"