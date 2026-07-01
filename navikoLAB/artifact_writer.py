from pathlib import Path
from datetime import datetime


class ArtifactWriter:
    def __init__(self, root_dir):
        self.root = Path(root_dir)

    def _safe_filename(self, filename):
        safe = (
            str(filename)
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("*", "_")
            .replace("?", "_")
            .replace('"', "_")
            .replace("<", "_")
            .replace(">", "_")
            .replace("|", "_")
            .strip()
        )

        if not safe:
            safe = "untitled.txt"

        return safe

    def write_text_file(
        self,
        folder_path,
        filename,
        content
    ):
        folder = Path(folder_path)
        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_name = self._safe_filename(filename)

        file_path = folder / safe_name

        file_path.write_text(
            str(content),
            encoding="utf-8"
        )

        return {
            "created_at":
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            "file": str(file_path),
            "size": len(str(content)),
            "status": "created"
        }

    def create_basic_app_files(
        self,
        project_dir,
        app_name="naviko_app"
    ):
        project_dir = Path(project_dir)
        project_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        results = []

        results.append(
            self.write_text_file(
                project_dir,
                "README.md",
                f"# {app_name}\n\nナビ子が作成したアプリプロジェクトです。\n"
            )
        )

        results.append(
            self.write_text_file(
                project_dir,
                "requirements.txt",
                "# 必要なライブラリをここに記載します。\n"
            )
        )

        results.append(
            self.write_text_file(
                project_dir,
                "main.py",
                (
                    "def main():\n"
                    "    print('Hello from Naviko app!')\n\n"
                    "if __name__ == '__main__':\n"
                    "    main()\n"
                )
            )
        )

        results.append(
            self.write_text_file(
                project_dir,
                "notes.txt",
                (
                    "=== ナビ子 作業メモ ===\n"
                    f"作成日時: {datetime.now().isoformat(timespec='seconds')}\n"
                    "状態: 初期ファイル作成済み\n"
                )
            )
        )

        return results

    def format_write_results(self, results):
        lines = []
        lines.append("=== ナビ子 v1.3 ArtifactWriter ===")

        for item in results:
            lines.append("")
            lines.append(f"status: {item.get('status')}")
            lines.append(f"file: {item.get('file')}")
            lines.append(f"size: {item.get('size')}")

        return "\n".join(lines)