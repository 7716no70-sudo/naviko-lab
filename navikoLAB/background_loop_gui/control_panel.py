# control_panel.py

import tkinter as tk


class ControlPanel:

    def __init__(self, root):
        self.frame = tk.Frame(root)

        self.start_btn = tk.Button(self.frame, text="Start Loop")
        self.stop_btn = tk.Button(self.frame, text="Stop Loop")

        self.start_btn.pack(side="left", padx=5)
        self.stop_btn.pack(side="left", padx=5)