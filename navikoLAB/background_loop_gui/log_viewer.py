# log_viewer.py

import tkinter as tk


class LogViewer:

    def __init__(self, root):
        self.frame = tk.Frame(root)

        self.text = tk.Text(self.frame, height=20)
        self.text.pack(fill="both", expand=True)

    def append(self, data):
        self.text.insert("end", str(data) + "\n")
        self.text.see("end")