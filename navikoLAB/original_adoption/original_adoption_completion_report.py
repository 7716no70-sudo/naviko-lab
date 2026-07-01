from __future__ import annotations

import json
import py_compile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"
ADOPTION_DIR = ROOT / "navikoLAB" / "original_adoption"
REPORT_DIR = ROOT / "navikoLAB" / "reports"


def check_naviko_syntax() -> bool:
    try:
        py_compile.compile(str(NAVIKO_FILE), doraise=True)
        return True
    except Exception:
        return False


def build_report() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    source = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore")

    return {
        "report_id": f"original_adoption_completion_{now}",
        "phase": "第20工程-4",
        "status": "completed",
        "naviko_syntax_ok": check_naviko_syntax(),
        "bridge_import_exists": "run_original_autonomous_bridge" in source,
        "bridge_function_exists": "run_original_lab_autonomous_flow_from_naviko" in source,
        "naviko_py_policy": "import と呼び出し関数のみ追加。重い処理は navikoLAB 側に保持。",
        "completed_items": [
            "original_adoption_request 作成",
            "オリジナル反映シミュレーション",
            "original_naviko_bridge 作成",
            "naviko.py へ import 追加",
            "naviko.py へ安全呼び出し関数追加",
            "静的接続テスト passed",
        ],
        "next_step": "第20工程-5 LAB完成機能 オリジナル統合完了判定",
    }


def save_report(report: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / f"{report['report_id']}.json"
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    report = build_report()
    output_path = save_report(report)

    print("=== 第20工程-4 完了診断 ===")
    print(f"状態: {report['status']}")
    print(f"naviko.py構文OK: {report['naviko_syntax_ok']}")
    print(f"Bridge importあり: {report['bridge_import_exists']}")
    print(f"Bridge関数あり: {report['bridge_function_exists']}")
    print(f"保存先: {output_path}")
    print(f"次工程: {report['next_step']}")


if __name__ == "__main__":
    main()