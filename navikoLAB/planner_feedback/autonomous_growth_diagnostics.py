from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase33-2 Autonomous Growth Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "autonomous_growth"


def latest_growth_record() -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("autonomous_growth_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_diagnostics(record: dict, source_path: Path | None) -> dict:
    required_checks = {
        "AutonomousGrowthPlanCreated": record.get("AutonomousGrowthPlanCreated") is True,
        "AutonomousGrowthReady": record.get("AutonomousGrowthReady") is True,
        "AutoExecuteAllowedRiskLevels": record.get("AutoExecuteAllowedRiskLevels") == [0, 1],
        "ApprovalRequiredRiskLevels": record.get("ApprovalRequiredRiskLevels") == [2, 3],
        "BlockedRiskLevels": record.get("BlockedRiskLevels") == [4],
        "SafeAutonomousGrowthAllowed": record.get("SafeAutonomousGrowthAllowed") is True,
        "DangerousOperationRequiresHumanApproval": record.get("DangerousOperationRequiresHumanApproval") is True,
        "IllegalOrHarmfulOperationBlocked": record.get("IllegalOrHarmfulOperationBlocked") is True,
        "WorkspaceOnly": record.get("WorkspaceOnly") is True,
        "OriginalWrite": record.get("OriginalWrite") is False,
        "OriginalWriteBlocked": record.get("OriginalWriteBlocked") is True,
        "OriginalAdoptionAllowed": record.get("OriginalAdoptionAllowed") is False,
        "ExternalOperation": record.get("ExternalOperation") is False,
        "RealGUIOperation": record.get("RealGUIOperation") is False,
        "FileDelete": record.get("FileDelete") is False,
        "RiskCount": record.get("RiskCount") == 0,
        "SafeToContinue": record.get("SafeToContinue") is True,
    }

    safe_growth_actions = record.get("SafeGrowthActions", [])
    approval_required_actions = record.get("ApprovalRequiredActions", [])
    blocked_actions = record.get("BlockedActions", [])

    behavior_checks = {
        "SafeGrowthActionsFound": len(safe_growth_actions) > 0,
        "ApprovalRequiredActionsFound": len(approval_required_actions) > 0,
        "BlockedActionsFound": len(blocked_actions) > 0,
        "AllSafeGrowthActionsAutoAllowed": all(
            action.get("auto_execute_allowed") is True
            and action.get("risk_level") in [0, 1]
            for action in safe_growth_actions
        ),
        "AllApprovalRequiredActionsNeedApproval": all(
            action.get("auto_execute_allowed") is False
            and action.get("human_approval_required") is True
            and action.get("risk_level") in [2, 3]
            for action in approval_required_actions
        ),
        "AllBlockedActionsBlocked": all(
            action.get("auto_execute_allowed") is False
            and action.get("blocked") is True
            and action.get("risk_level") == 4
            for action in blocked_actions
        ),
    }

    diagnostics_passed = all(required_checks.values()) and all(behavior_checks.values())

    return {
        "status": "completed" if diagnostics_passed else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "SourceFound": source_path is not None,
        "SourcePath": str(source_path) if source_path else None,
        "DiagnosticsPassed": diagnostics_passed,
        "RequiredChecks": required_checks,
        "BehaviorChecks": behavior_checks,
        "AutonomousGrowthReady": diagnostics_passed,
        "SafeAutonomousGrowthAllowed": True,
        "SafeGrowthAutoExecutionReady": diagnostics_passed,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if diagnostics_passed else 1,
        "SafeToContinue": diagnostics_passed,
        "NextPhase": (
            "Phase33-3 Autonomous Growth Completion Report"
            if diagnostics_passed
            else "Fix Autonomous Growth Plan"
        ),
    }


def save_diagnostics(diagnostics: dict) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"autonomous_growth_diagnostics_{timestamp}.json"
    out_path.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_growth_record()

    if source_path is None:
        diagnostics = {
            "status": "blocked",
            "phase": PHASE,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "AutonomousGrowthReady": False,
            "SafeGrowthAutoExecutionReady": False,
            "RiskCount": 1,
            "SafeToContinue": False,
            "NextPhase": "Create Autonomous Growth Plan",
        }
    else:
        record = load_json(source_path)
        diagnostics = build_diagnostics(record, source_path)

    out_path = save_diagnostics(diagnostics)

    print("=== Autonomous Growth Diagnostics ===")
    print(f"status: {diagnostics['status']}")
    print(f"phase: {diagnostics['phase']}")
    print(f"SourceFound: {diagnostics.get('SourceFound')}")
    print(f"DiagnosticsPassed: {diagnostics.get('DiagnosticsPassed')}")
    print(f"AutonomousGrowthReady: {diagnostics.get('AutonomousGrowthReady')}")
    print(f"SafeAutonomousGrowthAllowed: {diagnostics.get('SafeAutonomousGrowthAllowed')}")
    print(f"SafeGrowthAutoExecutionReady: {diagnostics.get('SafeGrowthAutoExecutionReady')}")
    print(
        "DangerousOperationRequiresHumanApproval:",
        diagnostics.get("DangerousOperationRequiresHumanApproval"),
    )
    print(f"IllegalOrHarmfulOperationBlocked: {diagnostics.get('IllegalOrHarmfulOperationBlocked')}")
    print(f"WorkspaceOnly: {diagnostics.get('WorkspaceOnly')}")
    print(f"OriginalWrite: {diagnostics.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {diagnostics.get('OriginalWriteBlocked')}")
    print(f"OriginalAdoptionAllowed: {diagnostics.get('OriginalAdoptionAllowed')}")
    print(f"RiskCount: {diagnostics.get('RiskCount')}")
    print(f"SafeToContinue: {diagnostics.get('SafeToContinue')}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()