import json
from pathlib import Path
from datetime import datetime


class WorkspaceManager:
    def __init__(self, root_dir):
        self.root = Path(root_dir)

        self.workspace_dir = self.root / "workspace"
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        self.app_dir = self.workspace_dir / "app_projects"
        self.image_dir = self.workspace_dir / "images"
        self.video_dir = self.workspace_dir / "videos"
        self.report_dir = self.workspace_dir / "reports"
        self.archive_dir = self.workspace_dir / "archives"

        for folder in [
            self.app_dir,
            self.image_dir,
            self.video_dir,
            self.report_dir,
            self.archive_dir
        ]:
            folder.mkdir(parents=True, exist_ok=True)

        self.workspace_log_file = (
            self.workspace_dir /
            "workspace_log.json"
        )

        if not self.workspace_log_file.exists():
            self.workspace_log_file.write_text(
                "[]",
                encoding="utf-8"
            )

    def _load_log(self):
        try:
            return json.loads(
                self.workspace_log_file.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return []

    def _save_log(self, data):
        self.workspace_log_file.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

    def create_project_folder(
        self,
        project_name,
        project_type="app"
    ):
        safe_name = (
            str(project_name)
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

        if not safe_name:
            safe_name = "untitled_project"

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        folder_name = f"{safe_name}_{timestamp}"

        base_dir = self.app_dir

        if project_type == "image":
            base_dir = self.image_dir
        elif project_type == "video":
            base_dir = self.video_dir
        elif project_type == "report":
            base_dir = self.report_dir
        elif project_type == "archive":
            base_dir = self.archive_dir

        project_dir = base_dir / folder_name
        project_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        record = {
            "created_at":
                datetime.now().isoformat(
                    timespec="seconds"
                ),
            "project_name": project_name,
            "project_type": project_type,
            "project_dir": str(project_dir)
        }

        log = self._load_log()
        log.append(record)
        self._save_log(log)

        return record

    def diagnose_workspace(self):
        log = self._load_log()

        return {
            "workspace_dir": str(self.workspace_dir),
            "app_projects_exists": self.app_dir.exists(),
            "images_exists": self.image_dir.exists(),
            "videos_exists": self.video_dir.exists(),
            "reports_exists": self.report_dir.exists(),
            "archives_exists": self.archive_dir.exists(),
            "project_count": len(log),
            "workspace_log_file":
                str(self.workspace_log_file)
        }

    def format_workspace_report(self, data):
        lines = []

        lines.append(
            "=== ナビ子 v1.3 WorkspaceManager ==="
        )

        lines.append(
            f"workspace: {data.get('workspace_dir')}"
        )

        lines.append(
            f"app_projects: {data.get('app_projects_exists')}"
        )

        lines.append(
            f"images: {data.get('images_exists')}"
        )

        lines.append(
            f"videos: {data.get('videos_exists')}"
        )

        lines.append(
            f"reports: {data.get('reports_exists')}"
        )

        lines.append(
            f"archives: {data.get('archives_exists')}"
        )

        lines.append(
            f"project_count: {data.get('project_count')}"
        )

        lines.append(
            f"log: {data.get('workspace_log_file')}"
        )

        return "\n".join(lines)