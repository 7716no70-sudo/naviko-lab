from pathlib import Path

from navikoLAB.bridge.bridge_diagnostics import run_bridge_diagnostics
from navikoLAB.approval.approval_diagnostics import run_approval_diagnostics
from navikoLAB.release.release_candidate_manager import ReleaseCandidateManager

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_FILE = ROOT.parent / "naviko" / "naviko.py"


def run_release_diagnostics():
    manager = ReleaseCandidateManager()
    manifest, manifest_path = manager.create_manifest()

    bridge = run_bridge_diagnostics()
    approval = run_approval_diagnostics()

    includes = manifest["includes"]
    safety = manifest["safety_policy"]
    connectors = manifest["connector_status"]

    checks = {
        "OriginalExists": ORIGINAL_FILE.exists(),
        "ManifestCreated": manifest_path.exists(),
        "BridgeDiagnostics": bridge["status"] == "passed",
        "ApprovalDiagnostics": approval["status"] == "passed",
        "MissionManagerIncluded": includes.get("MissionManager") is True,
        "TaskPlannerIncluded": includes.get("TaskPlanner") is True,
        "CapabilityRouterIncluded": includes.get("CapabilityRouter") is True,
        "ConnectorDispatcherIncluded": includes.get("ConnectorDispatcher") is True,
        "SearchDispatcherIncluded": includes.get("SearchDispatcher") is True,
        "BrowserConnectorIncluded": includes.get("BrowserConnector") is True,
        "DeepSearchEngineIncluded": includes.get("DeepSearchEngine") is True,
        "KnowledgeBaseIncluded": includes.get("KnowledgeBase") is True,
        "ExperienceManagerIncluded": includes.get("ExperienceManager") is True,
        "KnowledgeReflectionIncluded": includes.get("KnowledgeReflection") is True,
        "AutoImprovementSuggestionIncluded": includes.get("AutoImprovementSuggestion") is True,
        "AutoRefactoringPlanIncluded": includes.get("AutoRefactoringPlan") is True,
        "OriginalBridgeIncluded": includes.get("OriginalNavikoBridge") is True,
        "HumanApprovalIncluded": includes.get("HumanApprovalWorkflow") is True,
        "FinalSafetyIncluded": includes.get("FinalSafetyAudit") is True,
        "LongTermKnowledgeIncluded": includes.get("LongTermKnowledge") is True,
        "DirectWriteFalse": safety.get("original_direct_write") is False,
        "AutoApplyFalse": safety.get("auto_apply") is False,
        "HumanApprovalRequired": safety.get("human_approval_required") is True,
        "BackupRequired": safety.get("backup_required") is True,
        "SyntaxCheckRequired": safety.get("syntax_check_required") is True,
        "StartupCheckRequired": safety.get("startup_check_required") is True,
        "RollbackRequired": safety.get("rollback_required") is True,
        "BrowserReady": connectors.get("Browser") == "ready",
    }

    passed = sum(1 for v in checks.values() if v)
    failed = len(checks) - passed

    return {
        "status": "passed" if failed == 0 else "failed",
        "check_count": len(checks),
        "passed": passed,
        "failed": failed,
        "checks": checks,
        "version": manifest["version"],
        "manifest_path": str(manifest_path),
        "bridge_status": bridge["status"],
        "approval_status": approval["status"],
    }


if __name__ == "__main__":
    result = run_release_diagnostics()

    print("=== Release Diagnostics ===")
    print("状態:", result["status"])
    print("Version:", result["version"])
    print("確認項目:", result["check_count"])
    print("通過:", result["passed"])
    print("失敗:", result["failed"])

    for name, ok in result["checks"].items():
        print(f"- {name}: {'OK' if ok else 'NG'}")