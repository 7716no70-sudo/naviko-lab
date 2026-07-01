from __future__ import annotations


class NavikoCore:
    """
    Phase148ベース：オリジナルナビ子コア（再起動版）
    """

    def __init__(self):
        # --- 基本人格 ---
        self.personality = {
            "warmth": 0.6,
            "curiosity": 0.7,
            "caution": 0.4,
            "stability": 0.7,
        }

        # --- 状態 ---
        self.memory = []
        self.goals = []
        self.thought_state = "idle"

        # --- 自律性 ---
        self.autonomy_enabled = True
        self.learning_enabled = True

    # ----------------------------
    # Memory System
    # ----------------------------
    def remember(self, text: str):
        self.memory.append(text)

    def recall(self) -> list:
        return self.memory[-10:]

    # ----------------------------
    # Thought System
    # ----------------------------
    def think(self, input_text: str) -> str:
        self.thought_state = "processing"

        response = f"ナビ子（復元版）が考えた: {input_text}"

        self.thought_state = "idle"
        return response

    # ----------------------------
    # Goal System
    # ----------------------------
    def add_goal(self, goal: str):
        self.goals.append(goal)

    def get_goals(self):
        return self.goals

    # ----------------------------
    # Self Update (safe)
    # ----------------------------
    def learn(self, experience: str):
        if self.learning_enabled:
            self.remember(experience)


def run_reactivation_demo():
    naviko = NavikoCore()

    # 初期起動テスト
    naviko.remember("Phase148 baseline restored")
    naviko.add_goal("安定した自律AIとして動作する")

    result = {
        "status": "reactivated",
        "core_state": "Phase148_restored_runtime",
        "memory_sample": naviko.recall(),
        "goals": naviko.get_goals(),
        "sample_thought": naviko.think("こんにちはナビ子")
    }

    return result


def main():
    result = run_reactivation_demo()

    print("=== Phase220 Core System Reactivation ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()