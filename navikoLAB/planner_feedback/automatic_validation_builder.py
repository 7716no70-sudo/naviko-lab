from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase34-1 Automatic Validation Builder"


VALIDATION_STEPS = [
    {
        "name": "py_compile",
        "purpose": "Python構文チェックを行う。",
        "required": True,
        "auto_executable": True,
    },
    {
        "name": "diagnostics",
        "purpose": "安全状態・実行可否・RiskCountを診断する。",
        "required": True,
        "auto_executable": True,
    },
    {
        "name": "completion_report",
        "purpose": "工程完了状態を記録する。",
        "required": True,
        "auto_executable": True,
    },
    {
        "name": "rollback_decision",
        "purpose": "悪化・失敗時にロールバック要否を判定する。",
        "required": True,
        "auto_executable": True,
    },
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def autonomous_growth_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "autonomous_growth"


def validation_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "automatic_validation"


def latest_autonomous_growth_completion_report() -> Path | None:
    base = autonomous_growth_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("autonomous_growth_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_validation_record(source_path: Path | None) -> dict[str, Any]:
    growth_report_found = source_path is not None
    growth_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        growth_report_valid = (
            source.get("AutonomousGrowthCompleted") is True
            and source.get("SafeGrowthAutoExecutionReady") is True
            and source.get("SafeAutonomousGrowthAllowed") is True
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    ready = growth_report_found and growth_report_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "AutonomousGrowthCompletionReportFound": growth_report_found,
        "AutonomousGrowthCompletionReportValid": growth_report_valid,
        "SourcePath": str(source_path) if source_path else None,
        "AutomaticValidationPlanCreated": ready,
        "AutomaticValidationReady": ready,
        "ValidationMode": "safe_workspace_only_validation",
        "ValidationSteps": VALIDATION_STEPS,
        "SyntaxCheckRequired": True,
        "DiagnosticsRequired": True,
        "CompletionReportRequired": True,
        "RollbackDecisionRequired": True,
        "AutoValidationAllowed": True,
        "SafeAutonomousGrowthAllowed": True,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase34-2 Automatic Validation Diagnostics"
            if ready
            else "Fix Autonomous Growth Completion Report"
        ),
    }


def save_record(record: dict[str, Any]) -> Path:
    out_dir = validation_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"automatic_validation_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_autonomous_growth_completion_report()
    record = build_validation_record(source_path)
    out_path = save_record(record)

    print("=== Automatic Validation Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"AutonomousGrowthCompletionReportFound: {record['AutonomousGrowthCompletionReportFound']}")
    print(f"AutonomousGrowthCompletionReportValid: {record['AutonomousGrowthCompletionReportValid']}")
    print(f"AutomaticValidationPlanCreated: {record['AutomaticValidationPlanCreated']}")
    print(f"AutomaticValidationReady: {record['AutomaticValidationReady']}")
    print(f"ValidationMode: {record['ValidationMode']}")
    print(f"SyntaxCheckRequired: {record['SyntaxCheckRequired']}")
    print(f"DiagnosticsRequired: {record['DiagnosticsRequired']}")
    print(f"CompletionReportRequired: {record['CompletionReportRequired']}")
    print(f"RollbackDecisionRequired: {record['RollbackDecisionRequired']}")
    print(f"AutoValidationAllowed: {record['AutoValidationAllowed']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()