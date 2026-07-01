# navikoLAB/multi_agent/agent_manager.py


class AgentManager:
    """
    AgentManager v1.0

    役割:
    - AI OS内の役割をAgentとして管理する
    - まだ外部AIや別プロセスは動かさない
    - Brain / Planner / Execution / Reflection の担当範囲を整理する
    """

    def __init__(self):
        self.agents = {
            "brain": {
                "name": "BrainAgent",
                "role": "全体判断・入力統括",
                "status": "active",
                "can_execute": False,
            },
            "conversation": {
                "name": "ConversationAgent",
                "role": "会話返答・状態説明",
                "status": "active",
                "can_execute": False,
            },
            "memory": {
                "name": "MemoryAgent",
                "role": "会話記憶・短期記憶管理",
                "status": "active",
                "can_execute": False,
            },
            "planner": {
                "name": "PlannerAgent",
                "role": "目的を小さな工程に分解する",
                "status": "active",
                "can_execute": False,
            },
            "execution": {
                "name": "ExecutionAgent",
                "role": "安全モードで工程を実行確認する",
                "status": "active",
                "can_execute": True,
            },
            "reflection": {
                "name": "ReflectionAgent",
                "role": "実行評価を内省し、次の改善材料にする",
                "status": "active",
                "can_execute": False,
            },
            "growth": {
                "name": "GrowthAgent",
                "role": "学習ログから改善候補を考える",
                "status": "active",
                "can_execute": False,
            },
        }

    def list_agents(self):
        return self.agents.copy()

    def get_agent(self, key):
        return self.agents.get(key)

    def active_agents(self):
        return {
            key: value
            for key, value in self.agents.items()
            if value.get("status") == "active"
        }

    def summary(self):
        active = self.active_agents()

        return {
            "status": "ready",
            "agent_count": len(self.agents),
            "active_count": len(active),
            "agents": active,
            "external_ai_enabled": False,
            "real_pc_operation_enabled": False,
        }