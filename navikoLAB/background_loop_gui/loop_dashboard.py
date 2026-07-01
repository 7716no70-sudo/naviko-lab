# loop_dashboard.py

import tkinter as tk
from status_panel import StatusPanel
from control_panel import ControlPanel
from log_viewer import LogViewer


class LoopDashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Naviko Background Loop Monitor")

        self.status = StatusPanel(root)
        self.control = ControlPanel(root)
        self.logs = LogViewer(root)

        self.status.frame.pack(fill="x")
        self.control.frame.pack(fill="x")
        self.logs.frame.pack(fill="both", expand=True)

    def update(self, data):
        self.status.update(data)
        self.logs.append(data)