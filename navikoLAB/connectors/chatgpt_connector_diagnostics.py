import os
from pathlib import Path

from navikoLAB.connectors.chatgpt_connector import ChatGPTConnector
from navikoLAB.connectors.connector_dispatcher import ConnectorDispatcher


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"


def diagnose_chatgpt_connector():
    connector = ChatGPTConnector()
    dispatcher = ConnectorDispatcher(root_dir=ROOT)

    api_key_exists = bool(os.environ.get("OPENAI_API_KEY"))

    direct_result = connector.run(
        "ChatGPT Connector direct diagnostics test. Reply briefly in Japanese."
    )

    dispatcher_result = dispatcher.run(
        "chatgpt",
        "ChatGPT Connector dispatcher diagnostics test.",
        context={"source": "chatgpt_connector_diagnostics"},
    )

    return {
        "connector": "chatgpt",
        "api_key_exists": api_key_exists,
        "model": connector.model,
        "direct_status": direct_result.get("status"),
        "direct_reason": direct_result.get("reason"),
        "direct_error": direct_result.get("error"),
        "dispatcher_status": dispatcher_result.get("status"),
        "dispatcher_reason": dispatcher_result.get("reason"),
        "dispatcher_error": dispatcher_result.get("error"),
        "dispatcher_log": dispatcher_result.get("dispatcher_log"),
    }


def main():
    result = diagnose_chatgpt_connector()

    print("=== ChatGPT Connector 正式利用診断 ===")
    print(f"connector: {result['connector']}")
    print(f"OPENAI_API_KEY: {'あり' if result['api_key_exists'] else 'なし'}")
    print(f"model: {result['model']}")
    print("---------------")
    print(f"direct_status: {result['direct_status']}")

    if result.get("direct_reason"):
        print(f"direct_reason: {result['direct_reason']}")

    if result.get("direct_error"):
        print(f"direct_error: {result['direct_error']}")

    print("---------------")
    print(f"dispatcher_status: {result['dispatcher_status']}")

    if result.get("dispatcher_reason"):
        print(f"dispatcher_reason: {result['dispatcher_reason']}")

    if result.get("dispatcher_error"):
        print(f"dispatcher_error: {result['dispatcher_error']}")

    print(f"dispatcher_log: {result['dispatcher_log']}")

    print("---------------")

    if result["api_key_exists"] and result["dispatcher_status"] == "completed":
        print("診断結果: api_ready")
    elif not result["api_key_exists"] and result["dispatcher_status"] == "skipped":
        print("診断結果: safe_skipped")
    else:
        print("診断結果: warning")


if __name__ == "__main__":
    main()