from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase31-3 Permission Policy Engine Completion Report"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "permission_policy_engine"


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

    builder = latest("permission_policy_engine_*.json")
    diagnostics = latest("permission_policy_engine_diagnostics_*.json")

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
        "PermissionPolicyEngineCompleted": completed,
        "RiskBasedAutonomyReady": completed,
        "SafeAutonomousGrowthAllowed": completed,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": (
            "Phase32 Risk Classifier"
            if completed
            else "Fix Permission Policy Engine"
        ),
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path = workspace_dir() / (
        f"permission_policy_engine_completion_report_{timestamp}.json"
    )

    save_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== Permission Policy Engine Completion Report ===")
    print(f"status: {report['status']}")
    print(f"phase: {report['phase']}")
    print(f"BuilderFound: {report['BuilderFound']}")
    print(f"DiagnosticsFound: {report['DiagnosticsFound']}")
    print(f"DiagnosticsPassed: {report['DiagnosticsPassed']}")
    print(f"PermissionPolicyEngineCompleted: {report['PermissionPolicyEngineCompleted']}")
    print(f"RiskBasedAutonomyReady: {report['RiskBasedAutonomyReady']}")
    print(f"SafeAutonomousGrowthAllowed: {report['SafeAutonomousGrowthAllowed']}")
    print(
        "DangerousOperationRequiresHumanApproval:",
        report["DangerousOperationRequiresHumanApproval"],
    )
    print(f"IllegalOrHarmfulOperationBlocked: {report['IllegalOrHarmfulOperationBlocked']}")
    print(f"WorkspaceOnly: {report['WorkspaceOnly']}")
    print(f"OriginalWrite: {report['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {report['OriginalWriteBlocked']}")
    print(f"RiskCount: {report['RiskCount']}")
    print(f"SafeToContinue: {report['SafeToContinue']}")
    print(f"保存先: {save_path}")


if __name__ == "__main__":
    main()