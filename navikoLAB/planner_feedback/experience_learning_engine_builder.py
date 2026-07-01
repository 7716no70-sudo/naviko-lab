from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase39-1 Experience Learning Engine Builder"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
EXPERIENCE_DIR = WORKSPACE / "experience_learning_engine"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_phase38_completion():
    files = sorted(
        REPORT_DIR.glob("autonomous_mission_loop_completion_report_*.json"),
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
    EXPERIENCE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase38_path, phase38 = load_latest_phase38_completion()

    phase38_ready = bool(
        phase38
        and phase38.get("status") == "completed"
        and phase38.get("AutonomousMissionLoopReady") is True
        and phase38.get("WorkspaceOnly") is True
        and phase38.get("OriginalWrite") is False
        and phase38.get("OriginalWriteBlocked") is True
        and phase38.get("RiskCount") == 0
        and phase38.get("SafeToContinue") is True
    )

    engine = {
        "phase": PHASE,
        "ExperienceLearningEngineCreated": phase38_ready,
        "ExperienceLearningEngineReady": phase38_ready,
        "LearningMode": "safe_workspace_only_experience_learning",
        "LearningSteps": [
            "CollectMissionResult",
            "JudgeSuccessFailure",
            "AnalyzeCause",
            "ExtractReusableExperience",
            "CreateImprovementHint",
            "SaveExperience",
            "ConnectToNextMission",
        ],
        "ExperienceTargets": [
            "mission_success",
            "mission_failure",
            "validation_result",
            "risk_classification_result",
            "human_approval_result",
            "workspace_improvement_result",
        ],
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
        "RiskCount": 0 if phase38_ready else 1,
        "SafeToContinue": phase38_ready,
        "SourcePhase38CompletionPath": str(phase38_path) if phase38_path else None,
        "NextPhase": "Phase39-2 Experience Learning Engine Diagnostics"
        if phase38_ready
        else "Review Phase38 Completion Report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    engine_path = EXPERIENCE_DIR / f"experience_learning_engine_{ts}.json"
    engine_path.write_text(json.dumps(engine, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / f"experience_learning_engine_builder_report_{ts}.json"
    report_path.write_text(json.dumps(engine, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Experience Learning Engine Builder ===")
    print(f"status: {'completed' if phase38_ready else 'blocked'}")
    for key, value in engine.items():
        print(f"{key}: {value}")
    print(f"保存先: {engine_path}")
    print(f"レポート保存先: {report_path}")


if __name__ == "__main__":
    main()