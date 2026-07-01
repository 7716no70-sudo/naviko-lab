from __future__ import annotations


class ExecutionEngine:
    def execute_task(self, task: str, decision: str) -> str:
        if decision == "avoid":
            return f"[SKIP] {task}（危険回避）"
        elif decision == "prioritize":
            return f"[EXECUTE-PRIORITY] {task}"
        else:
            return f"[EXECUTE] {task}"


class ActionRouter:
    def route(self, action: str) -> str:
        return f"routing -> {action}"


class NavikoExecutor:
    def __init__(self):
        self.engine = ExecutionEngine()
        self.router = ActionRouter()
        self.state = "Phase223_execution_restored"

    def run(self, goal: str, decision: str) -> dict:
        action_result = self.engine.execute_task(goal, decision)
        routed = self.router.route(action_result)

        return {
            "goal": goal,
            "decision": decision,
            "action_result": action_result,
            "route": routed,
            "state": self.state
        }


def run_demo():
    naviko = NavikoExecutor()

    result1 = naviko.run("ファイル整理", "prioritize")
    result2 = naviko.run("不明タスク", "avoid")
    result3 = naviko.run("通常処理", "proceed")

    return {
        "status": "execution_restored",
        "sample1": result1,
        "sample2": result2,
        "sample3": result3
    }


def main():
    result = run_demo()

    print("=== Phase223 Execution Layer Restore ===")
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()