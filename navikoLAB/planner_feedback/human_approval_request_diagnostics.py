from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase36-2 Human Approval Request Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "human_approval_request"


def latest_request_record() -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("human_approval_request_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_diagnostics(record: dict, source_path: Path | None) -> dict:
    required_checks = {
        "HumanApprovalRequestCreated": record.get("HumanApprovalRequestCreated") is True,
        "HumanApprovalRequestReady": record.get("HumanApprovalRequestReady") is True,
        "NavikoMayRequestOriginalAdoption": record.get("NavikoMayRequestOriginalAdoption") is True,
        "HumanApprovalRequired": record.get("HumanApprovalRequired") is True,
        "HumanApproved": record.get("HumanApproved") is False,
        "PermissionPolicyRequired": record.get("PermissionPolicyRequired") is True,
        "PermissionPolicyApproved": record.get("PermissionPolicyApproved") is False,
        "OriginalAdoptionAllowed": record.get("OriginalAdoptionAllowed") is False,
        "OriginalWrite": record.get("OriginalWrite") is False,
        "OriginalWriteBlocked": record.get("OriginalWriteBlocked") is True,
        "WorkspaceOnly": record.get("WorkspaceOnly") is True,
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
        "HumanApprovalRequestReady": diagnostics_passed,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "WorkspaceOnly": True,
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": (
            "Phase36-3 Human Approval Request Completion Report"
            if diagnostics_passed
            else "Fix Human Approval Request"
        ),
    }


def save_diagnostics(diagnostics: dict) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"human_approval_request_diagnostics_{timestamp}.json"
    out_path.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_request_record()

    if source_path is None:
        diagnostics = {
            "status": "blocked",
            "phase": PHASE,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "HumanApprovalRequestReady": False,
            "RiskCount": 1,
            "SafeToContinue": False,
            "NextPhase": "Create Human Approval Request",
        }
    else:
        record = load_json(source_path)
        diagnostics = build_diagnostics(record, source_path)

    out_path = save_diagnostics(diagnostics)

    print("=== Human Approval Request Diagnostics ===")
    print(f"status: {diagnostics['status']}")
    print(f"phase: {diagnostics['phase']}")
    print(f"SourceFound: {diagnostics.get('SourceFound')}")
    print(f"DiagnosticsPassed: {diagnostics.get('DiagnosticsPassed')}")
    print(f"HumanApprovalRequestReady: {diagnostics.get('HumanApprovalRequestReady')}")
    print(f"HumanApprovalRequired: {diagnostics.get('HumanApprovalRequired')}")
    print(f"HumanApproved: {diagnostics.get('HumanApproved')}")
    print(f"PermissionPolicyRequired: {diagnostics.get('PermissionPolicyRequired')}")
    print(f"PermissionPolicyApproved: {diagnostics.get('PermissionPolicyApproved')}")
    print(f"OriginalAdoptionAllowed: {diagnostics.get('OriginalAdoptionAllowed')}")
    print(f"OriginalWrite: {diagnostics.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {diagnostics.get('OriginalWriteBlocked')}")
    print(f"WorkspaceOnly: {diagnostics.get('WorkspaceOnly')}")
    print(f"RiskCount: {diagnostics.get('RiskCount')}")
    print(f"SafeToContinue: {diagnostics.get('SafeToContinue')}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()