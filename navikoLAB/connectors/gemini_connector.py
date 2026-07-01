import json
import urllib.request
import urllib.error

try:
    from .api_key_manager import get_api_key
    from .base_ai_connector import BaseAIConnector
except ImportError:
    from api_key_manager import get_api_key
    from base_ai_connector import BaseAIConnector


DEFAULT_MODEL = "gemini-2.5-flash"


class GeminiConnector(BaseAIConnector):
    connector_name = "gemini"
    default_model = DEFAULT_MODEL
    provider_key = "GEMINI_API_KEY"

    def __init__(self, model=None):
        super().__init__(model=model, api_key=get_api_key("gemini"))
        self.api_url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent"
        )

    def build_payload(self, prompt, system_message=None):
        text = str(prompt)
        if system_message:
            text = f"{system_message}\n\n{text}"

        return {
            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1024
            }
        }

    def run(self, prompt, system_message=None):
        if not self.is_available():
            result = self.skipped_result("GEMINI_API_KEY is not configured.")
            self.write_log(prompt, result)
            return result

        payload = self.build_payload(prompt, system_message)

        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read().decode("utf-8")
                data = json.loads(raw)

            output_parts = []
            for candidate in data.get("candidates", []):
                content = candidate.get("content", {})
                for part in content.get("parts", []):
                    if "text" in part:
                        output_parts.append(part.get("text", ""))

            result = self.completed_result("\n".join(output_parts).strip())

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


def run_gemini_connector(prompt, system_message=None):
    connector = GeminiConnector()
    return connector.run(prompt, system_message)


def main():
    print("=== Gemini Connector 動作確認 ===")

    result = run_gemini_connector(
        "ナビ子LABのGemini Connector接続テストです。短く返答してください。"
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