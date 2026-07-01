# gui_launcher.py

import tkinter as tk
from loop_dashboard import LoopDashboard


class Launcher:

    def __init__(self):
        self.root = tk.Tk()
        self.dashboard = LoopDashboard(self.root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Launcher().run()