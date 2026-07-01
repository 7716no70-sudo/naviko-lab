from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase40-1 Long-Term Self Evolution Builder"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
EVOLUTION_DIR = WORKSPACE / "long_term_self_evolution"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_phase39_completion():
    files = sorted(
        REPORT_DIR.glob("experience_learning_engine_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not files:
        return None, None

    path = files[0]
    try:
        return path, json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return path, None


def main():
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase39_path, phase39 = load_latest_phase39_completion()

    phase39_ready = bool(
        phase39
        and phase39.get("status") == "completed"
        and phase39.get("ExperienceLearningEngineReady") is True
        and phase39.get("WorkspaceOnly") is True
        and phase39.get("OriginalWrite") is False
        and phase39.get("OriginalWriteBlocked") is True
        and phase39.get("RiskCount") == 0
        and phase39.get("SafeToContinue") is True
    )

    evolution = {
        "phase": PHASE,
        "LongTermSelfEvolutionCreated": phase39_ready,
        "LongTermSelfEvolutionReady": phase39_ready,
        "EvolutionMode": "safe_workspace_only_long_term_self_evolution",
        "EvolutionSteps": [
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
        ],
        "EvolutionTargets": [
            "planning_quality",
            "risk_prediction_accuracy",
            "validation_reliability",
            "experience_reuse",
            "mission_completion_rate",
            "approval_request_quality",
        ],
        "AutoExecutableRiskLevels": [0, 1],
        "ApprovalRequiredRiskLevels": [2, 3],
        "BlockedRiskLevels": [4],
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "PermissionPolicyRequired": True,
        "AutomaticValidationRequired": True,
        "RiskCount": 0 if phase39_ready else 1,
        "SafeToContinue": phase39_ready,
        "SourcePhase39CompletionPath": str(phase39_path) if phase39_path else None,
        "NextPhase": "Phase40-2 Long-Term Self Evolution Diagnostics"
        if phase39_ready
        else "Review Phase39 Completion Report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    evolution_path = EVOLUTION_DIR / f"long_term_self_evolution_{ts}.json"
    evolution_path.write_text(json.dumps(evolution, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / f"long_term_self_evolution_builder_report_{ts}.json"
    report_path.write_text(json.dumps(evolution, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Long-Term Self Evolution Builder ===")
    print(f"status: {'completed' if phase39_ready else 'blocked'}")
    for key, value in evolution.items():
        print(f"{key}: {value}")
    print(f"保存先: {evolution_path}")
    print(f"レポート保存先: {report_path}")


if __name__ == "__main__":
    main()