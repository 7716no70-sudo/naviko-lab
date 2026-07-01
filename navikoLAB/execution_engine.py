# navikoLAB/execution_engine.py

from navikoLAB.evaluation.execution_evaluator import ExecutionEvaluator
from navikoLAB.evaluation.execution_evaluation_reporter import ExecutionEvaluationReporter
from navikoLAB.reflection.reflection_engine import ReflectionEngine
from navikoLAB.reflection.reflection_reporter import ReflectionReporter


class ExecutionEngine:
    """
    ExecutionEngine v3.2

    役割:
    - 計画を安全モードで実行する
    - 実行結果を評価する
    - 評価レポートを保存する
    - ReflectionEngineで自己評価する
    - ReflectionReporterで内省結果を保存する
    """

    def __init__(self, base_dir=None):
        self.evaluator = ExecutionEvaluator()
        self.reporter = ExecutionEvaluationReporter(base_dir) if base_dir else None
        self.reflection_engine = ReflectionEngine()
        self.reflection_reporter = ReflectionReporter(base_dir) if base_dir else None

    def execute_plan(self, plan):
        if not plan or plan.get("status") != "planned":
            result = {
                "status": "no_plan",
                "goal": "",
                "completed_steps": [],
                "summary": "実行できる計画がありません。",
                "safe_mode": True,
            }
            return self._finalize(plan, result)

        completed = []

        for step in plan.get("steps", []):
            completed.append(
                {
                    "step": step,
                    "status": "simulated_completed",
                    "note": "安全モードで確認しました。外部操作は行っていません。",
                }
            )

        result = {
            "status": "completed",
            "goal": plan.get("goal", ""),
            "completed_steps": completed,
            "summary": f"{len(completed)}件の工程を安全モードで実行確認しました。",
            "safe_mode": True,
        }

        return self._finalize(plan, result)

    def _finalize(self, plan, result):
        result["evaluation"] = self.evaluator.evaluate(result)
        result["report"] = self._save_report(plan, result)
        result["reflection"] = self.reflection_engine.reflect_execution(result)
        result["reflection_report"] = self._save_reflection(result["reflection"])
        return result

    def _save_report(self, plan, result):
        if self.reporter is None:
            return {
                "status": "not_saved",
                "reason": "ExecutionEvaluationReporter が未接続です。",
            }

        try:
            return self.reporter.save_report(plan, result)
        except Exception as e:
            return {
                "status": "error",
                "reason": str(e),
            }

    def _save_reflection(self, reflection):
        if self.reflection_reporter is None:
            return {
                "status": "not_saved",
                "reason": "ReflectionReporter が未接続です。",
            }

        try:
            return self.reflection_reporter.save_reflection(reflection)
        except Exception as e:
            return {
                "status": "error",
                "reason": str(e),
            }