from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.analyzers.folder_analyzer import FolderAnalyzer
from navikoLAB.analyzers.python_analyzer import PythonAnalyzer
from navikoLAB.analyzers.dependency_analyzer import DependencyAnalyzer
from navikoLAB.knowledge.knowledge_base import KnowledgeBase
from navikoLAB.experience.experience_manager import ExperienceManager


class ArchitectureAnalyzer:
    """
    フォルダ構造・Python構造・依存関係から、
    ナビ子LAB全体のアーキテクチャ概要を読み取り専用で解析する基礎Analyzer。
    """

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parents[2]
        self.report_dir = self.root_dir / "navikoLAB" / "analyzers" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

        self.folder_analyzer = FolderAnalyzer(root_dir=self.root_dir)
        self.python_analyzer = PythonAnalyzer(root_dir=self.root_dir)
        self.dependency_analyzer = DependencyAnalyzer(root_dir=self.root_dir)
        self.knowledge_base = KnowledgeBase(root_dir=self.root_dir)
        self.experience_manager = ExperienceManager(root_dir=self.root_dir)

    def detect_layers(self, folder_report: dict) -> list[dict]:
        known_layers = [
            "connectors",
            "capabilities",
            "missions",
            "research",
            "search",
            "knowledge",
            "experience",
            "analyzers",
            "reports",
            "workspace",
            "builders",
            "reflection",
            "improvement_results",
        ]

        folders_text = " ".join(folder_report.get("folders_sample", []))
        layers = []

        for layer in known_layers:
            detected = layer.lower() in folders_text.lower()
            layers.append(
                {
                    "name": layer,
                    "detected": detected,
                }
            )

        return layers

    def infer_architecture_style(self, layers: list[dict]) -> str:
        detected = {item["name"] for item in layers if item.get("detected")}

        if {"connectors", "research", "knowledge", "experience", "analyzers"}.issubset(detected):
            return "modular_agent_research_knowledge_architecture"

        if {"connectors", "capabilities", "missions"}.issubset(detected):
            return "modular_agent_architecture"

        return "mixed_or_early_stage_architecture"

    def analyze(self, target_dir=None) -> dict:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = Path(target_dir) if target_dir else self.root_dir

        folder_report = self.folder_analyzer.analyze(target_dir=target, max_files=300)
        python_report = self.python_analyzer.analyze_project(target_dir=target, max_files=150)
        dependency_report = self.dependency_analyzer.analyze(target_dir=target, max_files=150)

        layers = self.detect_layers(folder_report)
        architecture_style = self.infer_architecture_style(layers)

        summary = {
            "target": str(target),
            "architecture_style": architecture_style,
            "folder_count": folder_report.get("folder_count"),
            "file_count": folder_report.get("file_count"),
            "python_file_count": python_report.get("python_file_count"),
            "syntax_error_count": python_report.get("syntax_error_count"),
            "total_functions": python_report.get("total_functions"),
            "total_classes": python_report.get("total_classes"),
            "external_import_count": len(dependency_report.get("external_imports", [])),
            "possible_missing_requirements_count": len(dependency_report.get("possible_missing_requirements", [])),
            "layers": layers,
        }

        recommendations = []

        if summary["syntax_error_count"] > 0:
            recommendations.append(
                {
                    "type": "syntax_review",
                    "priority": "high",
                    "summary": "構文エラーのあるPythonファイルがあります。",
                }
            )

        if summary["possible_missing_requirements_count"] > 0:
            recommendations.append(
                {
                    "type": "dependency_review",
                    "priority": "medium",
                    "summary": "requirements.txtに未記録の可能性がある外部importがあります。",
                }
            )

        if architecture_style == "modular_agent_research_knowledge_architecture":
            recommendations.append(
                {
                    "type": "architecture_stable",
                    "priority": "low",
                    "summary": "ナビ子LABはモジュール分離された研究・知識基盤型アーキテクチャとして整理されています。",
                }
            )

        report = {
            "title": "Architecture Analysis Report",
            "status": "completed",
            "created_at": now,
            "mode": "read_only",
            "summary": summary,
            "recommendations": recommendations,
            "folder_report": folder_report.get("report_path"),
            "python_report": python_report.get("report_path"),
            "dependency_report": dependency_report.get("report_path"),
        }

        report_path = self.report_dir / f"architecture_analysis_{now}.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        knowledge_record = self.knowledge_base.add_knowledge(
            title=f"ArchitectureAnalysis: {target.name}",
            content=json.dumps(report, ensure_ascii=False, indent=2),
            source="ArchitectureAnalyzer",
            tags=["architecture", "analysis", "dependency"],
            metadata={
                "target": str(target),
                "architecture_style": architecture_style,
                "syntax_error_count": summary["syntax_error_count"],
                "possible_missing_requirements_count": summary["possible_missing_requirements_count"],
            },
        )

        experience_record = self.experience_manager.add_experience(
            title=f"ArchitectureAnalyzer Experience: {target.name}",
            event_type="architecture_analysis",
            status="completed",
            summary=f"ArchitectureAnalyzer analyzed {target.name} in read-only mode.",
            source="ArchitectureAnalyzer",
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
        report = self.analyze(target_dir=self.root_dir)
        summary = report.get("summary", {})

        return {
            "name": "ArchitectureAnalyzer",
            "status": "ready" if report.get("status") == "completed" else "failed",
            "architecture_style": summary.get("architecture_style"),
            "syntax_error_count": summary.get("syntax_error_count"),
            "possible_missing_requirements_count": summary.get("possible_missing_requirements_count"),
            "recommendation_count": len(report.get("recommendations", [])),
            "report_path": report.get("report_path"),
            "knowledge_record": report.get("knowledge_record"),
            "experience_record": report.get("experience_record"),
        }


def main() -> None:
    print("=== ArchitectureAnalyzer 診断 ===")

    analyzer = ArchitectureAnalyzer()
    report = analyzer.diagnose()

    print(f"状態: {report.get('status')}")
    print(f"構造: {report.get('architecture_style')}")
    print(f"構文NG: {report.get('syntax_error_count')}")
    print(f"requirements不足候補: {report.get('possible_missing_requirements_count')}")
    print(f"提案件数: {report.get('recommendation_count')}")
    print(f"Knowledge保存: {report.get('knowledge_record')}")
    print(f"Experience保存: {report.get('experience_record')}")
    print(f"保存先: {report.get('report_path')}")


if __name__ == "__main__":
    main()