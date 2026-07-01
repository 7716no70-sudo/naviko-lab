from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase30-1 Final Original Adoption Readiness Builder"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def authorization_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "original_adoption_final_authorization"


def readiness_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "final_original_adoption_readiness"


def latest_authorization_completion_report() -> Path | None:
    base = authorization_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("original_adoption_final_authorization_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_readiness(source_path: Path | None) -> dict:
    completion_report_found = source_path is not None
    completion_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        completion_report_valid = (
            source.get("OriginalAdoptionFinalAuthorizationCompleted") is True
            and source.get("ReadyForNextPhase") is True
            and source.get("WorkspaceOnly") is True
            and source.get("OriginalWrite") is False
            and source.get("OriginalAdoptionAllowed") is False
            and source.get("HumanApproved") is False
            and source.get("PermissionPolicyApproved") is False
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    ready = completion_report_found and completion_report_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "AuthorizationCompletionReportFound": completion_report_found,
        "AuthorizationCompletionReportValid": completion_report_valid,
        "SourcePath": str(source_path) if source_path else None,
        "FinalOriginalAdoptionReadinessCreated": ready,
        "FinalOriginalAdoptionReady": ready,
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
        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase30-2 Final Original Adoption Readiness Diagnostics"
            if ready
            else "Fix Original Adoption Final Authorization Completion Report"
        ),
    }


def save_readiness(record: dict) -> Path:
    out_dir = readiness_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"final_original_adoption_readiness_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_authorization_completion_report()
    record = build_readiness(source_path)
    out_path = save_readiness(record)

    print("=== Final Original Adoption Readiness Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"AuthorizationCompletionReportFound: {record['AuthorizationCompletionReportFound']}")
    print(f"AuthorizationCompletionReportValid: {record['AuthorizationCompletionReportValid']}")
    print(f"FinalOriginalAdoptionReadinessCreated: {record['FinalOriginalAdoptionReadinessCreated']}")
    print(f"FinalOriginalAdoptionReady: {record['FinalOriginalAdoptionReady']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"HumanApprovalRequired: {record['HumanApprovalRequired']}")
    print(f"HumanApproved: {record['HumanApproved']}")
    print(f"PermissionPolicyRequired: {record['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {record['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()