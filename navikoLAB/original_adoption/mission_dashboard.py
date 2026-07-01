from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "navikoLAB" / "original_adoption" / "mission_dashboard_logs"


def run_dashboard_mission(goal: str) -> dict:
    from navikoLAB.original_adoption.original_naviko_bridge import run_original_autonomous_bridge

    result = run_original_autonomous_bridge(goal)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"mission_dashboard_run_{now}.json"

    log_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    result["dashboard_log"] = str(log_path)
    return result


def open_mission_dashboard(parent=None):
    win = tk.Toplevel(parent) if parent else tk.Toplevel()
    win.title("Naviko AI Mission Dashboard")
    win.geometry("820x680")
    win.configure(bg="#111827")
    win.wm_attributes("-topmost", True)

    title = tk.Label(
        win,
        text="AIミッションハブ",
        bg="#111827",
        fg="#ffffff",
        font=("MS Gothic", 16, "bold"),
    )
    title.pack(fill="x", padx=10, pady=10)

    goal_box = tk.Text(
        win,
        height=4,
        bg="#1f2937",
        fg="#ffffff",
        insertbackground="#ffffff",
        font=("MS Gothic", 11),
        wrap="word",
    )
    goal_box.pack(fill="x", padx=10, pady=6)
    goal_box.insert("1.0", "TODOアプリを作りたい")

    output = scrolledtext.ScrolledText(
        win,
        bg="#0f172a",
        fg="#e5e7eb",
        insertbackground="#ffffff",
        font=("MS Gothic", 10),
        wrap="word",
    )
    output.pack(fill="both", expand=True, padx=10, pady=10)

    def write(message: str):
        output.configure(state="normal")
        output.insert(tk.END, message + "\n")
        output.see(tk.END)
        output.configure(state="disabled")

    def write_dict(title_text: str, data):
        write(title_text)

        if not data:
            write("- なし")
            return

        if isinstance(data, dict):
            for key, value in data.items():
                write(f"- {key}: {value}")
            return

        if isinstance(data, list):
            for item in data:
                write(f"- {item}")
            return

        write(f"- {data}")

    def start_mission():
        goal = goal_box.get("1.0", "end").strip()
        if not goal:
            goal = "TODOアプリを作りたい"

        write("=== AIミッション開始 ===")
        write(f"目的: {goal}")

        try:
            result = run_dashboard_mission(goal)
            write(f"状態: {result.get('status')}")
            write(f"モード: {result.get('mode')}")
            write(f"メッセージ: {result.get('message')}")
            write(f"ログ: {result.get('dashboard_log')}")
            write("")

            write_dict("必要能力:", result.get("required_capabilities"))
            write_dict("不足能力:", result.get("missing_capabilities"))
            write_dict("推奨AI:", result.get("recommended_agents"))
            write("")

            artifacts = result.get("artifacts", {})
            write_dict("成果物:", artifacts)
            write("")

            reflection = result.get("multi_ai_reflection", {})
            write_dict("Reflection:", reflection)
            write("")

            improvement = result.get("multi_ai_improvement_request", {})
            write_dict("Improvement Request:", improvement)
            write("")

            write("接続フロー:")
            for item in result.get("flow", []):
                write(f"- {item}")

        except Exception as error:
            write(f"ERROR: {error}")

        write("=== AIミッション終了 ===")

    button_frame = tk.Frame(win, bg="#111827")
    button_frame.pack(fill="x", padx=10, pady=6)

    tk.Button(
        button_frame,
        text="AIミッション開始",
        command=start_mission,
        bg="#4f46e5",
        fg="#ffffff",
        font=("MS Gothic", 11, "bold"),
        bd=0,
        padx=12,
        pady=6,
    ).pack(side=tk.LEFT, padx=4)

    tk.Button(
        button_frame,
        text="閉じる",
        command=win.destroy,
        bg="#7f1d1d",
        fg="#ffffff",
        font=("MS Gothic", 11),
        bd=0,
        padx=12,
        pady=6,
    ).pack(side=tk.RIGHT, padx=4)

    write("AIミッションハブを起動しました。")
    write("目的を入力して「AIミッション開始」を押してください。")

    return win