import tkinter as tk
from tkinter import messagebox


def open_connector_status():
    try:
        from navikoLAB.connectors.connector_status_gui import open_connector_status_gui
        open_connector_status_gui()
    except Exception as e:
        messagebox.showerror(
            "Connector状態GUI エラー",
            str(e)
        )


def open_connector_toggle():
    try:
        from navikoLAB.connectors.connector_toggle_gui import open_connector_toggle_gui
        open_connector_toggle_gui()
    except Exception as e:
        messagebox.showerror(
            "Connector切替GUI エラー",
            str(e)
        )


def run_chatgpt_diagnostics():
    try:
        from navikoLAB.connectors.chatgpt_connector_diagnostics import diagnose_chatgpt_connector

        result = diagnose_chatgpt_connector()

        text = (
            "=== ChatGPT Connector 診断 ===\n"
            f"OPENAI_API_KEY: {'あり' if result.get('api_key_exists') else 'なし'}\n"
            f"model: {result.get('model')}\n"
            f"direct_status: {result.get('direct_status')}\n"
            f"dispatcher_status: {result.get('dispatcher_status')}\n"
            f"dispatcher_log: {result.get('dispatcher_log')}\n"
        )

        messagebox.showinfo(
            "ChatGPT Connector 診断",
            text
        )

    except Exception as e:
        messagebox.showerror(
            "ChatGPT診断 エラー",
            str(e)
        )


def open_connector_launcher():
    win = tk.Tk()
    win.title("ナビ子 Connector 管理")
    win.geometry("420x280")

    title = tk.Label(
        win,
        text="Connector 管理",
        font=("Meiryo", 14, "bold")
    )
    title.pack(pady=14)

    description = tk.Label(
        win,
        text="Connectorの状態確認・有効無効切替・ChatGPT診断を行います。",
        font=("Meiryo", 9)
    )
    description.pack(pady=6)

    status_button = tk.Button(
        win,
        text="Connector状態一覧",
        command=open_connector_status,
        width=28
    )
    status_button.pack(pady=6)

    toggle_button = tk.Button(
        win,
        text="Connector有効・無効切替",
        command=open_connector_toggle,
        width=28
    )
    toggle_button.pack(pady=6)

    chatgpt_button = tk.Button(
        win,
        text="ChatGPT Connector診断",
        command=run_chatgpt_diagnostics,
        width=28
    )
    chatgpt_button.pack(pady=6)

    close_button = tk.Button(
        win,
        text="閉じる",
        command=win.destroy,
        width=28
    )
    close_button.pack(pady=12)

    win.mainloop()


def main():
    open_connector_launcher()


if __name__ == "__main__":
    main()