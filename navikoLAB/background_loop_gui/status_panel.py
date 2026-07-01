# status_panel.py

import tkinter as tk


class StatusPanel:

    def __init__(self, root):
        self.frame = tk.Frame(root)

        self.phase_label = tk.Label(self.frame, text="Phase: -")
        self.risk_label = tk.Label(self.frame, text="Risk: -")
        self.decision_label = tk.Label(self.frame, text="Decision: -")

        self.phase_label.pack(side="left", padx=10)
        self.risk_label.pack(side="left", padx=10)
        self.decision_label.pack(side="left", padx=10)

    def update(self, data):
        self.phase_label.config(text=f"Phase: {data.get('phase')}")
        self.risk_label.config(text=f"Risk: {data.get('risk_level')}")
        self.decision_label.config(text=f"Decision: {data.get('decision', '-')}")