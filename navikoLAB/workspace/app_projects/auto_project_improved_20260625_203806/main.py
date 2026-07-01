import tkinter as tk
from tkinter import messagebox


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODOアプリ")
        self.root.geometry("420x420")

        self.todos = []

        self.title_label = tk.Label(
            root,
            text="TODOアプリ",
            font=("Meiryo", 16, "bold")
        )
        self.title_label.pack(pady=10)

        self.entry = tk.Entry(
            root,
            font=("Meiryo", 11)
        )
        self.entry.pack(fill="x", padx=20, pady=5)

        self.add_button = tk.Button(
            root,
            text="追加",
            command=self.add_todo
        )
        self.add_button.pack(fill="x", padx=20, pady=5)

        self.delete_button = tk.Button(
            root,
            text="選択したTODOを削除",
            command=self.delete_todo
        )
        self.delete_button.pack(fill="x", padx=20, pady=5)

        self.listbox = tk.Listbox(
            root,
            font=("Meiryo", 11)
        )
        self.listbox.pack(fill="both", expand=True, padx=20, pady=10)

        self.status_label = tk.Label(
            root,
            text="TODOを入力して追加してください。",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=20, pady=5)

    def add_todo(self):
        text = self.entry.get().strip()

        if not text:
            messagebox.showwarning(
                "入力エラー",
                "TODOを入力してください。"
            )
            return

        self.todos.append(text)
        self.listbox.insert(tk.END, text)
        self.entry.delete(0, tk.END)
        self.status_label.config(
            text=f"追加しました: {text}"
        )

    def delete_todo(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showinfo(
                "選択なし",
                "削除するTODOを選択してください。"
            )
            return

        index = selected[0]
        deleted = self.todos.pop(index)
        self.listbox.delete(index)
        self.status_label.config(
            text=f"削除しました: {deleted}"
        )


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
