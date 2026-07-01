from __future__ import annotations


class Memory:
    def __init__(self):
        self.data = []

    def add(self, text: str):
        self.data.append(text)

    def get_recent(self):
        return self.data[-5:]


class ThinkEngine:
    def think(self, memory, input_text: str) -> str:
        context = ", ".join(memory.get_recent())
        return f"思考結果: {input_text}（文脈: {context}）"


class DecisionEngine:
    def decide(self, thought: str) -> str:
        if "危険" in thought:
            return "avoid"
        if "重要" in thought:
            return "prioritize"
        return "proceed"


class ExecutionEngine:
    def execute(self, decision: str, task: str) -> str:
        if decision == "avoid":
            return f"[SKIP] {task}"
        if decision == "prioritize":
            return f"[PRIORITY EXEC] {task}"
        return f"[EXEC] {task}"


class NavikoOS:
    def __init__(self):
        self.memory = Memory()
        self.think_engine = ThinkEngine()
        self.decision_engine = DecisionEngine()
        self.execution_engine = ExecutionEngine()

        self.state = "Phase224_full_ai_os_running"

    def step(self, input_text: str) -> dict:
        # 1. Memory
        self.memory.add(input_text)

        # 2. Think
        thought = self.think_engine.think(self.memory, input_text)

        # 3. Decide
        decision = self.decision_engine.decide(thought)

        # 4. Execute
        result = self.execution_engine.execute(decision, input_text)

        return {
            "input": input_text,
            "thought": thought,
            "decision": decision,
            "result": result,
            "state": self.state
        }


def run_demo():
    os = NavikoOS()

    outputs = []
    outputs.append(os.step("タスク整理をする"))
    outputs.append(os.step("重要なレポート確認"))
    outputs.append(os.step("危険な処理チェック"))

    return {
        "status": "full_ai_os_running",
        "outputs": outputs
    }


def main():
    result = run_demo()

    print("=== Phase224 Full AI OS Restart ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()