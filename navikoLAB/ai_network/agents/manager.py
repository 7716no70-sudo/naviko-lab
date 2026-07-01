from .capability_router import CapabilityRouter
from .agent_executor import AgentExecutor
from .execution_history import ExecutionHistory
from .diagnostics import AgentDiagnostics


class AgentManager:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.router = CapabilityRouter()
        self.executor = AgentExecutor()
        self.history = ExecutionHistory(root_dir)
        self.diagnostics = AgentDiagnostics()

    def route(self, purpose):
        return self.router.route(purpose)

    def execute(self, purpose):
        agents = self.route(purpose)

        results = []

        for agent in agents:
            task = f"{purpose} に対して {agent} の役割を実行する"

            result = self.executor.execute(
                agent=agent,
                task=task,
                purpose=purpose
            )

            results.append(result)

        execution_result = {
            "purpose": purpose,
            "agents": agents,
            "results": results,
            "status": "simulated_completed"
        }

        history_file = self.history.save(execution_result)

        return {
            "execution_result": execution_result,
            "history_file": str(history_file)
        }

    def list_history(self):
        return self.history.list_recent()

    def diagnose(self):
        histories = self.history.list_recent()
        return self.diagnostics.diagnose(histories)