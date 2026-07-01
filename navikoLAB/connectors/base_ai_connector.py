from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

LOG_DIR = LAB_ROOT / "connectors" / "logs"


class BaseAIConnector:
    connector_name = "base_ai"
    default_model = ""
    provider_key = ""

    def __init__(self, model=None, api_key=None):
        self.model = model or self.default_model
        self.api_key = api_key
        self.log_file = LOG_DIR / f"{self.connector_name}_connector_log.jsonl"

    def is_available(self):
        return bool(self.api_key)

    def skipped_result(self, reason=None):
        return {
            "connector": self.connector_name,
            "status": "skipped",
            "reason": reason or f"{self.provider_key} API key is not configured.",
            "output": "",
        }

    def completed_result(self, output, extra=None):
        result = {
            "connector": self.connector_name,
            "status": "completed",
            "model": self.model,
            "output": output,
        }

        if extra:
            result.update(extra)

        return result

    def failed_result(self, error, error_type=None, extra=None):
        result = {
            "connector": self.connector_name,
            "status": "failed",
            "error_type": error_type or type(error).__name__,
            "error": str(error),
            "output": "",
        }

        if extra:
            result.update(extra)

        return result

    def write_log(self, prompt, result):
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "connector": self.connector_name,
            "prompt_preview": str(prompt)[:300],
            "result": result,
        }

        with self.log_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")