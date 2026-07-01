from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase36-1 Human Approval Request Builder"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def decision_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "original_adoption_decision"


def approval_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "human_approval_request"


def latest_decision_completion_report() -> Path | None:
    base = decision_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("original_adoption_decision_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_request(source_path: Path | None) -> dict[str, Any]:
    decision_report_found = source_path is not None
    decision_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        decision_report_valid = (
            source.get("OriginalAdoptionDecisionCompleted") is True
            and source.get("NavikoSelfDecisionReady") is True
            and source.get("NavikoMayRequestOriginalAdoption") is True
            and source.get("OriginalAdoptionAllowed") is False
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    ready = decision_report_found and decision_report_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "OriginalAdoptionDecisionCompletionReportFound": decision_report_found,
        "OriginalAdoptionDecisionCompletionReportValid": decision_report_valid,
        "SourcePath": str(source_path) if source_path else None,
        "HumanApprovalRequestCreated": ready,
        "HumanApprovalRequestReady": ready,
        "RequestType": "original_adoption_human_approval_required",
        "RequestReason": (
            "Naviko may request Original adoption, but Original write requires "
            "creator approval before any adoption is allowed."
        ),
        "NavikoMayRequestOriginalAdoption": True,
        "HumanApprovalRequired": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "WorkspaceOnly": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase36-2 Human Approval Request Diagnostics"
            if ready
            else "Fix Original Adoption Decision Completion Report"
        ),
    }


def save_request(record: dict[str, Any]) -> Path:
    out_dir = approval_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"human_approval_request_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_decision_completion_report()
    record = build_request(source_path)
    out_path = save_request(record)

    print("=== Human Approval Request Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(
        "OriginalAdoptionDecisionCompletionReportFound:",
        record["OriginalAdoptionDecisionCompletionReportFound"],
    )
    print(
        "OriginalAdoptionDecisionCompletionReportValid:",
        record["OriginalAdoptionDecisionCompletionReportValid"],
    )
    print(f"HumanApprovalRequestCreated: {record['HumanApprovalRequestCreated']}")
    print(f"HumanApprovalRequestReady: {record['HumanApprovalRequestReady']}")
    print(f"NavikoMayRequestOriginalAdoption: {record['NavikoMayRequestOriginalAdoption']}")
    print(f"HumanApprovalRequired: {record['HumanApprovalRequired']}")
    print(f"HumanApproved: {record['HumanApproved']}")
    print(f"PermissionPolicyRequired: {record['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {record['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()