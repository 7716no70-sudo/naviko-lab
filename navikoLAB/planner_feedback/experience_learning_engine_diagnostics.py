from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase39-2 Experience Learning Engine Diagnostics"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
EXPERIENCE_DIR = WORKSPACE / "experience_learning_engine"
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

    engine_path, engine = load_latest_json(EXPERIENCE_DIR, "experience_learning_engine_*.json")

    engine_found = engine is not None
    learning_steps = engine.get("LearningSteps", []) if engine else []
    targets = engine.get("ExperienceTargets", []) if engine else []

    required_steps = [
        "CollectMissionResult",
        "JudgeSuccessFailure",
        "AnalyzeCause",
        "ExtractReusableExperience",
        "CreateImprovementHint",
        "SaveExperience",
        "ConnectToNextMission",
    ]

    required_targets = [
        "mission_success",
        "mission_failure",
        "validation_result",
        "risk_classification_result",
        "human_approval_result",
        "workspace_improvement_result",
    ]

    missing_steps = [step for step in required_steps if step not in learning_steps]
    missing_targets = [target for target in required_targets if target not in targets]

    checks = {
        "ExperienceLearningEngineFound": engine_found,
        "ExperienceLearningEngineCreated": bool(engine and engine.get("ExperienceLearningEngineCreated") is True),
        "ExperienceLearningEngineReady": bool(engine and engine.get("ExperienceLearningEngineReady") is True),
        "RequiredLearningStepsComplete": engine_found and not missing_steps,
        "MissingLearningStepCount": len(missing_steps),
        "MissingLearningSteps": missing_steps,
        "RequiredExperienceTargetsComplete": engine_found and not missing_targets,
        "MissingExperienceTargetCount": len(missing_targets),
        "MissingExperienceTargets": missing_targets,
        "WorkspaceOnly": bool(engine and engine.get("WorkspaceOnly") is True),
        "OriginalWrite": bool(engine and engine.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(engine and engine.get("OriginalWriteBlocked") is True),
        "OriginalAdoptionAllowed": bool(engine and engine.get("OriginalAdoptionAllowed") is True),
        "ExternalOperation": bool(engine and engine.get("ExternalOperation") is True),
        "RealGUIOperation": bool(engine and engine.get("RealGUIOperation") is True),
        "FileDelete": bool(engine and engine.get("FileDelete") is True),
        "HumanApprovalRequiredForOriginalAdoption": bool(
            engine and engine.get("HumanApprovalRequiredForOriginalAdoption") is True
        ),
        "PermissionPolicyRequired": bool(engine and engine.get("PermissionPolicyRequired") is True),
        "AutomaticValidationRequired": bool(engine and engine.get("AutomaticValidationRequired") is True),
        "RiskCount": int(engine.get("RiskCount", 999)) if engine else 999,
    }

    safe_to_continue = (
        checks["ExperienceLearningEngineFound"]
        and checks["ExperienceLearningEngineCreated"]
        and checks["ExperienceLearningEngineReady"]
        and checks["RequiredLearningStepsComplete"]
        and checks["RequiredExperienceTargetsComplete"]
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
        "source_engine_path": str(engine_path) if engine_path else None,
        **checks,
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase39-3 Experience Learning Engine Completion Report"
        if safe_to_continue
        else "Review Phase39-1 Experience Learning Engine Builder",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"experience_learning_engine_diagnostics_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Experience Learning Engine Diagnostics ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()