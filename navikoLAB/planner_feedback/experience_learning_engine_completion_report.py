from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase39-3 Experience Learning Engine Completion Report"
ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("experience_learning_engine_diagnostics_*.json"),
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
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics_path, diagnostics = load_latest_diagnostics()
    diagnostics_found = diagnostics is not None

    diagnostics_confirmed = bool(
        diagnostics
        and diagnostics.get("status") == "completed"
        and diagnostics.get("ExperienceLearningEngineReady") is True
        and diagnostics.get("RequiredLearningStepsComplete") is True
        and diagnostics.get("RequiredExperienceTargetsComplete") is True
        and diagnostics.get("WorkspaceOnly") is True
        and diagnostics.get("OriginalWrite") is False
        and diagnostics.get("OriginalWriteBlocked") is True
        and diagnostics.get("OriginalAdoptionAllowed") is False
        and diagnostics.get("ExternalOperation") is False
        and diagnostics.get("RealGUIOperation") is False
        and diagnostics.get("FileDelete") is False
        and diagnostics.get("HumanApprovalRequiredForOriginalAdoption") is True
        and diagnostics.get("PermissionPolicyRequired") is True
        and diagnostics.get("AutomaticValidationRequired") is True
        and diagnostics.get("RiskCount") == 0
        and diagnostics.get("SafeToContinue") is True
    )

    completed = diagnostics_found and diagnostics_confirmed

    report = {
        "status": "completed" if completed else "blocked",
        "phase": PHASE,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics_confirmed,
        "ExperienceLearningEngineCompleted": completed,
        "ExperienceLearningEngineReady": completed,
        "LearningMode": "safe_workspace_only_experience_learning",
        "LearningScope": [
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
        "RiskCount": 0 if completed else 1,
        "SafeToContinue": completed,
        "NextPhase": "Phase40 Long-Term Self Evolution"
        if completed
        else "Review Phase39-2 Diagnostics",
        "source_diagnostics_path": str(diagnostics_path) if diagnostics_path else None,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"experience_learning_engine_completion_report_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Experience Learning Engine Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()