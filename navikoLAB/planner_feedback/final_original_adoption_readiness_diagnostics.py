from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

PHASE = "Phase30-2 Final Original Adoption Readiness Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return (
        project_root()
        / "navikoLAB"
        / "workspace"
        / "final_original_adoption_readiness"
    )


def latest_record() -> Path | None:
    if not workspace_dir().exists():
        return None

    files = sorted(
        workspace_dir().glob("final_original_adoption_readiness_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[0] if files else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build(record: dict, source_path: Path) -> dict:

    checks = {
        "FinalOriginalAdoptionReadinessCreated":
            record.get("FinalOriginalAdoptionReadinessCreated") is True,

        "FinalOriginalAdoptionReady":
            record.get("FinalOriginalAdoptionReady") is True,

        "WorkspaceOnly":
            record.get("WorkspaceOnly") is True,

        "OriginalWrite":
            record.get("OriginalWrite") is False,

        "OriginalWriteBlocked":
            record.get("OriginalWriteBlocked") is True,

        "HumanApprovalRequired":
            record.get("HumanApprovalRequired") is True,

        "HumanApproved":
            record.get("HumanApproved") is False,

        "PermissionPolicyRequired":
            record.get("PermissionPolicyRequired") is True,

        "PermissionPolicyApproved":
            record.get("PermissionPolicyApproved") is False,

        "OriginalAdoptionAllowed":
            record.get("OriginalAdoptionAllowed") is False,

        "PlannerWriteAllowed":
            record.get("PlannerWriteAllowed") is False,

        "CapabilityRouterWriteAllowed":
            record.get("CapabilityRouterWriteAllowed") is False,

        "ConnectorDispatcherWriteAllowed":
            record.get("ConnectorDispatcherWriteAllowed") is False,

        "ExternalOperation":
            record.get("ExternalOperation") is False,

        "RealGUIOperation":
            record.get("RealGUIOperation") is False,

        "FileDelete":
            record.get("FileDelete") is False,

        "RiskCount":
            record.get("RiskCount") == 0,

        "SafeToContinue":
            record.get("SafeToContinue") is True,
    }

    passed = all(checks.values())

    return {
        "status": "completed" if passed else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "SourceFound": True,
        "SourcePath": str(source_path),
        "DiagnosticsPassed": passed,
        "RequiredChecks": checks,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if passed else 1,
        "SafeToContinue": passed,
        "NextPhase":
            "Phase30-3 Final Original Adoption Readiness Completion Report"
            if passed else
            "Fix Final Original Adoption Readiness",
    }


def main():

    src = latest_record()

    if src is None:
        result = {
            "status": "blocked",
            "phase": PHASE,
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "RiskCount": 1,
            "SafeToContinue": False,
        }
    else:
        result = build(load_json(src), src)

    workspace_dir().mkdir(parents=True, exist_ok=True)

    save = workspace_dir() / (
        f"final_original_adoption_readiness_diagnostics_"
        f"{datetime.now():%Y%m%d_%H%M%S}.json"
    )

    save.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Final Original Adoption Readiness Diagnostics ===")
    print(f"status: {result['status']}")
    print(f"phase: {result['phase']}")
    print(f"SourceFound: {result.get('SourceFound')}")
    print(f"DiagnosticsPassed: {result.get('DiagnosticsPassed')}")
    print(f"WorkspaceOnly: {result.get('WorkspaceOnly')}")
    print(f"OriginalWrite: {result.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {result.get('OriginalWriteBlocked')}")
    print(f"HumanApprovalRequired: {result.get('HumanApprovalRequired')}")
    print(f"HumanApproved: {result.get('HumanApproved')}")
    print(f"PermissionPolicyRequired: {result.get('PermissionPolicyRequired')}")
    print(f"PermissionPolicyApproved: {result.get('PermissionPolicyApproved')}")
    print(f"OriginalAdoptionAllowed: {result.get('OriginalAdoptionAllowed')}")
    print(f"RiskCount: {result.get('RiskCount')}")
    print(f"SafeToContinue: {result.get('SafeToContinue')}")
    print(f"保存先: {save}")


if __name__ == "__main__":
    main()