# navikoLAB/growth_engine.py


class GrowthEngine:
    def __init__(self):
        self.growth_identity = {
            "core_identity": "成長できるAI OSとしてのナビ子",
            "primary_goal": "ナビ子を、成長できるAI OSとして起動・会話・記憶・判断できる状態にする",
            "current_stage": "Naviko v1.1 modular growth core",
            "required_core": [
                "人格",
                "記憶",
                "会話",
                "目標",
                "自己成長",
                "判断",
                "安全な実行",
            ],
            "not_yet_priority": [
                "画像生成",
                "動画生成",
                "音声生成",
                "金融解析",
                "ネット投稿",
                "本格PC操作",
            ],
        }

    def get_identity(self):
        return self.growth_identity

    def next_growth_step(self, memory_count, personality):
        trust = personality.get("trust", 0.5)
        stability = personality.get("stability", 0.5)

        if memory_count < 50:
            return "会話記憶をさらに安定させる"

        if trust < 0.7:
            return "ナオさんとの信頼関係を会話で育てる"

        if stability < 0.8:
            return "人格と返答の安定性を高める"

        return "判断コアと自己成長ループを接続する"