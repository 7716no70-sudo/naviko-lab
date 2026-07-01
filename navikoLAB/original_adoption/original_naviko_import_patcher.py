from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"
BACKUP_DIR = ROOT / "navikoLAB" / "original_adoption" / "naviko_patch_backups"


IMPORT_CODE = """
# === Original Naviko LAB Bridge import ===
try:
    from navikoLAB.original_adoption.original_naviko_bridge import run_original_autonomous_bridge
except Exception:
    run_original_autonomous_bridge = None
# === Original Naviko LAB Bridge import end ===

"""


FUNCTION_CODE = """

# === Original Naviko LAB Bridge caller ===
def run_original_lab_autonomous_flow_from_naviko(user_goal):
    \"\"\"
    オリジナル naviko.py から LAB統合フローを安全に呼び出す入口。
    naviko.py 側では重い処理を持たず、LAB側ブリッジへ委譲する。
    \"\"\"

    if run_original_autonomous_bridge is None:
        return {
            "status": "bridge_import_failed",
            "message": "original_naviko_bridge を import できませんでした。",
            "user_goal": user_goal,
        }

    try:
        return run_original_autonomous_bridge(user_goal)
    except Exception as error:
        return {
            "status": "bridge_runtime_error",
            "message": str(error),
            "user_goal": user_goal,
        }
# === Original Naviko LAB Bridge caller end ===

"""


def backup_naviko() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"naviko_before_original_bridge_{now}.py"
    shutil.copy2(NAVIKO_FILE, backup_path)
    return backup_path


def patch_naviko() -> dict:
    result = {
        "status": "not_started",
        "backup": None,
        "import_inserted": False,
        "function_inserted": False,
        "syntax_ok": False,
        "errors": [],
    }

    if not NAVIKO_FILE.exists():
        result["status"] = "failed"
        result["errors"].append("naviko.py が見つかりません。")
        return result

    source = NAVIKO_FILE.read_text(encoding="utf-8", errors="ignore")

    try:
        py_compile.compile(str(NAVIKO_FILE), doraise=True)
    except Exception as error:
        result["status"] = "failed"
        result["errors"].append(f"変更前の構文チェックに失敗: {error}")
        return result

    backup_path = backup_naviko()
    result["backup"] = str(backup_path)

    if "from navikoLAB.original_adoption.original_naviko_bridge import run_original_autonomous_bridge" not in source:
        import_anchor = "import threading\n"
        if import_anchor not in source:
            result["status"] = "failed"
            result["errors"].append("import挿入位置 import threading が見つかりません。")
            return result

        source = source.replace(import_anchor, import_anchor + IMPORT_CODE, 1)
        result["import_inserted"] = True

    if "def run_original_lab_autonomous_flow_from_naviko(user_goal):" not in source:
        function_anchor = "\ndef open_custom_chat_window():"
        if function_anchor not in source:
            result["status"] = "failed"
            result["errors"].append("関数挿入位置 def open_custom_chat_window が見つかりません。")
            return result

        source = source.replace(function_anchor, FUNCTION_CODE + function_anchor, 1)
        result["function_inserted"] = True

    NAVIKO_FILE.write_text(source, encoding="utf-8")

    try:
        py_compile.compile(str(NAVIKO_FILE), doraise=True)
        result["syntax_ok"] = True
        result["status"] = "patched"
    except Exception as error:
        shutil.copy2(backup_path, NAVIKO_FILE)
        result["status"] = "rolled_back"
        result["errors"].append(f"変更後の構文チェックに失敗したため復元: {error}")

    return result


def main() -> None:
    result = patch_naviko()

    print("=== naviko.py Original Bridge 最小接続 ===")
    print(f"状態: {result['status']}")
    print(f"バックアップ: {result['backup']}")
    print(f"import追加: {result['import_inserted']}")
    print(f"呼び出し関数追加: {result['function_inserted']}")
    print(f"構文OK: {result['syntax_ok']}")

    if result["errors"]:
        print("エラー:")
        for error in result["errors"]:
            print(f"- {error}")


if __name__ == "__main__":
    main()