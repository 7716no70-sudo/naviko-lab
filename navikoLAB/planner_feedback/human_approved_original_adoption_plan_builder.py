from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
ADOPTION_DIR = WORKSPACE_DIR / "human_approved_original_adoption"

SOURCE_PATH = ADOPTION_DIR / "human_approved_original_adoption_source.json"
OUTPUT_PATH = ADOPTION_DIR / "human_approved_original_adoption_plan.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    source = load_json(SOURCE_PATH)

    plan = {
        "status": "completed",
        "phase": "Phase25-2 Human Approved Original Adoption Plan Builder",
        "Project": "Original Naviko AI OS v2.0 Final Release",
        "AdoptionPlanStatus": "built",
        "AdoptionMode": "human_approval_required_read_only_plan",
        "SourceFound": SOURCE_PATH.exists(),
        "SourceCount": source.get("SourceCount", 0),
        "MissingSourceCount": source.get("MissingSourceCount", 0),
        "FinalReleaseReady": source.get("FinalReleaseReady") is True,
        "ArchiveReady": source.get("ArchiveReady") is True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "WorkspaceOnly": True,
        "AdoptionSteps": [
            "Confirm final release completion report",
            "Confirm optional archive completion report",
            "Require explicit human approval",
            "Require permission policy approval",
            "Keep Original write blocked until approval",
            "Run diagnostics before any adoption action",
        ],
        "SafetyPolicy": {
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "OriginalWriteBlocked": True,
            "OriginalAdoptionAllowed": False,
            "PlannerWriteAllowed": False,
            "CapabilityRouterWriteAllowed": False,
            "ConnectorDispatcherWriteAllowed": False,
            "AutoPatch": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "HumanApprovalRequired": True,
            "HumanApproved": False,
            "PermissionPolicyRequired": True,
            "PermissionPolicyApproved": False,
            "ReadOnlyReference": True,
        },
        "RiskCount": 0,
        "SafeToContinue": (
            source.get("SafeToContinue") is True
            and source.get("RiskCount") == 0
            and source.get("OriginalWrite") is False
            and source.get("OriginalWriteBlocked") is True
            and source.get("HumanApproved") is False
            and source.get("PermissionPolicyApproved") is False
        ),
        "CollectedSources": source.get("CollectedSources", {}),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approved Original Adoption Plan Builder ===")
    print(f"status: {plan['status']}")
    print(f"phase: {plan['phase']}")
    print(f"AdoptionPlanStatus: {plan['AdoptionPlanStatus']}")
    print(f"AdoptionMode: {plan['AdoptionMode']}")
    print(f"SourceFound: {plan['SourceFound']}")
    print(f"SourceCount: {plan['SourceCount']}")
    print(f"MissingSourceCount: {plan['MissingSourceCount']}")
    print(f"FinalReleaseReady: {plan['FinalReleaseReady']}")
    print(f"ArchiveReady: {plan['ArchiveReady']}")
    print(f"HumanApprovalRequired: {plan['HumanApprovalRequired']}")
    print(f"HumanApproved: {plan['HumanApproved']}")
    print(f"PermissionPolicyRequired: {plan['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {plan['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {plan['OriginalAdoptionAllowed']}")
    print(f"WorkspaceOnly: {plan['WorkspaceOnly']}")
    print(f"OriginalWrite: {plan['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {plan['OriginalWriteBlocked']}")
    print(f"RiskCount: {plan['RiskCount']}")
    print(f"SafeToContinue: {plan['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()