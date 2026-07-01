# navikoLAB/multi_agent/agent_route_analyzer.py

from collections import Counter


class AgentRouteAnalyzer:
    """
    AgentRouteAnalyzer v1.0

    役割:
    - AgentRouter の判定ログを分析する
    - どのAgentが多く使われているか集計する
    - safe_mode / external_ai / real_pc_operation を確認する
    """

    def analyze(self, logs):
        if not logs:
            return {
                "status": "no_logs",
                "total": 0,
                "agent_counts": {},
                "all_safe_mode": True,
                "external_ai_used": False,
                "real_pc_operation_used": False,
                "summary": "分析できるAgentRouterログがありません。",
            }

        agents = [item.get("agent") for item in logs if item.get("agent")]
        agent_counts = dict(Counter(agents))

        all_safe_mode = all(item.get("safe_mode") is True for item in logs)
        external_ai_used = any(item.get("external_ai") is True for item in logs)
        real_pc_operation_used = any(item.get("real_pc_operation") is True for item in logs)

        most_used_agent = None
        if agent_counts:
            most_used_agent = max(agent_counts, key=agent_counts.get)

        summary = (
            f"合計{len(logs)}件のルートログを分析しました。"
            f"最も多く使われたAgentは {most_used_agent} です。"
            f"安全モード維持: {all_safe_mode}。"
            f"外部AI使用: {external_ai_used}。"
            f"実PC操作使用: {real_pc_operation_used}。"
        )

        return {
            "status": "analyzed",
            "total": len(logs),
            "agent_counts": agent_counts,
            "most_used_agent": most_used_agent,
            "all_safe_mode": all_safe_mode,
            "external_ai_used": external_ai_used,
            "real_pc_operation_used": real_pc_operation_used,
            "summary": summary,
        }