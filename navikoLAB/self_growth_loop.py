# navikoLAB/self_growth_loop.py

import json
from pathlib import Path
from datetime import datetime


class SelfGrowthLoop:
    """
    SelfGrowthLoop v3.1

    役割:
    - 会話結果を学習ログとして保存する
    - 最近の学習を返す
    - Execution評価から改善候補を考える
    - AgentRouter分析から改善候補を考える
    """

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.growth_dir = self.base_dir / "growth_logs"
        self.growth_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = self.growth_dir / "self_growth_log.json"

    def load_json(self, path, default):
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
        except Exception:
            return default
        return default

    def save_json(self, path, data):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_learning(self, learning):
        logs = self.load_json(self.log_path, [])

        if "time" not in learning:
            learning["time"] = datetime.now().isoformat(timespec="seconds")

        if "learned" not in learning:
            learning["learned"] = self.build_learning_note(
                {
                    "intent": learning.get("intent"),
                    "risk": learning.get("risk"),
                    "action": learning.get("action"),
                }
            )

        logs.append(learning)

        if len(logs) > 100:
            logs = logs[-100:]

        self.save_json(self.log_path, logs)
        return learning

    def reflect_conversation(self, user_text, reply, decision, personality):
        learning = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "input": user_text,
            "reply": reply,
            "intent": decision.get("intent"),
            "risk": decision.get("risk"),
            "action": decision.get("action"),
            "personality_snapshot": personality.copy(),
            "learned": self.build_learning_note(decision),
        }
        return self.save_learning(learning)

    def recent_learnings(self, limit=5):
        logs = self.load_json(self.log_path, [])
        return logs[-limit:]

    def suggest_next_improvement(self, route_analysis=None):
        logs = self.recent_learnings(10)

        route_suggestion = self._suggest_from_route_analysis(route_analysis)
        if route_suggestion:
            return route_suggestion

        if not logs:
            return "学習ログがまだ少ないため、会話・記憶・判断の安定化を続ける"

        evaluation_suggestion = self._suggest_from_execution_evaluation(logs)
        if evaluation_suggestion:
            return evaluation_suggestion

        intents = [item.get("intent") for item in logs]

        if intents.count("unsafe_or_future") >= 2:
            return "将来機能の要求を安全に延期し、現在の第一目標へ戻す判断を強化する"

        if intents.count("growth_execution") >= 2:
            return "自己改善の実行結果を評価し、改善計画の質を高める"

        if intents.count("growth_check") >= 2:
            return "成長状態確認から、次の自己改善工程をより具体的に提案できるようにする"

        if intents.count("memory_check") >= 2:
            return "会話記憶と学習ログの連携を強化し、記憶確認を自然にする"

        if intents.count("plan_request") >= 2:
            return "計画要求を小さな工程に分解し、安全実行へつなげる力を高める"

        return "通常会話から、ナオさんとの関係性と会話継続の安定性を高める"

    def _suggest_from_route_analysis(self, route_analysis):
        if not isinstance(route_analysis, dict):
            return None

        if route_analysis.get("external_ai_used") is True:
            return "外部AI使用が検出されたため、安全確認と人間承認ゲートを強化する"

        if route_analysis.get("real_pc_operation_used") is True:
            return "実PC操作が検出されたため、実行権限と安全停止条件を最優先で確認する"

        if route_analysis.get("all_safe_mode") is False:
            return "安全モード外のルートが検出されたため、AgentRouterの安全判定を強化する"

        most_used = route_analysis.get("most_used_agent")

        if most_used == "memory":
            return "MemoryAgentの使用が多いため、会話記憶と学習ログの連携を強化する"

        if most_used == "planner":
            return "PlannerAgentの使用が多いため、計画分解とExecution接続の安定性を高める"

        if most_used == "growth":
            return "GrowthAgentの使用が多いため、自己改善候補の具体性を高める"

        if most_used == "reflection":
            return "ReflectionAgentの使用が多いため、内省結果を次の改善計画へ反映しやすくする"

        if most_used == "execution":
            return "ExecutionAgentの使用が多いため、実行評価と安全確認の精度を高める"

        return None

    def _suggest_from_execution_evaluation(self, logs):
        evaluations = []

        for item in logs:
            evaluation = item.get("execution_evaluation")
            if isinstance(evaluation, dict):
                evaluations.append(evaluation)

        if not evaluations:
            return None

        danger_count = sum(1 for e in evaluations if e.get("level") == "danger")
        warning_count = sum(1 for e in evaluations if e.get("level") == "warning")
        success_count = sum(1 for e in evaluations if e.get("success") is True)
        safe_count = sum(1 for e in evaluations if e.get("level") == "safe")

        if danger_count > 0:
            return "危険評価が出た実行結果を優先確認し、安全判定と停止条件を強化する"

        if warning_count >= 2:
            return "注意評価が続いているため、Executionの失敗理由を分析し、計画の安全確認を強化する"

        if success_count >= 3 and safe_count >= 3:
            return "安全実行が安定しているため、次は実行結果の評価理由をより詳しく記録できるようにする"

        if success_count >= 1:
            return "安全実行の成功結果をもとに、PlannerとExecutionの連携をさらに安定化する"

        return None

    def build_learning_note(self, decision):
        intent = decision.get("intent")

        if intent == "memory_check":
            return "記憶確認が行われた。会話記憶を自然に呼び出せることが重要。"

        if intent == "growth_check":
            return "成長AI OSとしての状態確認が行われた。目標をぶらさず維持することが重要。"

        if intent == "growth_execution":
            return "自己改善候補が実行された。評価結果を次の改善に反映することが重要。"

        if intent == "plan_request":
            return "計画や実装に関する入力があった。工程を小さく分け、安全に進める必要がある。"

        if intent == "unsafe_or_future":
            return "将来機能に関する入力があった。現在は第一目標を優先して延期する必要がある。"

        return "通常会話が行われた。関係性と会話継続の安定性が重要。"