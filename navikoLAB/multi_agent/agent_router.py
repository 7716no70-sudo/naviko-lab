# navikoLAB/multi_agent/agent_router.py


class AgentRouter:
    """
    AgentRouter v1.0

    役割:
    - ユーザー入力やintentを見て担当Agentを選ぶ
    - まだ外部AIや別プロセスは呼ばない
    - AI OS内部の役割分担だけを行う
    """

    def route(self, user_text, decision=None):
        text = user_text or ""
        intent = (decision or {}).get("intent", "chat")

        if intent == "memory_check" or any(word in text for word in ["記憶", "覚えて", "さっき"]):
            return self._route("memory", "記憶確認要求")

        if intent == "plan_request" or any(word in text for word in ["計画", "作って", "実装", "進めて"]):
            return self._route("planner", "計画・実装要求")

        if intent == "growth_check" or any(word in text for word in ["成長", "改善", "自己改善"]):
            return self._route("growth", "成長・改善要求")

        if any(word in text for word in ["評価", "振り返り", "内省", "Reflection"]):
            return self._route("reflection", "評価・内省要求")

        if any(word in text for word in ["実行", "安全モード"]):
            return self._route("execution", "実行確認要求")

        if any(word in text for word in ["状態", "調子", "会話"]):
            return self._route("conversation", "会話・状態確認要求")

        return self._route("brain", "通常入力")

    def _route(self, agent_key, reason):
        return {
            "agent": agent_key,
            "reason": reason,
            "external_ai": False,
            "real_pc_operation": False,
            "safe_mode": True,
        }