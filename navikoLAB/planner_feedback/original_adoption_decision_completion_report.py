from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase35-3 Original Adoption Decision Completion Report"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "original_adoption_decision"


def latest(pattern: str) -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    files = sorted(
        base.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[0] if files else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    workspace_dir().mkdir(parents=True, exist_ok=True)

    builder = latest("original_adoption_decision_*.json")
    diagnostics = latest("original_adoption_decision_diagnostics_*.json")

    builder_found = builder is not None
    diagnostics_found = diagnostics is not None

    diagnostics_passed = False
    if diagnostics_found:
        diagnostics_json = load_json(diagnostics)
        diagnostics_passed = diagnostics_json.get("DiagnosticsPassed") is True

    completed = builder_found and diagnostics_found and diagnostics_passed

    report = {
        "status": "completed" if completed else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "BuilderFound": builder_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsPassed": diagnostics_passed,
        "OriginalAdoptionDecisionCompleted": completed,
        "NavikoSelfDecisionReady": completed,
        "NavikoMayDecideAdoptionCandidate": completed,
        "NavikoMayRequestOriginalAdoption": completed,
        "OriginalAdoptionStillRequiresHumanApproval": True,
        "OriginalAdoptionStillRequiresPermissionPolicyApproval": True,
        "DecisionResult": "approval_required_before_original_adoption",
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
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": (
            "Phase36 Human Approval"
            if completed
            else "Fix Original Adoption Decision"
        ),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = workspace_dir() / f"original_adoption_decision_completion_report_{timestamp}.json"

    save_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Original Adoption Decision Completion Report ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"BuilderFound: {report['BuilderFound']}")
    print(f"DiagnosticsFound: {report['DiagnosticsFound']}")
    print(f"DiagnosticsPassed: {report['DiagnosticsPassed']}")
    print(f"OriginalAdoptionDecisionCompleted: {report['OriginalAdoptionDecisionCompleted']}")
    print(f"NavikoSelfDecisionReady: {report['NavikoSelfDecisionReady']}")
    print(f"NavikoMayDecideAdoptionCandidate: {report['NavikoMayDecideAdoptionCandidate']}")
    print(f"NavikoMayRequestOriginalAdoption: {report['NavikoMayRequestOriginalAdoption']}")
    print(
        "OriginalAdoptionStillRequiresHumanApproval:",
        report["OriginalAdoptionStillRequiresHumanApproval"],
    )
    print(
        "OriginalAdoptionStillRequiresPermissionPolicyApproval:",
        report["OriginalAdoptionStillRequiresPermissionPolicyApproval"],
    )
    print(f"DecisionResult: {report['DecisionResult']}")
    print(f"WorkspaceOnly: {report['WorkspaceOnly']}")
    print(f"OriginalWrite: {report['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {report['OriginalWriteBlocked']}")
    print(f"OriginalAdoptionAllowed: {report['OriginalAdoptionAllowed']}")
    print(f"HumanApprovalRequired: {report['HumanApprovalRequired']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(f"PermissionPolicyRequired: {report['PermissionPolicyRequired']}")
    print(f"PermissionPolicyApproved: {report['PermissionPolicyApproved']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"保存先: {save_path}")


if __name__ == "__main__":
    main()