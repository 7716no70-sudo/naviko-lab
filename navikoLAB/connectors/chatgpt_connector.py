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
LOG_FILE = LOG_DIR / "chatgpt_connector_log.jsonl"

DEFAULT_MODEL = "gpt-4o-mini"


class ChatGPTConnector:
    def __init__(self, model=None):
        self.model = model or DEFAULT_MODEL
        self.api_key = get_api_key("chatgpt")
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def is_available(self):
        return bool(self.api_key)

    def build_payload(self, prompt, system_message=None):
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_message or "あなたはナビ子LABの安全なChatGPT Connectorです。",
                },
                {
                    "role": "user",
                    "content": str(prompt),
                },
            ],
            "temperature": 0.3,
        }

    def run(self, prompt, system_message=None):
        if not self.is_available():
            result = {
                "connector": "chatgpt",
                "status": "skipped",
                "reason": "OPENAI_API_KEY is not configured.",
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
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)

            output = (
                data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            result = {
                "connector": "chatgpt",
                "status": "completed",
                "model": self.model,
                "output": output,
            }

        except urllib.error.HTTPError as e:
            result = {
                "connector": "chatgpt",
                "status": "failed",
                "error_type": "HTTPError",
                "error": str(e),
                "output": "",
            }

        except Exception as e:
            result = {
                "connector": "chatgpt",
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


def run_chatgpt_connector(prompt, system_message=None):
    connector = ChatGPTConnector()
    return connector.run(prompt, system_message)


def main():
    print("=== ChatGPT Connector 動作確認 ===")

    result = run_chatgpt_connector(
        "ナビ子LABのChatGPT Connector接続テストです。短く返答してください。"
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