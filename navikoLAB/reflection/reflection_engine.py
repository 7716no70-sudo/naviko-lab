# navikoLAB/reflection/reflection_engine.py

from datetime import datetime


class ReflectionEngine:
    """
    ReflectionEngine v1.0

    役割:
    - Execution評価結果をもとに自己評価する
    - 成功点・注意点・次の改善方針を整理する
    - 自己改善ループの判断材料を作る
    """

    def reflect_execution(self, execution_result):
        evaluation = execution_result.get("evaluation", {}) if execution_result else {}

        status = evaluation.get("status", "unknown")
        level = evaluation.get("level", "unknown")
        success = evaluation.get("success", False)
        summary = evaluation.get("summary", "")

        if success and level == "safe":
            reflection = {
                "status": "reflected",
                "time": datetime.now().isoformat(timespec="seconds"),
                "result_type": "safe_success",
                "success_point": "安全モードで計画の全工程を完了できた。",
                "concern": "現在は安全モードの確認のみで、実作業はまだ行っていない。",
                "next_improvement": "成功理由と評価理由をより詳しく記録し、次回の計画精度を高める。",
                "source_evaluation": {
                    "status": status,
                    "level": level,
                    "success": success,
                    "summary": summary,
                },
            }
            return reflection

        if level == "warning":
            return {
                "status": "reflected",
                "time": datetime.now().isoformat(timespec="seconds"),
                "result_type": "warning",
                "success_point": "実行結果を評価できた。",
                "concern": "一部の工程に注意が必要。",
                "next_improvement": "注意が出た工程を分析し、計画分解と安全判断を強化する。",
                "source_evaluation": {
                    "status": status,
                    "level": level,
                    "success": success,
                    "summary": summary,
                },
            }

        if level == "danger":
            return {
                "status": "reflected",
                "time": datetime.now().isoformat(timespec="seconds"),
                "result_type": "danger",
                "success_point": "危険評価を検出できた。",
                "concern": "安全上の問題があるため、実行を進めてはいけない。",
                "next_improvement": "危険条件を記録し、停止条件と人間承認ゲートを強化する。",
                "source_evaluation": {
                    "status": status,
                    "level": level,
                    "success": success,
                    "summary": summary,
                },
            }

        return {
            "status": "reflected",
            "time": datetime.now().isoformat(timespec="seconds"),
            "result_type": "unknown",
            "success_point": "実行結果を受け取った。",
            "concern": "評価内容が十分ではない。",
            "next_improvement": "ExecutionEvaluator の評価粒度を高める。",
            "source_evaluation": {
                "status": status,
                "level": level,
                "success": success,
                "summary": summary,
            },
        }