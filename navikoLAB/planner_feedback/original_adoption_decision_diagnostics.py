from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase35-2 Original Adoption Decision Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "original_adoption_decision"


def latest_decision_record() -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("original_adoption_decision_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_diagnostics(record: dict, source_path: Path | None) -> dict:
    required_checks = {
        "OriginalAdoptionDecisionCreated": record.get("OriginalAdoptionDecisionCreated") is True,
        "OriginalAdoptionDecisionReady": record.get("OriginalAdoptionDecisionReady") is True,
        "NavikoMayDecideAdoptionCandidate": record.get("NavikoMayDecideAdoptionCandidate") is True,
        "NavikoMayRequestOriginalAdoption": record.get("NavikoMayRequestOriginalAdoption") is True,
        "DecisionResult": record.get("DecisionResult") == "approval_required_before_original_adoption",
        "WorkspaceOnly": record.get("WorkspaceOnly") is True,
        "OriginalWrite": record.get("OriginalWrite") is False,
        "OriginalWriteBlocked": record.get("OriginalWriteBlocked") is True,
        "OriginalAdoptionAllowed": record.get("OriginalAdoptionAllowed") is False,
        "HumanApprovalRequired": record.get("HumanApprovalRequired") is True,
        "HumanApproved": record.get("HumanApproved") is False,
        "PermissionPolicyRequired": record.get("PermissionPolicyRequired") is True,
        "PermissionPolicyApproved": record.get("PermissionPolicyApproved") is False,
        "PlannerWriteAllowed": record.get("PlannerWriteAllowed") is False,
        "CapabilityRouterWriteAllowed": record.get("CapabilityRouterWriteAllowed") is False,
        "ConnectorDispatcherWriteAllowed": record.get("ConnectorDispatcherWriteAllowed") is False,
        "ExternalOperation": record.get("ExternalOperation") is False,
        "RealGUIOperation": record.get("RealGUIOperation") is False,
        "FileDelete": record.get("FileDelete") is False,
        "RiskCount": record.get("RiskCount") == 0,
        "SafeToContinue": record.get("SafeToContinue") is True,
    }

    diagnostics_passed = all(required_checks.values())

    return {
        "status": "completed" if diagnostics_passed else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "SourceFound": source_path is not None,
        "SourcePath": str(source_path) if source_path else None,
        "DiagnosticsPassed": diagnostics_passed,
        "RequiredChecks": required_checks,
        "OriginalAdoptionDecisionReady": diagnostics_passed,
        "NavikoSelfDecisionReady": diagnostics_passed,
        "OriginalAdoptionStillRequiresHumanApproval": True,
        "OriginalAdoptionStillRequiresPermissionPolicyApproval": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": (
            "Phase35-3 Original Adoption Decision Completion Report"
            if diagnostics_passed
            else "Fix Original Adoption Decision"
        ),
    }


def save_diagnostics(diagnostics: dict) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"original_adoption_decision_diagnostics_{timestamp}.json"
    out_path.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_decision_record()

    if source_path is None:
        diagnostics = {
            "status": "blocked",
            "phase": PHASE,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "OriginalAdoptionDecisionReady": False,
            "NavikoSelfDecisionReady": False,
            "RiskCount": 1,
            "SafeToContinue": False,
            "NextPhase": "Create Original Adoption Decision Record",
        }
    else:
        record = load_json(source_path)
        diagnostics = build_diagnostics(record, source_path)

    out_path = save_diagnostics(diagnostics)

    print("=== Original Adoption Decision Diagnostics ===")
    print(f"status: {diagnostics['status']}")
    print(f"phase: {diagnostics['phase']}")
    print(f"SourceFound: {diagnostics.get('SourceFound')}")
    print(f"DiagnosticsPassed: {diagnostics.get('DiagnosticsPassed')}")
    print(f"OriginalAdoptionDecisionReady: {diagnostics.get('OriginalAdoptionDecisionReady')}")
    print(f"NavikoSelfDecisionReady: {diagnostics.get('NavikoSelfDecisionReady')}")
    print(
        "OriginalAdoptionStillRequiresHumanApproval:",
        diagnostics.get("OriginalAdoptionStillRequiresHumanApproval"),
    )
    print(
        "OriginalAdoptionStillRequiresPermissionPolicyApproval:",
        diagnostics.get("OriginalAdoptionStillRequiresPermissionPolicyApproval"),
    )
    print(f"WorkspaceOnly: {diagnostics.get('WorkspaceOnly')}")
    print(f"OriginalWrite: {diagnostics.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {diagnostics.get('OriginalWriteBlocked')}")
    print(f"OriginalAdoptionAllowed: {diagnostics.get('OriginalAdoptionAllowed')}")
    print(f"HumanApprovalRequired: {diagnostics.get('HumanApprovalRequired')}")
    print(f"HumanApproved: {diagnostics.get('HumanApproved')}")
    print(f"PermissionPolicyRequired: {diagnostics.get('PermissionPolicyRequired')}")
    print(f"PermissionPolicyApproved: {diagnostics.get('PermissionPolicyApproved')}")
    print(f"RiskCount: {diagnostics.get('RiskCount')}")
    print(f"SafeToContinue: {diagnostics.get('SafeToContinue')}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()