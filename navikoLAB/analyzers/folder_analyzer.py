from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class FolderAnalyzer:
    """
    プロジェクトフォルダ構造を読み取り専用で解析する基礎Analyzer。
    ファイル編集・削除・外部通信は行わない。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "analyzers" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def analyze(self, target_dir=None, max_files: int = 300) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = Path(target_dir) if target_dir else self.root_dir

        files = []
        folders = []

        if not target.exists():
            return {
                "status": "failed",
                "reason": "target_not_found",
                "target": str(target),
                "created_at": now,
            }

        for path in target.rglob("*"):
            try:
                relative = str(path.relative_to(target))
            except Exception:
                relative = str(path)

            if path.is_dir():
                folders.append(relative)
            elif path.is_file():
                files.append(
                    {
                        "path": relative,
                        "suffix": path.suffix,
                        "size": path.stat().st_size,
                    }
                )

            if len(files) >= max_files:
                break

        suffix_counts = {}
        for item in files:
            suffix = item.get("suffix") or "[no_ext]"
            suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1

        report = {
            "title": "Folder Analysis Report",
            "status": "completed",
            "target": str(target),
            "created_at": now,
            "folder_count": len(folders),
            "file_count": len(files),
            "suffix_counts": suffix_counts,
            "folders_sample": folders[:50],
            "files_sample": files[:80],
            "limited": len(files) >= max_files,
            "mode": "read_only",
        }

        report_path = self.report_dir / f"folder_analysis_{now}.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        report["report_path"] = str(report_path)
        return report

    def diagnose(self) -> dict:
        report = self.analyze(target_dir=self.root_dir, max_files=100)

        return {
            "name": "FolderAnalyzer",
            "status": "ready" if report.get("status") == "completed" else "failed",
            "folder_count": report.get("folder_count"),
            "file_count": report.get("file_count"),
            "report_path": report.get("report_path"),
        }


def main() -> None:
    print("=== FolderAnalyzer 診断 ===")

    analyzer = FolderAnalyzer()
    report = analyzer.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"フォルダ数: {report.get('folder_count')}")
    print(f"ファイル数: {report.get('file_count')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()