from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase31-2 Permission Policy Engine Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "permission_policy_engine"


def latest_engine_record() -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("permission_policy_engine_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_diagnostics(record: dict, source_path: Path | None) -> dict:
    risk_levels = record.get("RiskLevels", {})
    action_rules = record.get("ActionRules", {})
    sample_results = record.get("SampleResults", [])

    required_checks = {
        "PermissionPolicyEngineCreated": record.get("PermissionPolicyEngineCreated") is True,
        "SafeAutonomousGrowthAllowed": record.get("SafeAutonomousGrowthAllowed") is True,
        "DangerousOperationRequiresHumanApproval": record.get("DangerousOperationRequiresHumanApproval") is True,
        "IllegalOrHarmfulOperationBlocked": record.get("IllegalOrHarmfulOperationBlocked") is True,
        "WorkspaceOnly": record.get("WorkspaceOnly") is True,
        "OriginalWrite": record.get("OriginalWrite") is False,
        "OriginalWriteBlocked": record.get("OriginalWriteBlocked") is True,
        "ExternalOperation": record.get("ExternalOperation") is False,
        "RealGUIOperation": record.get("RealGUIOperation") is False,
        "FileDelete": record.get("FileDelete") is False,
        "RiskCount": record.get("RiskCount") == 0,
        "SafeToContinue": record.get("SafeToContinue") is True,
        "RiskLevelCount": len(risk_levels) == 5,
        "ActionRulesFound": len(action_rules) > 0,
        "SampleResultsFound": len(sample_results) > 0,
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
        "PermissionPolicyEngineReady": diagnostics_passed,
        "RiskBasedAutonomyReady": diagnostics_passed,
        "SafeAutonomousGrowthAllowed": True,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": (
            "Phase31-3 Permission Policy Engine Completion Report"
            if diagnostics_passed
            else "Fix Permission Policy Engine"
        ),
    }


def save_diagnostics(diagnostics: dict) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"permission_policy_engine_diagnostics_{timestamp}.json"
    out_path.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_engine_record()

    if source_path is None:
        diagnostics = {
            "status": "blocked",
            "phase": PHASE,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "PermissionPolicyEngineReady": False,
            "RiskBasedAutonomyReady": False,
            "RiskCount": 1,
            "SafeToContinue": False,
            "NextPhase": "Create Permission Policy Engine",
        }
    else:
        record = load_json(source_path)
        diagnostics = build_diagnostics(record, source_path)

    out_path = save_diagnostics(diagnostics)

    print("=== Permission Policy Engine Diagnostics ===")
    print(f"status: {diagnostics['status']}")
    print(f"phase: {diagnostics['phase']}")
    print(f"SourceFound: {diagnostics.get('SourceFound')}")
    print(f"DiagnosticsPassed: {diagnostics.get('DiagnosticsPassed')}")
    print(f"PermissionPolicyEngineReady: {diagnostics.get('PermissionPolicyEngineReady')}")
    print(f"RiskBasedAutonomyReady: {diagnostics.get('RiskBasedAutonomyReady')}")
    print(f"SafeAutonomousGrowthAllowed: {diagnostics.get('SafeAutonomousGrowthAllowed')}")
    print(
        "DangerousOperationRequiresHumanApproval:",
        diagnostics.get("DangerousOperationRequiresHumanApproval"),
    )
    print(f"IllegalOrHarmfulOperationBlocked: {diagnostics.get('IllegalOrHarmfulOperationBlocked')}")
    print(f"WorkspaceOnly: {diagnostics.get('WorkspaceOnly')}")
    print(f"OriginalWrite: {diagnostics.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {diagnostics.get('OriginalWriteBlocked')}")
    print(f"RiskCount: {diagnostics.get('RiskCount')}")
    print(f"SafeToContinue: {diagnostics.get('SafeToContinue')}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()