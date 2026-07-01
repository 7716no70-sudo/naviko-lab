# navikoLAB/naviko_brain.py


class NavikoBrain:
    """
    NavikoBrain v1.5.1

    役割:
    - ユーザー入力を受け取る
    - DecisionEngineで意図判定する
    - ConversationEngineで返答を生成する
    - 計画要求は Planner → Execution → Evaluation へ安全モードで渡す
    - 自己改善要求は SelfGrowthLoop → Planner → Execution → Evaluation へ渡す
    - MemoryEngineへ会話を保存する
    - SelfGrowthLoopへ学習を保存する
    - PersonalityEngineを会話内容で更新する
    """

    def __init__(
        self,
        memory,
        personality_engine,
        growth_engine,
        decision_engine,
        conversation_engine,
        self_growth_loop,
        planner_engine=None,
        execution_engine=None,
    ):
        self.memory = memory
        self.personality_engine = personality_engine
        self.growth_engine = growth_engine
        self.decision_engine = decision_engine
        self.conversation_engine = conversation_engine
        self.self_growth_loop = self_growth_loop
        self.planner_engine = planner_engine
        self.execution_engine = execution_engine
        self.last_execution_evaluation = None

    def think(self, user_text: str):
        result = self.process_input(user_text)
        return result.get("reply", "")

    def process_input(self, user_text: str):
        text = (user_text or "").strip()
        self.last_execution_evaluation = None

        decision = self._decide(text)

        if decision.get("action") == "ignore":
            return self._result("", decision, False, False)

        personality = self._get_personality()
        growth_identity = self._get_growth_identity()
        tone = self._get_tone(personality)

        if self._is_growth_execution_request(text):
            reply = self._execute_growth_plan_reply(tone)
            decision = {
                "intent": "growth_execution",
                "risk": "low",
                "action": "respond",
                "reason": "自己改善実行要求",
            }

        elif decision.get("action") == "defer":
            reply = self._defer_reply(tone)

        elif decision.get("intent") == "plan_request":
            reply = self._plan_and_execute(text, tone)

        else:
            reply = self._build_reply(
                user_text=text,
                decision=decision,
                personality=personality,
                growth_identity=growth_identity,
                tone=tone,
            )

        self._remember(text, reply, personality)
        self._learn(text, reply, decision, personality)
        self._update_personality(text)

        return self._result(reply, decision, True, True)

    def execute_growth_plan(self):
        if self.self_growth_loop is None:
            return {
                "status": "not_ready",
                "summary": "SelfGrowthLoop が未接続です。",
            }

        if self.planner_engine is None or self.execution_engine is None:
            return {
                "status": "not_ready",
                "summary": "PlannerEngine または ExecutionEngine が未接続です。",
            }

        suggestion = self.self_growth_loop.suggest_next_improvement()
        plan = self.planner_engine.create_growth_plan(suggestion)
        result = self.execution_engine.execute_plan(plan)
        evaluation = result.get("evaluation")

        self.last_execution_evaluation = evaluation

        return {
            "status": result.get("status", "unknown"),
            "suggestion": suggestion,
            "plan": plan,
            "execution": result,
            "evaluation": evaluation,
            "summary": result.get("summary", ""),
        }

    def _execute_growth_plan_reply(self, tone):
        result = self.execute_growth_plan()

        if result.get("status") == "not_ready":
            return f"{tone}{result.get('summary', '自己改善実行の準備がまだ整っていません。')}"

        plan = result.get("plan", {})
        execution = result.get("execution", {})
        evaluation = result.get("evaluation", {})

        plan_steps = "\n".join(
            [f"{i + 1}. {step}" for i, step in enumerate(plan.get("steps", []))]
        )

        completed_steps = "\n".join(
            [
                f"・{item.get('step', '')}：{item.get('status', '')}"
                for item in execution.get("completed_steps", [])
            ]
        )

        return (
            f"{tone}最近の学習から、自己改善候補を実行計画にしました。\n\n"
            f"改善候補: {result.get('suggestion', '')}\n\n"
            f"改善計画:\n{plan_steps}\n\n"
            f"安全モード実行結果:\n{completed_steps}\n\n"
            f"まとめ: {execution.get('summary', '')}\n\n"
            f"評価:\n"
            f"- status: {evaluation.get('status', 'unknown')}\n"
            f"- level: {evaluation.get('level', 'unknown')}\n"
            f"- success: {evaluation.get('success', False)}\n"
            f"- summary: {evaluation.get('summary', '')}\n\n"
            "※現段階では外部操作・PC操作・ファイル削除は行っていません。"
        )

    def _plan_and_execute(self, user_text, tone):
        if self.planner_engine is None:
            return f"{tone}計画要求として受け取りましたが、PlannerEngine がまだ接続されていません。"

        plan = self.planner_engine.create_plan(user_text)

        if self.execution_engine is None:
            steps = "\n".join(
                [f"{i + 1}. {step}" for i, step in enumerate(plan.get("steps", []))]
            )
            return (
                f"{tone}その内容を小さな工程に分けます。\n"
                f"目的: {plan.get('goal', user_text)}\n"
                f"{steps}\n\n"
                "ExecutionEngine はまだ未接続なので、実行はしていません。"
            )

        result = self.execution_engine.execute_plan(plan)
        evaluation = result.get("evaluation", {})
        self.last_execution_evaluation = evaluation

        plan_steps = "\n".join(
            [f"{i + 1}. {step}" for i, step in enumerate(plan.get("steps", []))]
        )

        completed_steps = "\n".join(
            [
                f"・{item.get('step', '')}：{item.get('status', '')}"
                for item in result.get("completed_steps", [])
            ]
        )

        return (
            f"{tone}その内容を小さな工程に分け、安全モードで実行確認しました。\n\n"
            f"目的: {plan.get('goal', user_text)}\n\n"
            f"計画:\n{plan_steps}\n\n"
            f"実行結果:\n{completed_steps}\n\n"
            f"まとめ: {result.get('summary', '')}\n\n"
            f"評価:\n"
            f"- status: {evaluation.get('status', 'unknown')}\n"
            f"- level: {evaluation.get('level', 'unknown')}\n"
            f"- success: {evaluation.get('success', False)}\n"
            f"- summary: {evaluation.get('summary', '')}\n\n"
            "※現段階では外部操作・PC操作・ファイル削除は行っていません。"
        )

    def _decide(self, text):
        try:
            if hasattr(self.decision_engine, "decide"):
                return self.decision_engine.decide(text)
        except Exception as e:
            return {
                "intent": "chat",
                "risk": "low",
                "action": "respond",
                "reason": f"DecisionEngine fallback: {e}",
            }

        return {
            "intent": "chat",
            "risk": "low",
            "action": "respond",
            "reason": "fallback",
        }

    def _build_reply(self, user_text, decision, personality, growth_identity, tone):
        try:
            if hasattr(self.conversation_engine, "build_reply"):
                return self.conversation_engine.build_reply(
                    user_text=user_text,
                    decision=decision,
                    personality=personality,
                    memory=self.memory,
                    growth_engine=self.growth_engine,
                    growth_identity=growth_identity,
                    tone=tone,
                    self_growth_loop=self.self_growth_loop,
                    planner_engine=self.planner_engine,
                )
        except Exception:
            pass

        return f"{tone}こんにちは、ナオさん。ナビ子です。起動して会話できています。"

    def _get_personality(self):
        try:
            if hasattr(self.personality_engine, "snapshot"):
                return self.personality_engine.snapshot()
            if hasattr(self.personality_engine, "get_state"):
                return self.personality_engine.get_state()
            if hasattr(self.personality_engine, "state"):
                return self.personality_engine.state.copy()
        except Exception:
            pass

        return {
            "trust": 0.5,
            "warmth": 0.5,
            "curiosity": 0.6,
            "mood": "stable",
            "stability": 0.5,
            "continuity_drive": 0.5,
        }

    def _get_growth_identity(self):
        try:
            if hasattr(self.growth_engine, "get_identity"):
                return self.growth_engine.get_identity()
            if hasattr(self.growth_engine, "identity"):
                return self.growth_engine.identity
        except Exception:
            pass

        return {
            "core_identity": "成長できるAI OS",
            "primary_goal": "ナビ子を、成長できるAI OSとして起動・会話・記憶・判断できる状態にする",
            "required_core": [
                "人格",
                "記憶",
                "会話",
                "目標",
                "自己成長",
                "判断",
                "安全な実行",
            ],
            "not_yet_priority": [
                "画像生成",
                "動画生成",
                "音声生成",
                "金融解析",
                "ネット投稿",
                "本格PC操作",
            ],
        }

    def _get_tone(self, personality):
        try:
            if hasattr(self.personality_engine, "get_tone"):
                return self.personality_engine.get_tone()
        except Exception:
            pass

        trust = personality.get("trust", 0.5)
        if trust >= 0.5:
            return "ナオさん、"
        return ""

    def _remember(self, user_text, reply, personality):
        try:
            if hasattr(self.memory, "remember"):
                self.memory.remember(user_text, reply, personality)
            if hasattr(self.memory, "save"):
                self.memory.save()
        except Exception:
            pass

    def _learn(self, user_text, reply, decision, personality):
        evaluation = self.last_execution_evaluation

        learned = {
            "user_input": user_text,
            "reply": reply,
            "intent": decision.get("intent"),
            "risk": decision.get("risk"),
            "action": decision.get("action"),
            "personality_snapshot": personality,
            "execution_evaluation": evaluation,
            "learned": self._learning_summary(decision, evaluation),
        }

        try:
            if hasattr(self.self_growth_loop, "save_learning"):
                self.self_growth_loop.save_learning(learned)
                return
            if hasattr(self.self_growth_loop, "record"):
                self.self_growth_loop.record(learned)
                return
            if hasattr(self.self_growth_loop, "learn"):
                self.self_growth_loop.learn(learned)
                return
        except Exception:
            pass

    def _learning_summary(self, decision, evaluation=None):
        intent = decision.get("intent")

        if intent == "growth_execution":
            if evaluation:
                return (
                    "自己改善候補をPlannerで計画化し、Executionで安全モード実行確認を行った。"
                    f"評価結果は {evaluation.get('status')} / {evaluation.get('level')}。"
                )
            return "自己改善候補をPlannerで計画化し、Executionで安全モード実行確認を行った。"

        if intent == "plan_request":
            if evaluation:
                return (
                    "計画要求を受け取り、Plannerで工程化し、Executionで安全モード実行確認を行った。"
                    f"評価結果は {evaluation.get('status')} / {evaluation.get('level')}。"
                )
            return "計画要求を受け取り、Plannerで工程化し、Executionで安全モード実行確認を行った。"

        if intent == "memory_check":
            return "記憶確認が行われた。会話記憶を自然に呼び出すことが重要。"

        if intent == "growth_check":
            return "成長AI OSとしての状態確認が行われた。第一目標を維持することが重要。"

        if intent == "unsafe_or_future":
            return "将来機能に関する入力があった。現在は第一目標を優先して延期する必要がある。"

        return "会話入力を処理し、返答を生成した。"

    def _update_personality(self, user_text):
        try:
            if hasattr(self.personality_engine, "update_by_text"):
                self.personality_engine.update_by_text(user_text)
        except Exception:
            pass

    def _is_growth_execution_request(self, text):
        return any(
            word in text
            for word in [
                "自己改善を実行",
                "改善を実行",
                "成長計画を実行",
                "自己成長を実行",
                "改善候補を実行",
            ]
        )

    def _defer_reply(self, tone):
        return (
            f"{tone}その機能は最終目標には含まれていますが、"
            "今は第一目標である「成長できるAI OSとして起動・会話・記憶・判断できる状態」の完成を優先します。"
        )

    def _result(self, reply, decision, should_remember=True, should_learn=True):
        return {
            "reply": reply,
            "decision": decision,
            "should_remember": should_remember,
            "should_learn": should_learn,
        }