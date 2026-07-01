# navikoLAB/memory/memory_agent.py


class MemoryAgent:
    """
    MemoryAgent v1.0

    役割:
    - 会話記憶・学習ログ・AgentRouterログをまとめて見る
    - 記憶の重要度を簡易判定する
    - 後の長期記憶化の土台にする
    """

    def analyze_memory_context(self, memory_items, learning_items=None, route_items=None):
        memory_items = memory_items or []
        learning_items = learning_items or []
        route_items = route_items or []

        important_keywords = [
            "目的",
            "目標",
            "改善",
            "学習",
            "計画",
            "実行",
            "評価",
            "安全",
            "記憶",
            "Agent",
            "AI OS",
        ]

        analyzed = []

        for item in memory_items:
            user_text = item.get("user", "")
            score = 0
            reasons = []

            for keyword in important_keywords:
                if keyword in user_text:
                    score += 1
                    reasons.append(f"重要語「{keyword}」を含む")

            if any(route.get("input") == user_text for route in route_items):
                score += 1
                reasons.append("AgentRouterログと一致")

            if any(learning.get("user_input") == user_text for learning in learning_items):
                score += 1
                reasons.append("学習ログと一致")

            importance = "low"
            if score >= 3:
                importance = "high"
            elif score >= 1:
                importance = "medium"

            analyzed.append(
                {
                    "time": item.get("time"),
                    "user": user_text,
                    "importance": importance,
                    "score": score,
                    "reasons": reasons,
                }
            )

        return {
            "status": "analyzed",
            "memory_count": len(memory_items),
            "learning_count": len(learning_items),
            "route_count": len(route_items),
            "items": analyzed,
        }

    def summarize(self, analysis):
        if not analysis or analysis.get("status") != "analyzed":
            return "MemoryAgentで分析できる記憶情報がありません。"

        items = analysis.get("items", [])
        if not items:
            return "分析対象の記憶はまだありません。"

        lines = []
        for item in items[-5:]:
            reasons = item.get("reasons") or ["特別な理由なし"]
            lines.append(
                f"- {item.get('time')} / importance={item.get('importance')} / "
                f"score={item.get('score')} / user={item.get('user')} / "
                f"理由: {', '.join(reasons)}"
            )

        return "MemoryAgent 記憶分析\n\n" + "\n".join(lines)