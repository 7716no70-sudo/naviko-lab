# live_view.py

import tkinter as tk


class LiveView:

    def render(self, metrics):

        print("\n=== NAVIKO LIVE VIEW ===")
        print("Goals:", metrics["goal_count"])
        print("Evolution:", metrics["evolution"])
        print("System:", metrics["system_health"])