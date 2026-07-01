import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from datetime import datetime
import json
import shutil

from navikoLAB.connectors.connector_diagnostics import diagnose_connectors


ROOT = Path(__file__).resolve().parents[2]
LAB_ROOT = ROOT / "navikoLAB"

CAPABILITY_REGISTRY = LAB_ROOT / "capabilities" / "capability_registry.json"
BACKUP_DIR = LAB_ROOT / "capabilities" / "backups"


def load_registry_data():
    if not CAPABILITY_REGISTRY.exists():
        return None

    try:
        return json.loads(CAPABILITY_REGISTRY.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_registry_data(data):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"capability_registry_backup_{timestamp}.json"

    if CAPABILITY_REGISTRY.exists():
        shutil.copy2(CAPABILITY_REGISTRY, backup_path)

    CAPABILITY_REGISTRY.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    return backup_path


def set_connector_enabled(connector_id, enabled_value):
    data = load_registry_data()

    if data is None:
        return False, "capability_registry.json を読み込めませんでした。"

    updated = False

    if isinstance(data, dict) and isinstance(data.get("capabilities"), list):
        for cap in data["capabilities"]:
            cap_id = str(cap.get("id", cap.get("name", ""))).lower()
            if cap_id == connector_id:
                cap["enabled"] = enabled_value
                updated = True
                break

    elif isinstance(data, dict):
        for key, cap in data.items():
            if not isinstance(cap, dict):
                continue

            cap_id = str(cap.get("id", cap.get("name", key))).lower()
            if cap_id == connector_id:
                cap["enabled"] = enabled_value
                updated = True
                break

    elif isinstance(data, list):
        for cap in data:
            if not isinstance(cap, dict):
                continue

            cap_id = str(cap.get("id", cap.get("name", ""))).lower()
            if cap_id == connector_id:
                cap["enabled"] = enabled_value
                updated = True
                break

    if not updated:
        return False, f"{connector_id} が見つかりませんでした。"

    backup_path = save_registry_data(data)

    return True, f"{connector_id} を enabled={enabled_value} に変更しました。\nバックアップ: {backup_path}"


def open_connector_toggle_gui():
    win = tk.Tk()
    win.title("ナビ子 Connector 有効・無効切替")
    win.geometry("780x460")

    title = tk.Label(
        win,
        text="Connector 有効・無効切替",
        font=("Meiryo", 14, "bold")
    )
    title.pack(pady=10)

    summary_label = tk.Label(
        win,
        text="",
        font=("Meiryo", 10)
    )
    summary_label.pack(pady=5)

    columns = ("id", "exists", "enabled", "status", "type")

    tree = ttk.Treeview(
        win,
        columns=columns,
        show="headings",
        height=12
    )

    tree.heading("id", text="Connector")
    tree.heading("exists", text="存在")
    tree.heading("enabled", text="有効")
    tree.heading("status", text="状態")
    tree.heading("type", text="Type")

    tree.column("id", width=160)
    tree.column("exists", width=80, anchor="center")
    tree.column("enabled", width=80, anchor="center")
    tree.column("status", width=160, anchor="center")
    tree.column("type", width=120, anchor="center")

    tree.pack(fill="both", expand=True, padx=12, pady=8)

    def refresh():
        result = diagnose_connectors()

        for item in tree.get_children():
            tree.delete(item)

        for connector in result["connectors"]:
            tree.insert(
                "",
                "end",
                values=(
                    connector["id"],
                    connector["exists"],
                    connector["enabled"],
                    connector["status"],
                    connector["type"],
                )
            )

        summary_text = (
            f"想定: {result['total_expected']} / "
            f"登録済: {result['registered_count']} / "
            f"不足: {result['missing_count']} / "
            f"有効: {result['enabled_count']} / "
            f"無効: {result['disabled_count']} / "
            f"mock: {result['mock_count']} / "
            f"api: {result['api_count']}"
        )

        summary_label.config(text=summary_text)

    def get_selected_connector_id():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "未選択",
                "Connectorを1つ選択してください。"
            )
            return None

        values = tree.item(selected[0], "values")

        if not values:
            return None

        return str(values[0]).lower()

    def enable_selected():
        connector_id = get_selected_connector_id()

        if not connector_id:
            return

        ok, message = set_connector_enabled(connector_id, True)

        if ok:
            refresh()
            messagebox.showinfo("有効化完了", message)
        else:
            messagebox.showerror("有効化失敗", message)

    def disable_selected():
        connector_id = get_selected_connector_id()

        if not connector_id:
            return

        ok, message = set_connector_enabled(connector_id, False)

        if ok:
            refresh()
            messagebox.showinfo("無効化完了", message)
        else:
            messagebox.showerror("無効化失敗", message)

    button_frame = tk.Frame(win)
    button_frame.pack(pady=8)

    enable_button = tk.Button(
        button_frame,
        text="選択Connectorを有効化",
        command=enable_selected,
        width=20
    )
    enable_button.pack(side="left", padx=5)

    disable_button = tk.Button(
        button_frame,
        text="選択Connectorを無効化",
        command=disable_selected,
        width=20
    )
    disable_button.pack(side="left", padx=5)

    refresh_button = tk.Button(
        button_frame,
        text="状態更新",
        command=refresh,
        width=14
    )
    refresh_button.pack(side="left", padx=5)

    close_button = tk.Button(
        button_frame,
        text="閉じる",
        command=win.destroy,
        width=14
    )
    close_button.pack(side="left", padx=5)

    refresh()
    win.mainloop()


def main():
    open_connector_toggle_gui()


if __name__ == "__main__":
    main()