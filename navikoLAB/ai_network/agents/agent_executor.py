class AgentExecutor:
    def __init__(self):
        self.allowed_agents = [
            "planner",
            "coder",
            "image",
            "video",
            "research",
            "browser",
            "desktop",
            "file",
            "voice",
        ]

    def execute(self, agent, task, purpose=""):
        if agent not in self.allowed_agents:
            return {
                "agent": agent,
                "status": "blocked",
                "task": task,
                "purpose": purpose,
                "message": "未登録のエージェントです。"
            }

        return {
            "agent": agent,
            "status": "simulated",
            "task": task,
            "purpose": purpose,
            "message": f"{agent} エージェントの仮実行を完了しました。"
        }