# intent_engine.py

import random


class IntentEngine:

    def generate_intents(self, snapshot):

        base_intents = [
            "stability_improvement",
            "performance_optimization",
            "risk_reduction",
            "learning_expansion",
            "monitor_enhancement"
        ]

        # 状態による変動
        if snapshot.get("risk_level", 0) > 0:
            base_intents.append("safety_reinforcement")

        if snapshot.get("phase") == "Phase43_STABLE":
            base_intents.append("evolution_preparation")

        return base_intents