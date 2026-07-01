from __future__ import annotations

import json
import py_compile
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"
REPORT_DIR = ROOT / "navikoLAB" / "reports"


REQUIRED_MARKERS = [
    "from navikoLAB.original_adoption.mission_dashboard import open_mission_dashboard",
    "text=\"AIミッション\"",
    "open_mission_dashboard(c_win)",
]


def syntax_ok() -> bool:
    try:
        py_compile.compile(str(NAVIKO_FILE), doraise=True)
        return True
    except Exception:
        return False


def build_report() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    source = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore")

    markers = {marker: marker in source for marker in REQUIRED_MARKERS}
    completed = syntax_ok() and all(markers.values())

    return {
        "report_id": f"mission_dashboard_integration_{now}",
        "phase": "第21工程",
        "status": "completed" if completed else "failed",
        "completed": completed,
        "naviko_syntax_ok": syntax_ok(),
        "markers": markers,
        "summary": "naviko.py にAIミッションボタンを追加し、LAB側 Mission Dashboard を開く構成にした。",
        "policy": {
            "naviko_py_button_count_added": 1,
            "naviko_py_role": "Mission Dashboard を開く入口のみ",
            "heavy_logic_location": "navikoLAB/original_adoption/mission_dashboard.py",
        },
        "next_step": "第21工程-5 GUI起動確認",
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

    print("=== Mission Dashboard 統合確認 ===")
    print(f"状態: {report['status']}")
    print(f"完了: {report['completed']}")
    print(f"naviko.py構文OK: {report['naviko_syntax_ok']}")
    print("マーカー確認:")
    for marker, ok in report["markers"].items():
        print(f"- {marker}: {ok}")
    print(f"保存先: {output_path}")
    print(f"次工程: {report['next_step']}")


if __name__ == "__main__":
    main()