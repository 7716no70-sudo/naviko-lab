import json
from pathlib import Path
from datetime import datetime


class AppProjectBuilder:
    def __init__(
        self,
        root_dir,
        action_planner=None,
        workspace_manager=None,
        artifact_writer=None
    ):
        self.root = Path(root_dir)

        self.action_planner = action_planner
        self.workspace_manager = workspace_manager
        self.artifact_writer = artifact_writer

        self.builder_dir = self.root / "builders"
        self.builder_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.builder_log_file = (
            self.builder_dir /
            "app_project_builder_log.json"
        )

        if not self.builder_log_file.exists():
            self.builder_log_file.write_text(
                "[]",
                encoding="utf-8"
            )

    def _load_log(self):
        try:
            return json.loads(
                self.builder_log_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return []

    def _save_log(self, data):
        self.builder_log_file.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def should_generate_gui_app(self, purpose):
        text = str(purpose).lower()

        gui_keywords = [
            "gui",
            "tkinter",
            "画面",
            "ボタン",
            "ウィンドウ",
            "main.py にgui要素が少ない",
            "gui要素が少ない",
            "gui要素"
        ]

        for keyword in gui_keywords:
            if keyword in text:
                return True

        return False


    def create_gui_main_py_content(self, purpose):
        return f'''import tkinter as tk
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
            text=f"追加しました: {{text}}"
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
            text=f"削除しました: {{deleted}}"
        )


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
'''

    def build_basic_app_project(
        self,
        purpose,
        project_name="naviko_app_project"
    ):
        result = {
            "created_at":
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            "purpose": purpose,
            "project_name": project_name,
            "action_plan": None,
            "project": None,
            "files": [],
            "status": "started",
            "messages": []
        }

        if not self.action_planner:
            result["status"] = "failed"
            result["messages"].append(
                "ActionPlanner が接続されていません。"
            )
            self._append_log(result)
            return result

        if not self.workspace_manager:
            result["status"] = "failed"
            result["messages"].append(
                "WorkspaceManager が接続されていません。"
            )
            self._append_log(result)
            return result

        if not self.artifact_writer:
            result["status"] = "failed"
            result["messages"].append(
                "ArtifactWriter が接続されていません。"
            )
            self._append_log(result)
            return result

        action_plan = self.action_planner.create_action_plan(
            purpose
        )

        result["action_plan"] = action_plan
        result["messages"].append(
            "具体的作業を作成しました。"
        )

        project = self.workspace_manager.create_project_folder(
            project_name,
            project_type="app"
        )

        result["project"] = project
        result["messages"].append(
            "プロジェクトフォルダを作成しました。"
        )

        files = self.artifact_writer.create_basic_app_files(
            project["project_dir"],
            app_name=project_name
        )

        if self.should_generate_gui_app(purpose):
            project_dir = Path(project["project_dir"])
            main_file = project_dir / "main.py"

            main_file.write_text(
                self.create_gui_main_py_content(purpose),
                encoding="utf-8"
            )

            result["messages"].append(
                "改善要求によりGUI版main.pyを生成しました。"
            )

        result["files"] = files
        result["messages"].append(
            "初期ファイルを作成しました。"
        )

        result["status"] = "completed"

        self._append_log(result)
        return result

    def _append_log(self, result):
        log = self._load_log()
        log.append(result)
        self._save_log(log)

    def diagnose_builder(self):
        log = self._load_log()

        completed = 0
        failed = 0

        for item in log:
            if item.get("status") == "completed":
                completed += 1
            elif item.get("status") == "failed":
                failed += 1

        return {
            "builder_log_count": len(log),
            "completed_count": completed,
            "failed_count": failed,
            "builder_log_file":
                str(self.builder_log_file),
            "action_planner_connected":
                self.action_planner is not None,
            "workspace_manager_connected":
                self.workspace_manager is not None,
            "artifact_writer_connected":
                self.artifact_writer is not None
        }

    def format_build_result(self, result):
        lines = []

        lines.append(
            "=== ナビ子 v1.3 AppProjectBuilder ==="
        )

        lines.append(
            f"目的: {result.get('purpose')}"
        )

        lines.append(
            f"状態: {result.get('status')}"
        )

        lines.append("")

        lines.append("メッセージ:")
        for msg in result.get("messages", []):
            lines.append(f"- {msg}")

        project = result.get("project")
        if project:
            lines.append("")
            lines.append(
                f"プロジェクト: {project.get('project_name')}"
            )
            lines.append(
                f"保存先: {project.get('project_dir')}"
            )

        action_plan = result.get("action_plan")
        if action_plan:
            lines.append("")
            lines.append("具体的作業:")
            for i, action in enumerate(
                action_plan.get("actions", []),
                start=1
            ):
                lines.append(
                    f"{i}. {action}"
                )

        files = result.get("files", [])
        if files:
            lines.append("")
            lines.append("作成ファイル:")
            for item in files:
                lines.append(
                    f"- {item.get('file')}"
                )

        return "\n".join(lines)