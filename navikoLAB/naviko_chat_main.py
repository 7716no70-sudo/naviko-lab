# navikoLAB/naviko_chat_main.py

import tkinter as tk
from tkinter import scrolledtext

from navikoLAB.core.naviko_core import NavikoCore


class NavikoChatGUI:
    """
    Naviko Chat GUI v2.0

    役割:
    - ウィンドウを起動する
    - ユーザー入力を NavikoCore に渡す
    - NavikoCore / NavikoBrain の返答を表示する
    """

    def __init__(self, root):
        self.core = NavikoCore()

        self.root = root
        self.root.title("Naviko AI OS v1.4 - Chat GUI")
        self.root.geometry("760x540")

        self.chat_area = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state="disabled",
            font=("Meiryo", 10),
        )
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(root, font=("Meiryo", 10))
        self.entry.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry.bind("<Return>", self.send_message)

        self.button = tk.Button(
            root,
            text="送信",
            command=self.send_message,
            font=("Meiryo", 10),
        )
        self.button.pack(padx=10, pady=(0, 10))

        boot = self.core.boot()
        self.add_message("ナビ子", boot["message"])
        self.add_message("System", "NavikoCore / NavikoBrain 接続完了")

    def add_message(self, speaker, text):
        self.chat_area.configure(state="normal")
        self.chat_area.insert(tk.END, f"{speaker}: {text}\n\n")
        self.chat_area.configure(state="disabled")
        self.chat_area.see(tk.END)

    def send_message(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text:
            return

        self.entry.delete(0, tk.END)
        self.add_message("ナオさん", user_text)

        result = self.core.handle_input(user_text)
        reply = result.get("reply", "")

        self.add_message("ナビ子", reply)


def main():
    root = tk.Tk()
    NavikoChatGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()