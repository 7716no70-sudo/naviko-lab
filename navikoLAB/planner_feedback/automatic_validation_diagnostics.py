from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase34-2 Automatic Validation Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "automatic_validation"


def latest_validation_record() -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("automatic_validation_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_diagnostics(record: dict, source_path: Path | None) -> dict:
    validation_steps = record.get("ValidationSteps", [])

    required_checks = {
        "AutomaticValidationPlanCreated": record.get("AutomaticValidationPlanCreated") is True,
        "AutomaticValidationReady": record.get("AutomaticValidationReady") is True,
        "SyntaxCheckRequired": record.get("SyntaxCheckRequired") is True,
        "DiagnosticsRequired": record.get("DiagnosticsRequired") is True,
        "CompletionReportRequired": record.get("CompletionReportRequired") is True,
        "RollbackDecisionRequired": record.get("RollbackDecisionRequired") is True,
        "AutoValidationAllowed": record.get("AutoValidationAllowed") is True,
        "WorkspaceOnly": record.get("WorkspaceOnly") is True,
        "OriginalWrite": record.get("OriginalWrite") is False,
        "OriginalWriteBlocked": record.get("OriginalWriteBlocked") is True,
        "OriginalAdoptionAllowed": record.get("OriginalAdoptionAllowed") is False,
        "ExternalOperation": record.get("ExternalOperation") is False,
        "RealGUIOperation": record.get("RealGUIOperation") is False,
        "FileDelete": record.get("FileDelete") is False,
        "RiskCount": record.get("RiskCount") == 0,
        "SafeToContinue": record.get("SafeToContinue") is True,
        "ValidationStepsFound": len(validation_steps) > 0,
    }

    step_names = {step.get("name") for step in validation_steps}
    behavior_checks = {
        "PyCompileStepFound": "py_compile" in step_names,
        "DiagnosticsStepFound": "diagnostics" in step_names,
        "CompletionReportStepFound": "completion_report" in step_names,
        "RollbackDecisionStepFound": "rollback_decision" in step_names,
        "AllStepsRequired": all(step.get("required") is True for step in validation_steps),
        "AllStepsAutoExecutable": all(
            step.get("auto_executable") is True for step in validation_steps
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
        "AutomaticValidationReady": diagnostics_passed,
        "AutoValidationAllowed": True,
        "SyntaxCheckRequired": True,
        "DiagnosticsRequired": True,
        "CompletionReportRequired": True,
        "RollbackDecisionRequired": True,
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
            "Phase34-3 Automatic Validation Completion Report"
            if diagnostics_passed
            else "Fix Automatic Validation Plan"
        ),
    }


def save_diagnostics(diagnostics: dict) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"automatic_validation_diagnostics_{timestamp}.json"
    out_path.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_validation_record()

    if source_path is None:
        diagnostics = {
            "status": "blocked",
            "phase": PHASE,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "AutomaticValidationReady": False,
            "RiskCount": 1,
            "SafeToContinue": False,
            "NextPhase": "Create Automatic Validation Plan",
        }
    else:
        record = load_json(source_path)
        diagnostics = build_diagnostics(record, source_path)

    out_path = save_diagnostics(diagnostics)

    print("=== Automatic Validation Diagnostics ===")
    print(f"status: {diagnostics['status']}")
    print(f"phase: {diagnostics['phase']}")
    print(f"SourceFound: {diagnostics.get('SourceFound')}")
    print(f"DiagnosticsPassed: {diagnostics.get('DiagnosticsPassed')}")
    print(f"AutomaticValidationReady: {diagnostics.get('AutomaticValidationReady')}")
    print(f"AutoValidationAllowed: {diagnostics.get('AutoValidationAllowed')}")
    print(f"SyntaxCheckRequired: {diagnostics.get('SyntaxCheckRequired')}")
    print(f"DiagnosticsRequired: {diagnostics.get('DiagnosticsRequired')}")
    print(f"CompletionReportRequired: {diagnostics.get('CompletionReportRequired')}")
    print(f"RollbackDecisionRequired: {diagnostics.get('RollbackDecisionRequired')}")
    print(f"WorkspaceOnly: {diagnostics.get('WorkspaceOnly')}")
    print(f"OriginalWrite: {diagnostics.get('OriginalWrite')}")
    print(f"OriginalWriteBlocked: {diagnostics.get('OriginalWriteBlocked')}")
    print(f"OriginalAdoptionAllowed: {diagnostics.get('OriginalAdoptionAllowed')}")
    print(f"RiskCount: {diagnostics.get('RiskCount')}")
    print(f"SafeToContinue: {diagnostics.get('SafeToContinue')}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()