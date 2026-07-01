from __future__ import annotations

import py_compile
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NAVIKO_FILE = ROOT / "naviko.py"
BACKUP_DIR = ROOT / "navikoLAB" / "original_adoption" / "naviko_patch_backups"


DASHBOARD_IMPORT_CODE = """
try:
    from navikoLAB.original_adoption.mission_dashboard import open_mission_dashboard
except Exception:
    open_mission_dashboard = None

"""


MISSION_BUTTON_CODE = """

    tk.Button(
        top_menu,
        text="AIミッション",
        command=lambda: open_mission_dashboard(c_win) if open_mission_dashboard else append_chat_bubble(
            c_area,
            "navi",
            "AIミッションハブを読み込めませんでした。"
        ),
        bg="#059669",
        fg="#ffffff",
        font=("MS Gothic", 9, "bold"),
        bd=0,
        padx=10
    ).pack(side=tk.LEFT, padx=3)
"""


def backup_naviko() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"naviko_before_mission_dashboard_button_{now}.py"
    shutil.copy2(NAVIKO_FILE, backup_path)
    return backup_path


def patch_naviko() -> dict:
    result = {
        "status": "not_started",
        "backup": None,
        "dashboard_import_inserted": False,
        "mission_button_inserted": False,
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

    if "from navikoLAB.original_adoption.mission_dashboard import open_mission_dashboard" not in source:
        import_anchor = (
            "except Exception:\n"
            "    run_original_autonomous_bridge = None\n"
        )

        if import_anchor not in source:
            result["status"] = "failed"
            result["errors"].append("Mission Dashboard import 挿入位置が見つかりません。")
            return result

        source = source.replace(import_anchor, import_anchor + DASHBOARD_IMPORT_CODE, 1)
        result["dashboard_import_inserted"] = True

    if 'text="AIミッション"' not in source:
        button_anchor = (
            "    tk.Button(\n"
            "        top_menu,\n"
            "        text=\"ナビ子メニュー\",\n"
            "        command=lambda: open_naviko_menu_window(c_area),\n"
            "        bg=\"#4f46e5\",\n"
            "        fg=\"#ffffff\",\n"
            "        font=(\"MS Gothic\", 9, \"bold\"),\n"
            "        bd=0,\n"
            "        padx=10\n"
            "    ).pack(side=tk.LEFT, padx=3)\n"
        )

        if button_anchor not in source:
            result["status"] = "failed"
            result["errors"].append("AIミッションボタン挿入位置が見つかりません。")
            return result

        source = source.replace(button_anchor, button_anchor + MISSION_BUTTON_CODE, 1)
        result["mission_button_inserted"] = True

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

    print("=== AIミッションボタン追加 ===")
    print(f"状態: {result['status']}")
    print(f"バックアップ: {result['backup']}")
    print(f"Dashboard import追加: {result['dashboard_import_inserted']}")
    print(f"AIミッションボタン追加: {result['mission_button_inserted']}")
    print(f"構文OK: {result['syntax_ok']}")

    if result["errors"]:
        print("エラー:")
        for error in result["errors"]:
            print(f"- {error}")


if __name__ == "__main__":
    main()