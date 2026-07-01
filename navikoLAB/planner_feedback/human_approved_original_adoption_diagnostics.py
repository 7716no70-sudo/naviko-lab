from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
ADOPTION_DIR = WORKSPACE_DIR / "human_approved_original_adoption"

PLAN_PATH = ADOPTION_DIR / "human_approved_original_adoption_plan.json"
OUTPUT_PATH = ADOPTION_DIR / "human_approved_original_adoption_diagnostics.json"

REQUIRED_KEYS = [
    "status",
    "phase",
    "Project",
    "AdoptionPlanStatus",
    "AdoptionMode",
    "SourceFound",
    "SourceCount",
    "MissingSourceCount",
    "FinalReleaseReady",
    "ArchiveReady",
    "HumanApprovalRequired",
    "HumanApproved",
    "PermissionPolicyRequired",
    "PermissionPolicyApproved",
    "OriginalAdoptionAllowed",
    "OriginalWrite",
    "OriginalWriteBlocked",
    "WorkspaceOnly",
    "AdoptionSteps",
    "SafetyPolicy",
    "RiskCount",
    "SafeToContinue",
    "CollectedSources",
]

REQUIRED_SAFETY = {
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
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    plan_found = PLAN_PATH.exists()
    plan = load_json(PLAN_PATH) if plan_found else {}

    missing_keys = [key for key in REQUIRED_KEYS if key not in plan]

    safety = plan.get("SafetyPolicy", {})
    safety_mismatches = {
        key: {"expected": expected, "actual": safety.get(key)}
        for key, expected in REQUIRED_SAFETY.items()
        if safety.get(key) != expected
    }

    diagnostics_ok = (
        plan_found
        and not missing_keys
        and not safety_mismatches
        and plan.get("AdoptionPlanStatus") == "built"
        and plan.get("AdoptionMode") == "human_approval_required_read_only_plan"
        and plan.get("SourceFound") is True
        and plan.get("SourceCount") == 2
        and plan.get("MissingSourceCount") == 0
        and plan.get("FinalReleaseReady") is True
        and plan.get("ArchiveReady") is True
        and plan.get("HumanApprovalRequired") is True
        and plan.get("HumanApproved") is False
        and plan.get("PermissionPolicyRequired") is True
        and plan.get("PermissionPolicyApproved") is False
        and plan.get("OriginalAdoptionAllowed") is False
        and plan.get("OriginalWrite") is False
        and plan.get("OriginalWriteBlocked") is True
        and plan.get("WorkspaceOnly") is True
        and plan.get("RiskCount") == 0
        and plan.get("SafeToContinue") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase25-3 Human Approved Original Adoption Diagnostics",
        "PlanFound": plan_found,
        "RequiredKeysOK": len(missing_keys) == 0,
        "MissingKeys": missing_keys,
        "SafetyPolicyOK": len(safety_mismatches) == 0,
        "SafetyMismatches": safety_mismatches,
        "AdoptionPlanStatusOK": plan.get("AdoptionPlanStatus") == "built",
        "AdoptionModeOK": plan.get("AdoptionMode") == "human_approval_required_read_only_plan",
        "SourceFound": plan.get("SourceFound") is True,
        "SourceCountOK": plan.get("SourceCount") == 2,
        "MissingSourceCountOK": plan.get("MissingSourceCount") == 0,
        "FinalReleaseReady": plan.get("FinalReleaseReady") is True,
        "ArchiveReady": plan.get("ArchiveReady") is True,
        "HumanApprovalRequired": plan.get("HumanApprovalRequired"),
        "HumanApproved": plan.get("HumanApproved"),
        "PermissionPolicyRequired": plan.get("PermissionPolicyRequired"),
        "PermissionPolicyApproved": plan.get("PermissionPolicyApproved"),
        "OriginalAdoptionAllowed": plan.get("OriginalAdoptionAllowed"),
        "WorkspaceOnly": plan.get("WorkspaceOnly"),
        "OriginalWrite": plan.get("OriginalWrite"),
        "OriginalWriteBlocked": plan.get("OriginalWriteBlocked"),
        "RiskCount": 0 if diagnostics_ok else 1,
        "SafeToContinue": diagnostics_ok,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approved Original Adoption Diagnostics ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PlanFound: {result['PlanFound']}")
    print(f"RequiredKeysOK: {result['RequiredKeysOK']}")
    print(f"SafetyPolicyOK: {result['SafetyPolicyOK']}")
    print(f"AdoptionPlanStatusOK: {result['AdoptionPlanStatusOK']}")
    print(f"AdoptionModeOK: {result['AdoptionModeOK']}")
    print(f"SourceFound: {result['SourceFound']}")
    print(f"SourceCountOK: {result['SourceCountOK']}")
    print(f"MissingSourceCountOK: {result['MissingSourceCountOK']}")
    print(f"FinalReleaseReady: {result['FinalReleaseReady']}")
    print(f"ArchiveReady: {result['ArchiveReady']}")
    print(f"HumanApprovalRequired: {result['HumanApprovalRequired']}")
    print(f"HumanApproved: {result['HumanApproved']}")
    print(f"PermissionPolicyRequired: {result['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {result['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {result['OriginalAdoptionAllowed']}")
    print(f"WorkspaceOnly: {result['WorkspaceOnly']}")
    print(f"OriginalWrite: {result['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {result['OriginalWriteBlocked']}")
    print(f"RiskCount: {result['RiskCount']}")
    print(f"SafeToContinue: {result['SafeToContinue']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()