# navikoLAB/runtime/ai_os_dependency_graph.py

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json


PHASE = "Phase95-1 AI OS Dependency Graph"

ROOT = Path(__file__).resolve().parents[2]

GRAPH_DIR = ROOT / "runtime" / "dependency_graph"
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

GRAPH_FILE = GRAPH_DIR / "ai_os_dependency_graph.json"


DEPENDENCY_CHAIN = [
    {
        "node": "GoalManager",
        "depends_on": [],
        "next": ["GoalDaemon"],
    },
    {
        "node": "GoalDaemon",
        "depends_on": ["GoalManager"],
        "next": ["EventRouter"],
    },
    {
        "node": "EventRouter",
        "depends_on": ["GoalDaemon"],
        "next": ["UnifiedControlPlane"],
    },
    {
        "node": "UnifiedControlPlane",
        "depends_on": ["EventRouter"],
        "next": ["UnifiedExecutionBus"],
    },
    {
        "node": "UnifiedExecutionBus",
        "depends_on": ["UnifiedControlPlane"],
        "next": ["PolicyEngine"],
    },
    {
        "node": "PolicyEngine",
        "depends_on": ["UnifiedExecutionBus"],
        "next": ["PermissionLayer"],
    },
    {
        "node": "PermissionLayer",
        "depends_on": ["PolicyEngine"],
        "next": ["CapabilityPermission"],
    },
    {
        "node": "CapabilityPermission",
        "depends_on": ["PermissionLayer"],
        "next": ["HumanApproval"],
    },
    {
        "node": "HumanApproval",
        "depends_on": ["CapabilityPermission"],
        "next": ["OperationGuard"],
    },
    {
        "node": "OperationGuard",
        "depends_on": ["HumanApproval"],
        "next": ["HealthMonitor"],
    },
    {
        "node": "HealthMonitor",
        "depends_on": ["OperationGuard"],
        "next": ["StabilityKernel"],
    },
    {
        "node": "StabilityKernel",
        "depends_on": ["HealthMonitor"],
        "next": ["BackupManager"],
    },
    {
        "node": "BackupManager",
        "depends_on": ["StabilityKernel"],
        "next": ["RecoveryManager"],
    },
    {
        "node": "RecoveryManager",
        "depends_on": ["BackupManager"],
        "next": ["AuditManager"],
    },
    {
        "node": "AuditManager",
        "depends_on": ["RecoveryManager"],
        "next": ["HistoryManager"],
    },
    {
        "node": "HistoryManager",
        "depends_on": ["AuditManager"],
        "next": [],
    },
]


def build_dependency_graph():
    graph = {
        "status": "completed",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "node_count": len(DEPENDENCY_CHAIN),
        "edge_count": sum(len(node["next"]) for node in DEPENDENCY_CHAIN),
        "graph_type": "safe_linear_ai_os_dependency_graph",
        "nodes": DEPENDENCY_CHAIN,
        "mode": "dry_run",
        "OriginalWrite": False,
        "ExternalOperation": False,
        "BrowserOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "AutoExecute": False,
        "HumanApproved": False,
        "HumanApprovalRequired": True,
        "RiskCount": 0,
        "SafeToContinue": True,
        "CurrentLevel": "safe_dry_run_dependency_graph_ready",
    }

    GRAPH_FILE.write_text(
        json.dumps(graph, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return graph


def main():
    graph = build_dependency_graph()

    print("=== AI OS Dependency Graph ===")
    print("status:", graph["status"])
    print("phase:", graph["phase"])
    print("GraphType:", graph["graph_type"])
    print("NodeCount:", graph["node_count"])
    print("EdgeCount:", graph["edge_count"])
    print("DependencyGraphCreated:", True)
    print("DependencyGraphPath:", GRAPH_FILE)
    print("CurrentLevel:", graph["CurrentLevel"])
    print("RiskCount:", graph["RiskCount"])
    print("SafeToContinue:", graph["SafeToContinue"])


if __name__ == "__main__":
    main()