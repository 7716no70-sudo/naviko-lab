from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase35-1 Original Adoption Decision Builder"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validation_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "automatic_validation"


def decision_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "original_adoption_decision"


def latest_validation_completion_report() -> Path | None:
    base = validation_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("automatic_validation_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_decision_record(source_path: Path | None) -> dict[str, Any]:
    validation_report_found = source_path is not None
    validation_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        validation_report_valid = (
            source.get("AutomaticValidationCompleted") is True
            and source.get("AutomaticValidationReady") is True
            and source.get("AutoValidationAllowed") is True
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    ready = validation_report_found and validation_report_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "AutomaticValidationCompletionReportFound": validation_report_found,
        "AutomaticValidationCompletionReportValid": validation_report_valid,
        "SourcePath": str(source_path) if source_path else None,

        "OriginalAdoptionDecisionCreated": ready,
        "OriginalAdoptionDecisionReady": ready,

        "DecisionMode": "self_decision_with_human_approval_for_original_write",
        "NavikoMayDecideAdoptionCandidate": True,
        "NavikoMayRequestOriginalAdoption": True,

        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,

        "HumanApprovalRequired": True,
        "HumanApproved": False,

        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,

        "DecisionResult": "approval_required_before_original_adoption",
        "DecisionReason": (
            "Automatic validation is ready, but Original adoption requires "
            "human approval and permission policy approval before any write."
        ),

        "WorkspaceOnly": True,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,

        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase35-2 Original Adoption Decision Diagnostics"
            if ready
            else "Fix Automatic Validation Completion Report"
        ),
    }


def save_record(record: dict[str, Any]) -> Path:
    out_dir = decision_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"original_adoption_decision_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_validation_completion_report()
    record = build_decision_record(source_path)
    out_path = save_record(record)

    print("=== Original Adoption Decision Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(
        "AutomaticValidationCompletionReportFound:",
        record["AutomaticValidationCompletionReportFound"],
    )
    print(
        "AutomaticValidationCompletionReportValid:",
        record["AutomaticValidationCompletionReportValid"],
    )
    print(f"OriginalAdoptionDecisionCreated: {record['OriginalAdoptionDecisionCreated']}")
    print(f"OriginalAdoptionDecisionReady: {record['OriginalAdoptionDecisionReady']}")
    print(f"DecisionMode: {record['DecisionMode']}")
    print(f"NavikoMayDecideAdoptionCandidate: {record['NavikoMayDecideAdoptionCandidate']}")
    print(f"NavikoMayRequestOriginalAdoption: {record['NavikoMayRequestOriginalAdoption']}")
    print(f"DecisionResult: {record['DecisionResult']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"HumanApprovalRequired: {record['HumanApprovalRequired']}")
    print(f"HumanApproved: {record['HumanApproved']}")
    print(f"PermissionPolicyRequired: {record['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {record['PermissionPolicyApproved']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()