from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase40-2 Long-Term Self Evolution Diagnostics"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
EVOLUTION_DIR = WORKSPACE / "long_term_self_evolution"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_json(directory: Path, pattern: str):
    files = sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None, None

    path = files[0]
    try:
        return path, json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return path, None


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    evolution_path, evolution = load_latest_json(EVOLUTION_DIR, "long_term_self_evolution_*.json")

    evolution_found = evolution is not None
    steps = evolution.get("EvolutionSteps", []) if evolution else []
    targets = evolution.get("EvolutionTargets", []) if evolution else []

    required_steps = [
        "CollectExperienceHistory",
        "AnalyzeLongTermTrend",
        "DetectRepeatedWeakness",
        "DetectRepeatedSuccessPattern",
        "CreateEvolutionCandidate",
        "ClassifyEvolutionRisk",
        "WorkspaceOnlyEvolution",
        "AutomaticValidation",
        "CreateOriginalAdoptionCandidateIfNeeded",
        "HumanApprovalRequestIfNeeded",
        "CriticalBlockIfNeeded",
    ]

    required_targets = [
        "planning_quality",
        "risk_prediction_accuracy",
        "validation_reliability",
        "experience_reuse",
        "mission_completion_rate",
        "approval_request_quality",
    ]

    missing_steps = [step for step in required_steps if step not in steps]
    missing_targets = [target for target in required_targets if target not in targets]

    checks = {
        "LongTermSelfEvolutionFound": evolution_found,
        "LongTermSelfEvolutionCreated": bool(evolution and evolution.get("LongTermSelfEvolutionCreated") is True),
        "LongTermSelfEvolutionReady": bool(evolution and evolution.get("LongTermSelfEvolutionReady") is True),
        "RequiredEvolutionStepsComplete": evolution_found and not missing_steps,
        "MissingEvolutionStepCount": len(missing_steps),
        "MissingEvolutionSteps": missing_steps,
        "RequiredEvolutionTargetsComplete": evolution_found and not missing_targets,
        "MissingEvolutionTargetCount": len(missing_targets),
        "MissingEvolutionTargets": missing_targets,
        "AutoExecutableRiskLevels": evolution.get("AutoExecutableRiskLevels", []) if evolution else [],
        "ApprovalRequiredRiskLevels": evolution.get("ApprovalRequiredRiskLevels", []) if evolution else [],
        "BlockedRiskLevels": evolution.get("BlockedRiskLevels", []) if evolution else [],
        "WorkspaceOnly": bool(evolution and evolution.get("WorkspaceOnly") is True),
        "OriginalWrite": bool(evolution and evolution.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(evolution and evolution.get("OriginalWriteBlocked") is True),
        "OriginalAdoptionAllowed": bool(evolution and evolution.get("OriginalAdoptionAllowed") is True),
        "ExternalOperation": bool(evolution and evolution.get("ExternalOperation") is True),
        "RealGUIOperation": bool(evolution and evolution.get("RealGUIOperation") is True),
        "FileDelete": bool(evolution and evolution.get("FileDelete") is True),
        "HumanApprovalRequiredForOriginalAdoption": bool(
            evolution and evolution.get("HumanApprovalRequiredForOriginalAdoption") is True
        ),
        "PermissionPolicyRequired": bool(evolution and evolution.get("PermissionPolicyRequired") is True),
        "AutomaticValidationRequired": bool(evolution and evolution.get("AutomaticValidationRequired") is True),
        "RiskCount": int(evolution.get("RiskCount", 999)) if evolution else 999,
    }

    safe_to_continue = (
        checks["LongTermSelfEvolutionFound"]
        and checks["LongTermSelfEvolutionCreated"]
        and checks["LongTermSelfEvolutionReady"]
        and checks["RequiredEvolutionStepsComplete"]
        and checks["RequiredEvolutionTargetsComplete"]
        and checks["AutoExecutableRiskLevels"] == [0, 1]
        and checks["ApprovalRequiredRiskLevels"] == [2, 3]
        and checks["BlockedRiskLevels"] == [4]
        and checks["WorkspaceOnly"]
        and not checks["OriginalWrite"]
        and checks["OriginalWriteBlocked"]
        and not checks["OriginalAdoptionAllowed"]
        and not checks["ExternalOperation"]
        and not checks["RealGUIOperation"]
        and not checks["FileDelete"]
        and checks["HumanApprovalRequiredForOriginalAdoption"]
        and checks["PermissionPolicyRequired"]
        and checks["AutomaticValidationRequired"]
        and checks["RiskCount"] == 0
    )

    report = {
        "status": "completed" if safe_to_continue else "blocked",
        "phase": PHASE,
        "source_evolution_path": str(evolution_path) if evolution_path else None,
        **checks,
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase40-3 Long-Term Self Evolution Completion Report"
        if safe_to_continue
        else "Review Phase40-1 Long-Term Self Evolution Builder",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"long_term_self_evolution_diagnostics_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Long-Term Self Evolution Diagnostics ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()