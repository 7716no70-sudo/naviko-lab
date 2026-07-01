import tkinter as tk
from tkinter import messagebox


def open_connector_management():
    try:
        from navikoLAB.connectors.connector_gui_launcher import open_connector_launcher
        open_connector_launcher()
    except Exception as e:
        messagebox.showerror(
            "Connector管理 エラー",
            str(e)
        )


def show_future_feature(name):
    messagebox.showinfo(
        f"{name}",
        f"{name} は今後の工程で追加予定です。"
    )


def open_ai_management_hub():
    win = tk.Tk()
    win.title("ナビ子 AI管理ハブ")
    win.geometry("460x360")

    title = tk.Label(
        win,
        text="AI管理ハブ",
        font=("Meiryo", 15, "bold")
    )
    title.pack(pady=14)

    description = tk.Label(
        win,
        text="Connector・Knowledge・Research・Experience を管理する入口です。",
        font=("Meiryo", 9)
    )
    description.pack(pady=6)

    tk.Button(
        win,
        text="Connector管理",
        command=open_connector_management,
        width=32
    ).pack(pady=6)

    tk.Button(
        win,
        text="Knowledge管理（予定）",
        command=lambda: show_future_feature("Knowledge管理"),
        width=32
    ).pack(pady=6)

    tk.Button(
        win,
        text="Research管理（予定）",
        command=lambda: show_future_feature("Research管理"),
        width=32
    ).pack(pady=6)

    tk.Button(
        win,
        text="Experience管理（予定）",
        command=lambda: show_future_feature("Experience管理"),
        width=32
    ).pack(pady=6)

    tk.Button(
        win,
        text="Agent / Capability管理（予定）",
        command=lambda: show_future_feature("Agent / Capability管理"),
        width=32
    ).pack(pady=6)

    tk.Button(
        win,
        text="閉じる",
        command=win.destroy,
        width=32
    ).pack(pady=14)

    win.mainloop()


def main():
    open_ai_management_hub()


if __name__ == "__main__":
    main()