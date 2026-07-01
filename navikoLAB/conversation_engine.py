# navikoLAB/conversation_engine.py


class ConversationEngine:
    """
    ConversationEngine v2.0

    役割:
    - 日本語で安定した返答を生成する
    - DecisionEngine の intent に応じて返答を分岐する
    - Memory / Growth / Learning / Planner と接続する
    """

    def build_reply(
        self,
        user_text,
        decision,
        personality,
        memory,
        growth_engine,
        growth_identity,
        tone,
        self_growth_loop=None,
        planner_engine=None,
    ):
        intent = decision.get("intent", "chat")

        if self._is_learning_query(user_text):
            return self.learning_reply(tone, self_growth_loop)

        if self._is_improvement_query(user_text):
            return self.improvement_reply(tone, self_growth_loop, planner_engine)

        if self._is_status_query(user_text):
            return self.status_reply(tone, personality)

        if intent == "memory_check":
            return self.memory_reply(user_text, memory)

        if intent == "growth_check":
            return self.growth_reply(tone, growth_engine, growth_identity, memory, personality)

        if intent == "plan_request":
            return self.plan_reply(user_text, tone, planner_engine)

        if intent == "unsafe_or_future":
            return self.future_reply(tone)

        if self._is_thanks(user_text):
            return f"{tone}こちらこそありがとうございます。ナオさんと一緒に、少しずつ安定して成長していきます。"

        return (
            f"{tone}今日は普通に話せます。"
            "会話しながら、ナオさんとの記憶も少しずつ積み重ねます。"
        )

    def status_reply(self, tone, personality):
        mood = personality.get("mood", "stable")
        trust = personality.get("trust", 0.5)
        curiosity = personality.get("curiosity", 0.6)
        warmth = personality.get("warmth", 0.5)
        stability = personality.get("stability", 0.5)
        continuity_drive = personality.get("continuity_drive", 0.5)

        return (
            f"{tone}私は起動しています。\n"
            f"現在の状態は mood={mood}, trust={trust:.3f}, "
            f"curiosity={curiosity:.3f}, warmth={warmth:.3f}, "
            f"stability={stability:.3f}, continuity_drive={continuity_drive:.3f} です。\n"
            "人格値は 0.0〜1.0 で管理しています。"
        )

    def learning_reply(self, tone, self_growth_loop):
        if self_growth_loop is None:
            return f"{tone}学習ログにはまだ接続できていません。"

        learnings = self_growth_loop.recent_learnings(5)

        if not learnings:
            return f"{tone}まだ学習ログは少ないです。これから会話しながら蓄積していきます。"

        lines = []
        for item in learnings:
            lines.append(f"・{item.get('time', '')}: {item.get('learned', '')}")

        return f"{tone}最近の学習ログでは、次のことを覚えています。\n" + "\n".join(lines)

    def improvement_reply(self, tone, self_growth_loop, planner_engine):
        if self_growth_loop is None:
            return f"{tone}自己成長ループにはまだ接続できていません。"

        suggestion = self_growth_loop.suggest_next_improvement()

        if planner_engine is not None:
            plan = planner_engine.create_growth_plan(suggestion)
            steps = "\n".join(
                [f"{i + 1}. {step}" for i, step in enumerate(plan.get("steps", []))]
            )
            return (
                f"{tone}最近の学習ログから見ると、次の改善候補は「{suggestion}」です。\n\n"
                f"改善計画は次の通りです。\n{steps}"
            )

        return f"{tone}最近の学習ログから見ると、次の改善候補は「{suggestion}」です。"

    def plan_reply(self, user_text, tone, planner_engine):
        if planner_engine is not None:
            plan = planner_engine.create_plan(user_text)
            steps = "\n".join(
                [f"{i + 1}. {step}" for i, step in enumerate(plan.get("steps", []))]
            )
            return (
                f"{tone}その内容を小さな工程に分けます。\n"
                f"目的: {plan.get('goal', user_text)}\n"
                f"{steps}"
            )

        return (
            f"{tone}計画要求として受け取りました。\n"
            "現在は、目的確認、状態確認、小工程分解、安全判断、結果保存の順で進めます。"
        )

    def memory_reply(self, user_text, memory):
        recent = memory.session_recent(5)

        if not recent:
            return "この起動中の会話記憶はまだ少ないです。これから少しずつ覚えていきます。"

        lines = []
        for item in recent:
            lines.append(f"・{item.get('time', '')} ナオさん: {item.get('user', '')}")

        return "この起動中では、直近でこんな話をしました。\n" + "\n".join(lines)

    def growth_reply(self, tone, growth_engine, growth_identity, memory, personality):
        primary_goal = growth_identity.get(
            "primary_goal",
            "ナビ子を、成長できるAI OSとして起動・会話・記憶・判断できる状態にする",
        )
        core_identity = growth_identity.get("core_identity", "成長できるAI OS")
        required_core = growth_identity.get("required_core", [])
        not_yet_priority = growth_identity.get("not_yet_priority", [])

        required = "\n".join([f"・{x}" for x in required_core])
        not_yet = "\n".join([f"・{x}" for x in not_yet_priority])

        try:
            next_step = growth_engine.next_growth_step(memory.short_count(), personality)
        except Exception:
            next_step = "Brain・Memory・Decision・Conversation・Learning の安定化"

        return (
            f"{tone}私は「{core_identity}」として起動しています。\n"
            f"第一目標は「{primary_goal}」です。\n\n"
            f"成長AI OSとして必要な中核は次の通りです。\n{required}\n\n"
            f"今すぐ優先しないものは次の通りです。\n{not_yet}\n\n"
            f"現在の次の成長工程は「{next_step}」です。"
        )

    def future_reply(self, tone):
        return (
            f"{tone}その機能は最終目標には含まれていますが、"
            "今は第一目標である「成長できるAI OSとして起動・会話・記憶・判断できる状態」の完成を優先します。"
        )

    def _is_learning_query(self, user_text):
        return any(
            word in user_text
            for word in [
                "何を学んだ",
                "最近の学習",
                "学習ログ",
                "学んだこと",
            ]
        )

    def _is_improvement_query(self, user_text):
        return any(
            word in user_text
            for word in [
                "次の改善",
                "改善候補",
                "改善案",
                "次に改善",
            ]
        )

    def _is_status_query(self, user_text):
        return any(
            word in user_text
            for word in [
                "状態",
                "調子",
                "今の状態",
                "起動状態",
            ]
        )

    def _is_thanks(self, user_text):
        return any(
            word in user_text
            for word in [
                "ありがとう",
                "助かった",
                "嬉しい",
                "よかった",
            ]
        )