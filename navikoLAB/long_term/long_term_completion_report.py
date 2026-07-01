from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from navikoLAB.long_term.long_term_diagnostics import LongTermDiagnostics


ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "long_term" / "reports"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics = LongTermDiagnostics().run()

    result = {
        "status": "completed" if diagnostics["status"] == "passed" else "warning",
        "stage": "第35工程 長期Knowledge / KnowledgeGraph / ExperienceGraph / ProjectKnowledge / ArchitectureMemory",
        "diagnostics": diagnostics,
        "completed_items": [
            "KnowledgeGraph",
            "ExperienceGraph",
            "ProjectKnowledge",
            "ArchitectureMemory",
            "LongTermDiagnostics",
            "LongTermCompletionReport",
        ],
        "external_storage": {
            "external_hdd_required_later": True,
            "external_hdd_connected_now": False,
            "migration_ready": True,
        },
        "next_stage": "第36工程 最終統合診断 / ProjectCompletionScore / FinalRoadmap",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }

    output = REPORT_DIR / f"long_term_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== LongTerm Completion Report ===")
    print(f"状態: {result['status']}")
    print(f"工程: {result['stage']}")
    print(f"KnowledgeGraph数: {diagnostics['knowledge_graph_count']}")
    print(f"ExperienceGraph数: {diagnostics['experience_graph_count']}")
    print(f"ProjectKnowledge数: {diagnostics['project_knowledge_count']}")
    print(f"ArchitectureMemory数: {diagnostics['architecture_memory_count']}")
    print(f"不足候補: {len(diagnostics['missing'])}")
    print(f"外付けHDD移行準備: {result['external_storage']['migration_ready']}")
    print(f"保存先: {output}")
    print(f"次工程: {result['next_stage']}")


if __name__ == "__main__":
    main()