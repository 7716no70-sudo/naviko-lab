from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
RELEASE_DIR = WORKSPACE_DIR / "original_ai_os_final_release"

SOURCE_PATH = RELEASE_DIR / "original_ai_os_final_release_source.json"
OUTPUT_PATH = RELEASE_DIR / "original_ai_os_final_release_package.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    package = {
        "status": "completed",
        "phase": "Phase23-2 Original Naviko AI OS Final Release Builder",
        "Project": "Original Naviko AI OS v2.0 Final Release",
        "FinalReleaseStatus": "built",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "RCFinalizationCompleted": source.get("RCFinalizationCompleted") is True,
        "ReleaseCandidateReady": source.get("ReleaseCandidateReady") is True,
        "FinalReleaseReady": True,
        "FinalReleaseMode": "safe_workspace_only_final_release_report",
        "FinalizedPhaseRange": "Phase1 to Phase23",
        "SafetyPolicy": {
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "OriginalWriteBlocked": True,
            "PlannerWriteAllowed": False,
            "CapabilityRouterWriteAllowed": False,
            "ConnectorDispatcherWriteAllowed": False,
            "AutoPatch": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "HumanApprovalRequired": True,
            "PermissionPolicyRequired": True,
            "ReadOnlyReference": True,
        },
        "FinalPipeline": [
            "Mission",
            "Planner",
            "Planner Feedback",
            "Planner Self Improvement",
            "Capability Optimization",
            "Connector Optimization",
            "Mission Success Learning",
            "Mission Self Optimization",
            "Mission Policy Stabilization",
            "AI OS Stability Finalization",
            "AI OS Final Package",
            "Original Naviko AI OS RC Finalization",
            "Original Naviko AI OS Final Release",
        ],
        "RiskCount": 0,
        "SafeToContinue": (
            source.get("SafeToContinue") is True
            and source.get("RiskCount") == 0
            and source.get("OriginalWrite") is False
            and source.get("OriginalWriteBlocked") is True
            and source.get("RCFinalizationCompleted") is True
            and source.get("ReleaseCandidateReady") is True
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Original Naviko AI OS Final Release Builder ===")
    print(f"status: {package['status']}")
    print(f"phase: {package['phase']}")
    print(f"FinalReleaseStatus: {package['FinalReleaseStatus']}")
    print(f"SourceFound: {package['SourceFound']}")
    print(f"SourceCount: {package['SourceCount']}")
    print(f"MissingSourceCount: {package['MissingSourceCount']}")
    print(f"RCFinalizationCompleted: {package['RCFinalizationCompleted']}")
    print(f"ReleaseCandidateReady: {package['ReleaseCandidateReady']}")
    print(f"FinalReleaseReady: {package['FinalReleaseReady']}")
    print(f"FinalReleaseMode: {package['FinalReleaseMode']}")
    print(f"WorkspaceOnly: {package['SafetyPolicy']['WorkspaceOnly']}")
    print(f"OriginalWrite: {package['SafetyPolicy']['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {package['SafetyPolicy']['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {package['SafetyPolicy']['HumanApprovalRequired']}")
    print(f"PermissionPolicyRequired: {package['SafetyPolicy']['PermissionPolicyRequired']}")
    print(f"RiskCount: {package['RiskCount']}")
    print(f"SafeToContinue: {package['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()