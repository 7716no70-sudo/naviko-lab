from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.folder_analyzer import FolderAnalyzer
from navikoLAB.analyzers.python_analyzer import PythonAnalyzer
from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


class AppAnalyzer:
    """
    FolderAnalyzer / PythonAnalyzer を統合し、
    アプリ全体の構造を読み取り専用で解析する基礎Analyzer。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "analyzers" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.folder_analyzer = FolderAnalyzer(root_dir=self.root_dir)
        self.python_analyzer = PythonAnalyzer(root_dir=self.root_dir)
        self.knowledge_base = KnowledgeBase(root_dir=self.root_dir)
        self.experience_manager = ExperienceManager(root_dir=self.root_dir)

    def analyze_app(self, target_dir=None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = Path(target_dir) if target_dir else self.root_dir

        folder_report = self.folder_analyzer.analyze(target_dir=target, max_files=300)
        python_report = self.python_analyzer.analyze_project(target_dir=target, max_files=150)

        app_summary = {
            "target": str(target),
            "folder_count": folder_report.get("folder_count"),
            "file_count": folder_report.get("file_count"),
            "python_file_count": python_report.get("python_file_count"),
            "syntax_ok_count": python_report.get("syntax_ok_count"),
            "syntax_error_count": python_report.get("syntax_error_count"),
            "total_functions": python_report.get("total_functions"),
            "total_classes": python_report.get("total_classes"),
            "suffix_counts": folder_report.get("suffix_counts", {}),
        }

        status = "completed"
        if python_report.get("syntax_error_count", 0) > 0:
            status = "needs_review"

        report = {
            "title": "App Analysis Report",
            "status": status,
            "created_at": now,
            "mode": "read_only",
            "summary": app_summary,
            "folder_report": folder_report.get("report_path"),
            "python_report": python_report.get("report_path"),
        }

        report_path = self.report_dir / f"app_analysis_{now}.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        knowledge_record = self.knowledge_base.add_knowledge(
            title=f"AppAnalysis: {target.name}",
            content=json.dumps(report, ensure_ascii=False, indent=2),
            source="AppAnalyzer",
            tags=["app_analysis", "folder", "python"],
            metadata={
                "target": str(target),
                "status": status,
                "python_file_count": python_report.get("python_file_count"),
                "syntax_error_count": python_report.get("syntax_error_count"),
            },
        )

        experience_record = self.experience_manager.add_experience(
            title=f"AppAnalyzer Experience: {target.name}",
            event_type="app_analysis",
            status=status,
            summary=f"AppAnalyzer analyzed {target.name} in read-only mode.",
            source="AppAnalyzer",
            metadata={
                "target": str(target),
                "report_path": str(report_path),
                "knowledge_id": knowledge_record.get("id"),
                "knowledge_path": knowledge_record.get("path"),
            },
        )

        report["report_path"] = str(report_path)
        report["knowledge_record"] = {
            "id": knowledge_record.get("id"),
            "path": knowledge_record.get("path"),
        }
        report["experience_record"] = {
            "id": experience_record.get("id"),
            "path": experience_record.get("path"),
        }

        return report

    def diagnose(self) -> dict:
        report = self.analyze_app(target_dir=self.root_dir)

        return {
            "name": "AppAnalyzer",
            "status": "ready" if report.get("status") in ["completed", "needs_review"] else "failed",
            "analysis_status": report.get("status"),
            "summary": report.get("summary"),
            "report_path": report.get("report_path"),
            "knowledge_record": report.get("knowledge_record"),
            "experience_record": report.get("experience_record"),
        }


def main() -> None:
    print("=== AppAnalyzer 診断 ===")

    analyzer = AppAnalyzer()
    report = analyzer.diagnose()

    summary = report.get("summary", {})

    print(f"状態: {report.get('status')}")
    print(f"解析状態: {report.get('analysis_status')}")
    print(f"フォルダ数: {summary.get('folder_count')}")
    print(f"ファイル数: {summary.get('file_count')}")
    print(f"Pythonファイル数: {summary.get('python_file_count')}")
    print(f"構文NG: {summary.get('syntax_error_count')}")
    print(f"Knowledge保存: {report.get('knowledge_record')}")
    print(f"Experience保存: {report.get('experience_record')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()