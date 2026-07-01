import json
import urllib.request
import urllib.error

try:
    from .api_key_manager import get_api_key
    from .base_ai_connector import BaseAIConnector
except ImportError:
    from api_key_manager import get_api_key
    from base_ai_connector import BaseAIConnector


DEFAULT_MODEL = "grok-4.3"


class GrokConnector(BaseAIConnector):
    connector_name = "grok"
    default_model = DEFAULT_MODEL
    provider_key = "XAI_API_KEY"

    def __init__(self, model=None):
        super().__init__(model=model, api_key=get_api_key("grok"))
        self.api_url = "https://api.x.ai/v1/chat/completions"

    def build_payload(self, prompt, system_message=None):
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_message or "あなたはナビ子LABの安全なGrok Connectorです。",
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
            result = self.skipped_result("XAI_API_KEY is not configured.")
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

            result = self.completed_result(output)

        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8")
            except Exception:
                error_body = ""

            result = self.failed_result(
                e,
                error_type="HTTPError",
                extra={"error_body": error_body[:1000]},
            )

        except Exception as e:
            result = self.failed_result(e)

        self.write_log(prompt, result)
        return result


def run_grok_connector(prompt, system_message=None):
    connector = GrokConnector()
    return connector.run(prompt, system_message)


def main():
    print("=== Grok Connector 動作確認 ===")

    result = run_grok_connector(
        "ナビ子LABのGrok Connector接続テストです。短く返答してください。"
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