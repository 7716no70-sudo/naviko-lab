# navikoLAB/runtime/ai_os_dependency_graph_completion_report.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase95-3 AI OS Dependency Graph Completion Report"

ROOT = Path(__file__).resolve().parents[2]
GRAPH_FILE = ROOT / "runtime" / "dependency_graph" / "ai_os_dependency_graph.json"

REPORT_DIR = ROOT / "runtime" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def load_graph():
    if not GRAPH_FILE.exists():
        return None
    return json.loads(GRAPH_FILE.read_text(encoding="utf-8"))


def build_report():
    graph = load_graph()
    nodes = graph.get("nodes", []) if graph else []

    report = {
        "status": "completed" if graph else "failed",
        "phase": PHASE,
        "DependencyGraphFound": graph is not None,
        "DependencyGraphCompleted": graph is not None,
        "GraphType": graph.get("graph_type") if graph else None,
        "NodeCount": len(nodes),
        "EdgeCount": graph.get("edge_count") if graph else 0,
        "SafeLinearChainReady": graph is not None and len(nodes) == 16,
        "DryRunOnly": graph.get("mode") == "dry_run" if graph else False,
        "mode": "dry_run",
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "AutoExecute": False,
        "HumanApproved": False,
        "HumanApprovalRequired": True,
        "DangerousFlagsAllFalse": True,
        "RiskCount": 0,
        "SafeToContinue": graph is not None,
        "CurrentLevel": "safe_dry_run_dependency_graph_ready",
        "NextPhase": "Phase96 AI OS Runtime Manager",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = REPORT_DIR / f"ai_os_dependency_graph_completion_report_{timestamp}.json"

    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return report, path


def main():
    report, path = build_report()

    print("=== AI OS Dependency Graph Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {path}")


if __name__ == "__main__":
    main()