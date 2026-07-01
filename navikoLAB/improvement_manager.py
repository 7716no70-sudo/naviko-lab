import json
import time
from pathlib import Path


class ImprovementManager:
    def __init__(self, lab_dir):
        self.lab_dir = Path(lab_dir)
        self.improvement_dir = self.lab_dir / "improvements"
        self.history_dir = self.lab_dir / "improvement_history"

        self.improvement_dir.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def load_json(self, path, default):
        path = Path(path)

        if not path.exists():
            return default

        try:
            return json.loads(
                path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            )
        except Exception:
            return default

    def save_json(self, path, data):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def load_latest_improvement_request(self):
        files = sorted(
            self.improvement_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if not files:
            return None, None

        latest = files[0]
        data = self.load_json(latest, {})

        return data, latest

    def format_improvement_prompt(self, request):
        if not request:
            return ""

        items = request.get("improvement_requests", [])

        if not items:
            return ""

        lines = []
        lines.append("")
        lines.append("【前回Reflectionからの改善要求】")

        for item in items:
            lines.append(f"- {item}")

        return "\n".join(lines)

    def save_improvement_build_history(
        self,
        purpose,
        improved_purpose,
        request_file,
        build_result
    ):
        history_file = (
            self.history_dir
            / f"improvement_build_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )

        data = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "purpose": purpose,
            "improved_purpose": improved_purpose,
            "request_file": str(request_file) if request_file else "",
            "build_result": build_result,
            "status": build_result.get("status", "unknown")
        }

        self.save_json(history_file, data)

        return history_file

    def diagnose(self):
        requests = list(self.improvement_dir.glob("*.json"))
        histories = list(self.history_dir.glob("*.json"))

        return {
            "improvement_request_count": len(requests),
            "improvement_build_history_count": len(histories),
            "status": "ok"
        }