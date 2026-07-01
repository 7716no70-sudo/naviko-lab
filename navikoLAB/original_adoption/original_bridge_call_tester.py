from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.original_adoption.original_naviko_bridge import run_original_autonomous_bridge


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"
TEST_LOG_DIR = ROOT / "navikoLAB" / "original_adoption" / "bridge_call_tests"


def run_test() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    source = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore")

    import_exists = (
        "from navikoLAB.original_adoption.original_naviko_bridge "
        "import run_original_autonomous_bridge"
    ) in source

    function_exists = (
        "def run_original_lab_autonomous_flow_from_naviko(user_goal):"
    ) in source

    bridge_result = run_original_autonomous_bridge("TODOアプリを作りたい")

    status = "passed" if import_exists and function_exists and bridge_result.get("status") == "bridge_ready" else "failed"

    return {
        "test_id": f"original_bridge_static_test_{now}",
        "status": status,
        "naviko_file": str(NAVIKO_FILE),
        "import_exists": import_exists,
        "function_exists": function_exists,
        "bridge_result": bridge_result,
    }


def save_result(result: dict) -> Path:
    TEST_LOG_DIR.mkdir(parents=True, exist_ok=True)
    output_path = TEST_LOG_DIR / f"{result['test_id']}.json"
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main() -> None:
    result = run_test()
    output_path = save_result(result)

    print("=== Original Bridge 静的接続テスト ===")
    print(f"状態: {result['status']}")
    print(f"importあり: {result['import_exists']}")
    print(f"呼び出し関数あり: {result['function_exists']}")
    print(f"ブリッジ状態: {result['bridge_result'].get('status')}")
    print(f"モード: {result['bridge_result'].get('mode')}")
    print(f"保存先: {output_path}")


if __name__ == "__main__":
    main()