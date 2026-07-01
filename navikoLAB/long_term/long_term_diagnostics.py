from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LONG_TERM_DIR = ROOT / "navikoLAB" / "long_term"
GRAPH_DIR = LONG_TERM_DIR / "graphs"
PROJECT_DIR = LONG_TERM_DIR / "project_knowledge"
ARCHITECTURE_DIR = LONG_TERM_DIR / "architecture_memory"


class LongTermDiagnostics:
    def run(self) -> dict:
        knowledge_graphs = list(GRAPH_DIR.glob("knowledge_graph_*.json")) if GRAPH_DIR.exists() else []
        experience_graphs = list(GRAPH_DIR.glob("experience_graph_*.json")) if GRAPH_DIR.exists() else []
        project_records = list(PROJECT_DIR.glob("project_knowledge_*.json")) if PROJECT_DIR.exists() else []
        architecture_records = list(ARCHITECTURE_DIR.glob("architecture_memory_*.json")) if ARCHITECTURE_DIR.exists() else []

        missing = []

        if not knowledge_graphs:
            missing.append("knowledge_graph")

        if not experience_graphs:
            missing.append("experience_graph")

        if not project_records:
            missing.append("project_knowledge")

        if not architecture_records:
            missing.append("architecture_memory")

        return {
            "status": "passed" if not missing else "warning",
            "knowledge_graph_count": len(knowledge_graphs),
            "experience_graph_count": len(experience_graphs),
            "project_knowledge_count": len(project_records),
            "architecture_memory_count": len(architecture_records),
            "missing": missing,
        }


def main() -> None:
    result = LongTermDiagnostics().run()

    print("=== LongTerm Diagnostics ===")
    print(f"状態: {result['status']}")
    print(f"KnowledgeGraph数: {result['knowledge_graph_count']}")
    print(f"ExperienceGraph数: {result['experience_graph_count']}")
    print(f"ProjectKnowledge数: {result['project_knowledge_count']}")
    print(f"ArchitectureMemory数: {result['architecture_memory_count']}")
    print(f"不足候補: {len(result['missing'])}")

    for item in result["missing"]:
        print(f"- {item}")


if __name__ == "__main__":
    main()