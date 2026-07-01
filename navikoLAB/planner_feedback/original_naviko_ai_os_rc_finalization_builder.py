from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
RC_DIR = WORKSPACE_DIR / "original_ai_os_rc_finalization"

SOURCE_PATH = RC_DIR / "original_ai_os_rc_finalization_source.json"
OUTPUT_PATH = RC_DIR / "original_ai_os_rc_finalization_package.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    package = {
        "status": "completed",
        "phase": "Phase22-2 Original Naviko AI OS RC Finalization Builder",
        "Project": "Original Naviko AI OS v2.0 RC",
        "RCFinalizationStatus": "built",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "FinalPackageReady": source.get("FinalPackageReady") is True,
        "ReleaseCandidateReady": True,
        "ReleaseCandidateMode": "safe_read_only_rc_finalization",
        "FinalizedPhaseRange": "Phase1 to Phase22",
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
        ],
        "RiskCount": 0,
        "SafeToContinue": (
            source.get("SafeToContinue") is True
            and source.get("RiskCount") == 0
            and source.get("OriginalWrite") is False
            and source.get("OriginalWriteBlocked") is True
            and source.get("FinalPackageReady") is True
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Original Naviko AI OS RC Finalization Builder ===")
    print(f"status: {package['status']}")
    print(f"phase: {package['phase']}")
    print(f"RCFinalizationStatus: {package['RCFinalizationStatus']}")
    print(f"SourceFound: {package['SourceFound']}")
    print(f"SourceCount: {package['SourceCount']}")
    print(f"MissingSourceCount: {package['MissingSourceCount']}")
    print(f"FinalPackageReady: {package['FinalPackageReady']}")
    print(f"ReleaseCandidateReady: {package['ReleaseCandidateReady']}")
    print(f"ReleaseCandidateMode: {package['ReleaseCandidateMode']}")
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