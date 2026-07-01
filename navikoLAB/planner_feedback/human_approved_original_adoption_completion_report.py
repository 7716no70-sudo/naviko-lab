from pathlib import Path
import json
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR / "workspace"
ADOPTION_DIR = WORKSPACE_DIR / "human_approved_original_adoption"

PLAN_PATH = ADOPTION_DIR / "human_approved_original_adoption_plan.json"
DIAGNOSTICS_PATH = ADOPTION_DIR / "human_approved_original_adoption_diagnostics.json"
OUTPUT_PATH = ADOPTION_DIR / "human_approved_original_adoption_completion_report.json"

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    plan_found = PLAN_PATH.exists()
    diagnostics_found = DIAGNOSTICS_PATH.exists()

    plan = load_json(PLAN_PATH) if plan_found else {}
    diagnostics = load_json(DIAGNOSTICS_PATH) if diagnostics_found else {}

    safety = plan.get("SafetyPolicy", {})

    completed = (
        plan_found
        and diagnostics_found
        and diagnostics.get("SafeToContinue") is True
        and diagnostics.get("RiskCount") == 0
        and plan.get("FinalReleaseReady") is True
        and plan.get("ArchiveReady") is True
        and plan.get("HumanApprovalRequired") is True
        and plan.get("HumanApproved") is False
        and plan.get("PermissionPolicyRequired") is True
        and plan.get("PermissionPolicyApproved") is False
        and plan.get("OriginalAdoptionAllowed") is False
        and safety.get("WorkspaceOnly") is True
        and safety.get("OriginalWrite") is False
        and safety.get("OriginalWriteBlocked") is True
    )

    result = {
        "status": "completed",
        "phase": "Phase25-4 Human Approved Original Adoption Completion Report",
        "PlanFound": plan_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics.get("SafeToContinue") is True,
        "AdoptionPreparationCompleted": completed,
        "AdoptionReadyForHumanApproval": completed,
        "Project": plan.get("Project"),
        "AdoptionPlanStatus": plan.get("AdoptionPlanStatus"),
        "AdoptionMode": plan.get("AdoptionMode"),
        "FinalReleaseReady": plan.get("FinalReleaseReady"),
        "ArchiveReady": plan.get("ArchiveReady"),
        "HumanApprovalRequired": plan.get("HumanApprovalRequired"),
        "HumanApproved": plan.get("HumanApproved"),
        "PermissionPolicyRequired": plan.get("PermissionPolicyRequired"),
        "PermissionPolicyApproved": plan.get("PermissionPolicyApproved"),
        "OriginalAdoptionAllowed": plan.get("OriginalAdoptionAllowed"),
        "WorkspaceOnly": safety.get("WorkspaceOnly"),
        "OriginalWrite": safety.get("OriginalWrite"),
        "OriginalWriteBlocked": safety.get("OriginalWriteBlocked"),
        "PlannerWriteAllowed": safety.get("PlannerWriteAllowed"),
        "CapabilityRouterWriteAllowed": safety.get("CapabilityRouterWriteAllowed"),
        "ConnectorDispatcherWriteAllowed": safety.get("ConnectorDispatcherWriteAllowed"),
        "AutoPatch": safety.get("AutoPatch"),
        "FileDelete": safety.get("FileDelete"),
        "ExternalOperation": safety.get("ExternalOperation"),
        "RealGUIOperation": safety.get("RealGUIOperation"),
        "ReadOnlyReference": safety.get("ReadOnlyReference"),
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase26 Human Approval Gate / Permission Policy Approval",
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    OUTPUT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Human Approved Original Adoption Completion Report ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"PlanFound: {result['PlanFound']}")
    print(f"DiagnosticsFound: {result['DiagnosticsFound']}")
    print(f"DiagnosticsConfirmed: {result['DiagnosticsConfirmed']}")
    print(f"AdoptionPreparationCompleted: {result['AdoptionPreparationCompleted']}")
    print(f"AdoptionReadyForHumanApproval: {result['AdoptionReadyForHumanApproval']}")
    print(f"Project: {result['Project']}")
    print(f"AdoptionPlanStatus: {result['AdoptionPlanStatus']}")
    print(f"AdoptionMode: {result['AdoptionMode']}")
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
    print(f"NextPhase: {result['NextPhase']}")
    print(f"保存先: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()