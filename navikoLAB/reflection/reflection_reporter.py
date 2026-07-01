# navikoLAB/reflection/reflection_reporter.py

import json
from pathlib import Path
from datetime import datetime


class ReflectionReporter:
    """
    ReflectionReporter v1.0

    役割:
    - ReflectionEngine の内省結果を保存する
    - 後から自己改善履歴として確認できるようにする
    """

    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.report_dir = self.base_dir / "reflection" / "reflection_reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def save_reflection(self, reflection):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.report_dir / f"reflection_{now}.json"

        report = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "reflection": reflection,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return {
            "status": "saved",
            "path": str(path),
            "reflection": reflection,
        }