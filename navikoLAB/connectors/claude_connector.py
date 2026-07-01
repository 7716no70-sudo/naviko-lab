import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

try:
    from .api_key_manager import get_api_key
except ImportError:
    from api_key_manager import get_api_key


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

LOG_DIR = LAB_ROOT / "connectors" / "logs"
LOG_FILE = LOG_DIR / "claude_connector_log.jsonl"

ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_MODEL = "claude-3-5-haiku-latest"


class ClaudeConnector:
    def __init__(self, model=None):
        self.model = model or DEFAULT_MODEL
        self.api_key = get_api_key("claude")
        self.api_url = "https://api.anthropic.com/v1/messages"

    def is_available(self):
        return bool(self.api_key)

    def build_payload(self, prompt, system_message=None):
        return {
            "model": self.model,
            "max_tokens": 1024,
            "temperature": 0.3,
            "system": system_message or "あなたはナビ子LABの安全なClaude Connectorです。",
            "messages": [
                {
                    "role": "user",
                    "content": str(prompt),
                }
            ],
        }

    def run(self, prompt, system_message=None):
        if not self.is_available():
            result = {
                "connector": "claude",
                "status": "skipped",
                "reason": "ANTHROPIC_API_KEY is not configured.",
                "output": "",
            }
            self.write_log(prompt, result)
            return result

        payload = self.build_payload(prompt, system_message)

        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": ANTHROPIC_VERSION,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)

            output_parts = []
            for item in data.get("content", []):
                if item.get("type") == "text":
                    output_parts.append(item.get("text", ""))

            result = {
                "connector": "claude",
                "status": "completed",
                "model": self.model,
                "output": "\n".join(output_parts).strip(),
            }

        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                error_body = ""

            result = {
                "connector": "claude",
                "status": "failed",
                "error_type": "HTTPError",
                "error": str(e),
                "error_body": error_body[:1000],
                "output": "",
            }

        except Exception as e:
            result = {
                "connector": "claude",
                "status": "failed",
                "error_type": type(e).__name__,
                "error": str(e),
                "output": "",
            }

        self.write_log(prompt, result)
        return result

    def write_log(self, prompt, result):
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt_preview": str(prompt)[:300],
            "result": result,
        }

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def run_claude_connector(prompt, system_message=None):
    connector = ClaudeConnector()
    return connector.run(prompt, system_message)


def main():
    print("=== Claude Connector 動作確認 ===")

    result = run_claude_connector(
        "ナビ子LABのClaude Connector接続テストです。短く返答してください。"
    )

    print(f"status: {result.get('status')}")
    print(f"connector: {result.get('connector')}")

    if result.get("reason"):
        print(f"reason: {result.get('reason')}")

    if result.get("error"):
        print(f"error: {result.get('error')}")

    output = result.get("output", "")
    if output:
        print("output:")
        print(output[:500])


if __name__ == "__main__":
    main()