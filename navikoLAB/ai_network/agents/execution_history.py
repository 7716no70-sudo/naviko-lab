import json
import time
from pathlib import Path


class ExecutionHistory:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.exec_dir = self.root_dir / "agent_executions"
        self.exec_dir.mkdir(parents=True, exist_ok=True)

    def save(self, execution_result):
        exec_file = (
            self.exec_dir
            / f"agent_execution_{time.strftime('%Y%m%d_%H%M%S')}.json"
        )

        data = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "execution_result": execution_result
        }

        with open(exec_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return exec_file

    def list_recent(self, limit=10):
        files = sorted(
            self.exec_dir.glob("*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        histories = []

        for file in files[:limit]:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                histories.append({
                    "file": file.name,
                    "data": data
                })
            except Exception as e:
                histories.append({
                    "file": file.name,
                    "error": str(e)
                })

        return histories