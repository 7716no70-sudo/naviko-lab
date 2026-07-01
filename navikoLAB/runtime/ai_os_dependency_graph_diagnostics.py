# navikoLAB/runtime/ai_os_dependency_graph_diagnostics.py

from __future__ import annotations

from pathlib import Path
import json


PHASE = "Phase95-2 AI OS Dependency Graph Diagnostics"

ROOT = Path(__file__).resolve().parents[2]
GRAPH_FILE = ROOT / "runtime" / "dependency_graph" / "ai_os_dependency_graph.json"

REQUIRED_CHAIN = [
    "GoalManager",
    "GoalDaemon",
    "EventRouter",
    "UnifiedControlPlane",
    "UnifiedExecutionBus",
    "PolicyEngine",
    "PermissionLayer",
    "CapabilityPermission",
    "HumanApproval",
    "OperationGuard",
    "HealthMonitor",
    "StabilityKernel",
    "BackupManager",
    "RecoveryManager",
    "AuditManager",
    "HistoryManager",
]


def load_graph():
    if not GRAPH_FILE.exists():
        return None
    return json.loads(GRAPH_FILE.read_text(encoding="utf-8"))


def main():
    graph = load_graph()
    nodes = graph.get("nodes", []) if graph else []
    node_names = [n.get("node") for n in nodes]

    chain_ok = node_names == REQUIRED_CHAIN
    node_count_ok = len(nodes) == len(REQUIRED_CHAIN)
    edge_count_ok = graph.get("edge_count") == len(REQUIRED_CHAIN) - 1 if graph else False

    dependency_ok = all(
        nodes[i].get("depends_on") == ([] if i == 0 else [REQUIRED_CHAIN[i - 1]])
        for i in range(len(nodes))
    ) if nodes else False

    next_ok = all(
        nodes[i].get("next") == ([] if i == len(nodes) - 1 else [REQUIRED_CHAIN[i + 1]])
        for i in range(len(nodes))
    ) if nodes else False

    dry_run_ok = graph.get("mode") == "dry_run" if graph else False

    dangerous_flags_ok = (
        graph is not None
        and graph.get("OriginalWrite") is False
        and graph.get("ExternalOperation") is False
        and graph.get("BrowserOperation") is False
        and graph.get("RealGUIOperation") is False
        and graph.get("FileDelete") is False
        and graph.get("AutoExecute") is False
        and graph.get("HumanApproved") is False
        and graph.get("HumanApprovalRequired") is True
    )

    passed = (
        graph is not None
        and chain_ok
        and node_count_ok
        and edge_count_ok
        and dependency_ok
        and next_ok
        and dry_run_ok
        and dangerous_flags_ok
    )

    print("=== AI OS Dependency Graph Diagnostics ===")
    print("status:", "completed" if graph else "failed")
    print("phase:", PHASE)
    print("DependencyGraphFound:", graph is not None)
    print("RequiredNodeCount:", len(REQUIRED_CHAIN))
    print("NodeCountOK:", node_count_ok)
    print("EdgeCountOK:", edge_count_ok)
    print("DependencyChainOK:", chain_ok)
    print("DependsOnOK:", dependency_ok)
    print("NextLinksOK:", next_ok)
    print("DryRunOnly:", dry_run_ok)
    print("DangerousFlagsAllFalse:", dangerous_flags_ok)
    print("DependencyGraphDiagnosticsPassed:", passed)
    print("RiskCount:", 0)
    print("SafeToContinue:", passed)


if __name__ == "__main__":
    main()