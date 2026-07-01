# navikoLAB/evaluation/execution_evaluator.py


class ExecutionEvaluator:
    """
    ExecutionEvaluator v1.0

    役割:
    - ExecutionEngine の結果を評価する
    - 安全モード実行が正常に終わったか確認する
    - 次の改善につなげる評価メモを作る
    """

    def evaluate(self, execution_result):
        if not execution_result:
            return {
                "status": "no_result",
                "success": False,
                "level": "warning",
                "summary": "評価できる実行結果がありません。",
            }

        status = execution_result.get("status")
        safe_mode = execution_result.get("safe_mode", True)
        completed_steps = execution_result.get("completed_steps", [])

        if status != "completed":
            return {
                "status": "not_completed",
                "success": False,
                "level": "warning",
                "summary": "実行は完了していません。",
            }

        if not safe_mode:
            return {
                "status": "unsafe_mode",
                "success": False,
                "level": "danger",
                "summary": "安全モード外の実行結果です。確認が必要です。",
            }

        if not completed_steps:
            return {
                "status": "no_steps",
                "success": False,
                "level": "warning",
                "summary": "完了した工程がありません。",
            }

        failed_steps = [
            step for step in completed_steps
            if step.get("status") not in ["completed", "simulated_completed"]
        ]

        if failed_steps:
            return {
                "status": "partial",
                "success": False,
                "level": "warning",
                "summary": f"{len(failed_steps)}件の工程に注意が必要です。",
            }

        return {
            "status": "success",
            "success": True,
            "level": "safe",
            "summary": f"{len(completed_steps)}件の工程が安全モードで正常に完了しました。",
        }