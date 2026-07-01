# navikoLAB/runtime/ui_layer.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import json
import tkinter as tk


PHASE = "Phase106-4 Naviko UI Layer"

ROOT = Path(__file__).resolve().parents[2]

UI_DIR = ROOT / "runtime" / "ui"
UI_DIR.mkdir(parents=True, exist_ok=True)

UI_STATE_FILE = UI_DIR / "ui_state.json"


# -----------------------------
# UI STATE MODEL
# -----------------------------

@dataclass
class UIState:
    window_title: str
    width: int
    height: int
    theme: str
    last_input: str
    last_output: str


# -----------------------------
# NAVIKO UI CORE
# -----------------------------

class NavikoUI:

    def __init__(self):

        self.state = UIState(
            window_title="Naviko AI OS",
            width=500,
            height=400,
            theme="dark",
            last_input="",
            last_output=""
        )

        self.root = tk.Tk()
        self.root.title(self.state.window_title)
        self.root.geometry(f"{self.state.width}x{self.state.height}")

        self.create_widgets()

    # -----------------------------
    # UI WIDGETS
    # -----------------------------

    def create_widgets(self):

        self.text_area = tk.Text(self.root, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.entry = tk.Entry(self.root)
        self.entry.pack(fill=tk.X)

        self.button = tk.Button(
            self.root,
            text="Send to Naviko",
            command=self.on_send
        )
        self.button.pack()

        self.output_label = tk.Label(self.root, text="Output: ready", fg="green")
        self.output_label.pack()

    # -----------------------------
    # EVENT HANDLER
    # -----------------------------

    def on_send(self):

        user_input = self.entry.get()

        self.state.last_input = user_input

        response = self.process_input(user_input)

        self.state.last_output = response

        self.text_area.insert(tk.END, f"\nUser: {user_input}\nNaviko: {response}\n")

        self.output_label.config(text=f"Output: {response}")

        self.save_state()

    # -----------------------------
    # SIMPLE NAVIKO LOGIC (DRY RUN)
    # -----------------------------

    def process_input(self, text: str):

        if "hello" in text.lower():
            return "Hello. I am Naviko."

        elif "status" in text.lower():
            return "System is running in dry_run mode."

        elif "task" in text.lower():
            return "Task received and queued (simulated)."

        else:
            return "I understood your input (dry_run response)."

    # -----------------------------
    # SAVE STATE
    # -----------------------------

    def save_state(self):

        UI_STATE_FILE.write_text(
            json.dumps(self.state.__dict__, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    # -----------------------------
    # RUN UI
    # -----------------------------

    def run(self):

        self.root.mainloop()


# -----------------------------
# ENTRY POINT
# -----------------------------

def main():

    ui = NavikoUI()

    print("=== Naviko UI Layer ===")
    print("phase:", PHASE)
    print("mode: dry_run")
    print("status: launching UI")

    ui.run()


if __name__ == "__main__":
    main()