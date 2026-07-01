import tkinter as tk
from tkinter import ttk, messagebox

from navikoLAB.connectors.connector_diagnostics import diagnose_connectors


def load_connector_rows():
    result = diagnose_connectors()
    return result


def open_connector_status_gui():
    result = load_connector_rows()

    win = tk.Tk()
    win.title("ナビ子 Connector 状態一覧")
    win.geometry("760x420")

    title = tk.Label(
        win,
        text="Connector 状態一覧",
        font=("Meiryo", 14, "bold")
    )
    title.pack(pady=10)

    summary_text = (
        f"想定: {result['total_expected']} / "
        f"登録済: {result['registered_count']} / "
        f"不足: {result['missing_count']} / "
        f"有効: {result['enabled_count']} / "
        f"無効: {result['disabled_count']} / "
        f"mock: {result['mock_count']} / "
        f"api: {result['api_count']}"
    )

    summary_label = tk.Label(
        win,
        text=summary_text,
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

    tree.pack(fill="both", expand=True, padx=12, pady=8)

    def refresh():
        new_result = load_connector_rows()

        for item in tree.get_children():
            tree.delete(item)

        for connector in new_result["connectors"]:
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

        new_summary = (
            f"想定: {new_result['total_expected']} / "
            f"登録済: {new_result['registered_count']} / "
            f"不足: {new_result['missing_count']} / "
            f"有効: {new_result['enabled_count']} / "
            f"無効: {new_result['disabled_count']} / "
            f"mock: {new_result['mock_count']} / "
            f"api: {new_result['api_count']}"
        )

        summary_label.config(text=new_summary)

        messagebox.showinfo(
            "更新",
            "Connector状態を更新しました。"
        )

    button_frame = tk.Frame(win)
    button_frame.pack(pady=8)

    refresh_button = tk.Button(
        button_frame,
        text="状態更新",
        command=refresh,
        width=16
    )
    refresh_button.pack(side="left", padx=5)

    close_button = tk.Button(
        button_frame,
        text="閉じる",
        command=win.destroy,
        width=16
    )
    close_button.pack(side="left", padx=5)

    win.mainloop()


def main():
    open_connector_status_gui()


if __name__ == "__main__":
    main()