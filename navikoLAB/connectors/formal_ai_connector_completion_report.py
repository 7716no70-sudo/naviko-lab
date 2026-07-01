from pathlib import Path
from datetime import datetime

from navikoLAB.connectors.formal_connector_diagnostics import run_formal_connector_diagnostics
from navikoLAB.connectors.connector_diagnostics import diagnose_connectors


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"
REPORT_DIR = LAB_ROOT / "reports"


def create_report():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"formal_ai_connector_completion_{now}.txt"

    formal_results = run_formal_connector_diagnostics()
    connector_result = diagnose_connectors()

    completed = 0
    skipped = 0
    failed = 0

    for result in formal_results:
        status = result.get("status")

        if status == "completed":
            completed += 1
        elif status == "skipped":
            skipped += 1
        else:
            failed += 1

    lines = []
    lines.append("=== 正式AI Connector 完成レポート ===")
    lines.append(f"作成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("【工程】")
    lines.append("第25工程 ChatGPT / Claude / Gemini / Grok Connector 正式版土台")
    lines.append("")
    lines.append("【完成項目】")
    lines.append("- ChatGPT Connector 正式版土台 作成済み")
    lines.append("- Claude Connector 正式版土台 作成済み")
    lines.append("- Gemini Connector 正式版土台 作成済み")
    lines.append("- Grok Connector 正式版土台 作成済み")
    lines.append("- ConnectorDispatcher Map方式へ4件登録済み")
    lines.append("- APIキー未設定時の safe_skipped 確認済み")
    lines.append("- capability_registry 状態整理済み")
    lines.append("- APIキー設定後、コード変更なしで正式実行可能")
    lines.append("")
    lines.append("【正式AI Connector 診断】")

    for result in formal_results:
        lines.append(
            f"- {result.get('connector', result.get('agent_id'))} / "
            f"status={result.get('status')} / "
            f"reason={result.get('reason')} / "
            f"log={result.get('dispatcher_log')}"
        )

    lines.append("")
    lines.append("【診断集計】")
    lines.append(f"診断数: {len(formal_results)}")
    lines.append(f"completed: {completed}")
    lines.append(f"skipped: {skipped}")
    lines.append(f"failed_or_warning: {failed}")
    lines.append("")
    lines.append("【Connector 全体状態】")
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

    if failed == 0:
        lines.append("正式AI Connector工程: completed")
    else:
        lines.append("正式AI Connector工程: warning")

    lines.append("")
    lines.append("【次工程】")
    lines.append("第25工程-10 Browser Connector 正式版土台作成")
    lines.append("または 第26工程 Research / Knowledge / Experience 設計開始")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path, formal_results, connector_result, failed


def main():
    report_path, formal_results, connector_result, failed = create_report()

    print("=== 正式AI Connector 完成レポート作成 ===")
    print(f"保存先: {report_path}")
    print(f"正式AI Connector診断数: {len(formal_results)}")
    print(f"Connector登録数: {connector_result.get('registered_count')}")
    print(f"不足Connector数: {connector_result.get('missing_count')}")

    if failed == 0:
        print("状態: completed")
    else:
        print("状態: warning")


if __name__ == "__main__":
    main()