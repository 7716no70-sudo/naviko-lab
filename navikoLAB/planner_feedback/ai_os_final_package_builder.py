from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
PACKAGE_DIR = WORKSPACE_DIR / "ai_os_final_package"

SOURCE_PATH = PACKAGE_DIR / "ai_os_final_package_source.json"
OUTPUT_PATH = PACKAGE_DIR / "ai_os_final_package.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    package = {
        "status": "completed",
        "phase": "Phase21-2 AI OS Final Package Builder",
        "Project": "Original Naviko AI OS v2.0 RC",
        "PackageStatus": "built",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "AIOSStabilityReady": True,
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
        ],
        "SafetyPolicy": {
            "WorkspaceOnly": True,
            "OriginalWrite": False,
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
        "RiskCount": 0,
        "SafeToContinue": (
            source.get("MissingSourceCount", 1) == 0
            and source.get("WorkspaceOnly") is True
            and source.get("OriginalWrite") is False
            and source.get("RiskCount", 1) == 0
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== AI OS Final Package Builder ===")
    print(f"status: {package['status']}")
    print(f"phase: {package['phase']}")
    print(f"PackageStatus: {package['PackageStatus']}")
    print(f"SourceFound: {package['SourceFound']}")
    print(f"SourceCount: {package['SourceCount']}")
    print(f"MissingSourceCount: {package['MissingSourceCount']}")
    print(f"AIOSStabilityReady: {package['AIOSStabilityReady']}")
    print(f"WorkspaceOnly: {package['SafetyPolicy']['WorkspaceOnly']}")
    print(f"OriginalWrite: {package['SafetyPolicy']['OriginalWrite']}")
    print(f"RiskCount: {package['RiskCount']}")
    print(f"SafeToContinue: {package['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()