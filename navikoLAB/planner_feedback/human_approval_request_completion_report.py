from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

PHASE = "Phase36-3 Human Approval Request Completion Report"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return (
        project_root()
        / "navikoLAB"
        / "workspace"
        / "human_approval_request"
    )


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

    builder = latest("human_approval_request_*.json")
    diagnostics = latest("human_approval_request_diagnostics_*.json")

    builder_found = builder is not None
    diagnostics_found = diagnostics is not None

    diagnostics_passed = False

    if diagnostics_found:
        diagnostics_json = load_json(diagnostics)
        diagnostics_passed = (
            diagnostics_json.get("DiagnosticsPassed") is True
        )

    completed = (
        builder_found
        and diagnostics_found
        and diagnostics_passed
    )

    report = {
        "status": "completed" if completed else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),

        "BuilderFound": builder_found,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsPassed": diagnostics_passed,

        "HumanApprovalRequestCompleted": completed,
        "HumanApprovalRequestReady": completed,

        "HumanApprovalRequired": True,
        "HumanApproved": False,

        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,

        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,

        "WorkspaceOnly": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,

        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,

        "NextPhase": (
            "Phase37 Autonomous Improvement Cycle"
            if completed
            else "Fix Human Approval Request"
        ),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    save_path = (
        workspace_dir()
        / f"human_approval_request_completion_report_{timestamp}.json"
    )

    save_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=== Human Approval Request Completion Report ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"BuilderFound: {report['BuilderFound']}")
    print(f"DiagnosticsFound: {report['DiagnosticsFound']}")
    print(f"DiagnosticsPassed: {report['DiagnosticsPassed']}")
    print(
        "HumanApprovalRequestCompleted:",
        report["HumanApprovalRequestCompleted"],
    )
    print(
        "HumanApprovalRequestReady:",
        report["HumanApprovalRequestReady"],
    )
    print(f"HumanApprovalRequired: {report['HumanApprovalRequired']}")
    print(f"HumanApproved: {report['HumanApproved']}")
    print(
        f"PermissionPolicyRequired: {report['PermissionPolicyRequired']}"
    )
    print(
        f"PermissionPolicyApproved: {report['PermissionPolicyApproved']}"
    )
    print(f"OriginalWrite: {report['OriginalWrite']}")
    print(
        f"OriginalWriteBlocked: {report['OriginalWriteBlocked']}"
    )
    print(
        f"OriginalAdoptionAllowed: {report['OriginalAdoptionAllowed']}"
    )
    print(f"WorkspaceOnly: {report['WorkspaceOnly']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"保存先: {save_path}")


if __name__ == "__main__":
    main()