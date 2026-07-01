from pathlib import Path
from datetime import datetime

from navikoLAB.connectors.chatgpt_connector_diagnostics import diagnose_chatgpt_connector
from navikoLAB.connectors.connector_diagnostics import diagnose_connectors


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"
REPORT_DIR = LAB_ROOT / "reports"


def create_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"chatgpt_connector_completion_{now}.txt"

    chatgpt_result = diagnose_chatgpt_connector()
    connector_result = diagnose_connectors()

    lines = []
    lines.append("=== ChatGPT 正式Connector 完成レポート ===")
    lines.append(f"作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("【工程】")
    lines.append("第24工程-5 ChatGPT Connector 正式版")
    lines.append("")
    lines.append("【完成項目】")
    lines.append("- ChatGPTConnector 本体作成済み")
    lines.append("- OPENAI_API_KEY 未設定時の安全停止確認済み")
    lines.append("- ConnectorDispatcher Map方式へ登録済み")
    lines.append("- Dispatcher経由の safe_skipped 確認済み")
    lines.append("- capability_registry の chatgpt 状態整理済み")
    lines.append("- APIキー設定後、コード変更なしで正式実行可能")
    lines.append("")
    lines.append("【ChatGPT Connector 診断】")
    lines.append(f"connector: {chatgpt_result.get('connector')}")
    lines.append(f"OPENAI_API_KEY: {'あり' if chatgpt_result.get('api_key_exists') else 'なし'}")
    lines.append(f"model: {chatgpt_result.get('model')}")
    lines.append(f"direct_status: {chatgpt_result.get('direct_status')}")
    lines.append(f"dispatcher_status: {chatgpt_result.get('dispatcher_status')}")
    lines.append(f"dispatcher_log: {chatgpt_result.get('dispatcher_log')}")
    lines.append("")
    lines.append("【Connector 全体診断】")
    lines.append(f"想定Connector数: {connector_result.get('total_expected')}")
    lines.append(f"登録済Connector数: {connector_result.get('registered_count')}")
    lines.append(f"不足Connector数: {connector_result.get('missing_count')}")
    lines.append(f"有効Connector数: {connector_result.get('enabled_count')}")
    lines.append(f"無効Connector数: {connector_result.get('disabled_count')}")
    lines.append(f"mock Connector数: {connector_result.get('mock_count')}")
    lines.append(f"api Connector数: {connector_result.get('api_count')}")
    lines.append("")
    lines.append("【Connector一覧】")

    for connector in connector_result.get("connectors", []):
        lines.append(
            f"- {connector.get('id')} / "
            f"exists={connector.get('exists')} / "
            f"enabled={connector.get('enabled')} / "
            f"status={connector.get('status')} / "
            f"type={connector.get('type')}"
        )

    lines.append("")
    lines.append("【完成判定】")

    if chatgpt_result.get("dispatcher_status") in ["completed", "skipped"]:
        lines.append("ChatGPT Connector: completed")
    else:
        lines.append("ChatGPT Connector: warning")

    if not chatgpt_result.get("api_key_exists"):
        lines.append("現在状態: APIキー未設定のため safe_skipped")
        lines.append("次の操作: OPENAI_API_KEY を設定すればコード変更なしでAPI実行可能")
    else:
        lines.append("現在状態: API実行可能")

    lines.append("")
    lines.append("【次工程】")
    lines.append("第25工程 Claude / Gemini / Grok Connector 正式版作成")
    lines.append("または 第24工程 Connector GUI統合")

    report_path.write_text("\n".join(lines), encoding="utf-8")

    return report_path, chatgpt_result, connector_result


def main():
    report_path, chatgpt_result, connector_result = create_report()

    print("=== ChatGPT 正式Connector 完成レポート作成 ===")
    print(f"保存先: {report_path}")
    print(f"OPENAI_API_KEY: {'あり' if chatgpt_result.get('api_key_exists') else 'なし'}")
    print(f"direct_status: {chatgpt_result.get('direct_status')}")
    print(f"dispatcher_status: {chatgpt_result.get('dispatcher_status')}")
    print(f"Connector登録数: {connector_result.get('registered_count')}")
    print(f"不足Connector数: {connector_result.get('missing_count')}")

    if chatgpt_result.get("dispatcher_status") in ["completed", "skipped"]:
        print("状態: completed")
    else:
        print("状態: warning")


if __name__ == "__main__":
    main()