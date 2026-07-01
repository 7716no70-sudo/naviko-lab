from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class AppOperatorConnector:
    """
    アプリ操作能力の mock Connector。
    現段階では実際のPC操作は行わず、目的に対する操作計画だけを生成する。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.log_dir = self.root_dir / "navikoLAB" / "connectors" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def run(self, goal: str, context: dict | None = None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")

        result = {
            "connector": "app_operator",
            "status": "completed",
            "mode": "mock",
            "goal": goal,
            "created_at": now,
            "content": f"{goal} のために必要なアプリ操作手順案を作成しました。",
            "operation_plan": [
                "対象アプリを特定する",
                "必要な画面・入力欄・ボタンを確認する",
                "安全な操作手順を作成する",
                "実行前にユーザー確認を行う",
                "mock段階では実操作せず、計画のみ出力する",
            ],
            "context": context or {},
        }

        log_path = self.log_dir / f"app_operator_connector_{now}.json"
        log_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        result["log_file"] = str(log_path)

        return result


def main() -> None:
    connector = AppOperatorConnector()
    result = connector.run("TODOアプリを作りたい")

    print("=== AppOperatorConnector mock 診断 ===")
    print(f"状態: {result['status']}")
    print(f"モード: {result['mode']}")
    print(f"内容: {result['content']}")
    print(f"保存先: {result['log_file']}")
    print("操作計画:")
    for step in result["operation_plan"]:
        print(f"- {step}")


if __name__ == "__main__":
    main()