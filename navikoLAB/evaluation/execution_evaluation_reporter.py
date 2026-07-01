# navikoLAB/evaluation/execution_evaluation_reporter.py

import json
from pathlib import Path
from datetime import datetime


class ExecutionEvaluationReporter:
    """
    ExecutionEvaluationReporter v1.0

    役割:
    - ExecutionEngine の実行結果と評価結果を保存する
    - 後から自己改善履歴として確認できるようにする
    """

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.report_dir = self.base_dir / "evaluation" / "execution_reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def save_report(self, plan, execution_result):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.report_dir / f"execution_evaluation_{now}.json"

        report = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "plan": plan,
            "execution_result": execution_result,
            "evaluation": execution_result.get("evaluation", {}),
            "safe_mode": execution_result.get("safe_mode", True),
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return {
            "status": "saved",
            "path": str(path),
            "evaluation": report["evaluation"],
        }