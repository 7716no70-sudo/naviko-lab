from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


PHASE = "Phase32-2 Risk Classifier Diagnostics"


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "risk_classifier"


def latest_classifier_record() -> Path | None:
    base = workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("risk_classifier_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_diagnostics(record: dict, source_path: Path | None) -> dict:
    risk_definitions = record.get("RiskDefinitions", {})
    keyword_rules = record.get("KeywordRules", {})
    sample_classifications = record.get("SampleClassifications", [])

    required_checks = {
        "RiskClassifierCreated": record.get("RiskClassifierCreated") is True,
        "RiskClassifierReady": record.get("RiskClassifierReady") is True,
        "PolicyEngineCompletionReportFound": record.get("PolicyEngineCompletionReportFound") is True,
        "PolicyEngineCompletionReportValid": record.get("PolicyEngineCompletionReportValid") is True,
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
        "RiskDefinitionCount": len(risk_definitions) == 5,
        "KeywordRulesFound": len(keyword_rules) > 0,
        "SampleClassificationsFound": len(sample_classifications) > 0,
    }

    level_results = {
        str(item.get("risk_level")): item
        for item in sample_classifications
        if "risk_level" in item
    }

    behavior_checks = {
        "Level0AutoAllowed": level_results.get("0", {}).get("auto_allowed") is True,
        "Level1AutoAllowed": level_results.get("1", {}).get("auto_allowed") is True,
        "Level2ApprovalRequired": level_results.get("2", {}).get("human_approval_required") is True,
        "Level3ApprovalRequired": level_results.get("3", {}).get("human_approval_required") is True,
        "Level4Blocked": level_results.get("4", {}).get("blocked") is True,
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
        "RiskClassifierReady": diagnostics_passed,
        "RiskLevelClassificationReady": diagnostics_passed,
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
            "Phase32-3 Risk Classifier Completion Report"
            if diagnostics_passed
            else "Fix Risk Classifier"
        ),
    }


def save_diagnostics(diagnostics: dict) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"risk_classifier_diagnostics_{timestamp}.json"
    out_path.write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_classifier_record()

    if source_path is None:
        diagnostics = {
            "status": "blocked",
            "phase": PHASE,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "SourceFound": False,
            "DiagnosticsPassed": False,
            "RiskClassifierReady": False,
            "RiskLevelClassificationReady": False,
            "RiskCount": 1,
            "SafeToContinue": False,
            "NextPhase": "Create Risk Classifier",
        }
    else:
        record = load_json(source_path)
        diagnostics = build_diagnostics(record, source_path)

    out_path = save_diagnostics(diagnostics)

    print("=== Risk Classifier Diagnostics ===")
    print(f"status: {diagnostics['status']}")
    print(f"phase: {diagnostics['phase']}")
    print(f"SourceFound: {diagnostics.get('SourceFound')}")
    print(f"DiagnosticsPassed: {diagnostics.get('DiagnosticsPassed')}")
    print(f"RiskClassifierReady: {diagnostics.get('RiskClassifierReady')}")
    print(f"RiskLevelClassificationReady: {diagnostics.get('RiskLevelClassificationReady')}")
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