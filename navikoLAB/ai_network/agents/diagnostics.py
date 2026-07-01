class AgentDiagnostics:
    def diagnose(self, histories):
        total = len(histories)
        failed_agents = []

        latest_status = "履歴なし"
        latest_file = "なし"

        if histories:
            latest = histories[0]
            latest_file = latest.get("file", "不明")

            data = latest.get("data", {})
            execution_result = data.get("execution_result", {})
            latest_status = execution_result.get("status", "不明")

            for result in execution_result.get("results", []):
                if result.get("status") not in ["simulated", "completed"]:
                    failed_agents.append(
                        result.get("agent", "不明")
                    )

        return {
            "history_count": total,
            "latest_file": latest_file,
            "latest_status": latest_status,
            "failed_agents": failed_agents
        }