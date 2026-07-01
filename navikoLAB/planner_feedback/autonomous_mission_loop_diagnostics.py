from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase38-2 Autonomous Mission Loop Diagnostics"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
MISSION_DIR = WORKSPACE / "autonomous_mission_loop"
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

    mission_path, mission = load_latest_json(MISSION_DIR, "autonomous_mission_loop_*.json")

    mission_found = mission is not None
    loop_steps = mission.get("LoopSteps", []) if mission else []

    required_steps = [
        "ReceivePurpose",
        "CreateMission",
        "ObserveWorkspace",
        "AnalyzeState",
        "CreatePlan",
        "ClassifyRisk",
        "WorkspaceAction",
        "AutomaticValidation",
        "ExperienceRecord",
        "NextActionDecision",
        "HumanApprovalRequestIfNeeded",
        "CriticalBlockIfNeeded",
    ]

    missing_steps = [step for step in required_steps if step not in loop_steps]

    checks = {
        "MissionLoopFound": mission_found,
        "MissionLoopCreated": bool(mission and mission.get("MissionLoopCreated") is True),
        "MissionLoopReady": bool(mission and mission.get("MissionLoopReady") is True),
        "RequiredStepsComplete": mission_found and not missing_steps,
        "MissingStepCount": len(missing_steps),
        "MissingSteps": missing_steps,
        "AutoExecutableRiskLevels": mission.get("AutoExecutableRiskLevels", []) if mission else [],
        "ApprovalRequiredRiskLevels": mission.get("ApprovalRequiredRiskLevels", []) if mission else [],
        "BlockedRiskLevels": mission.get("BlockedRiskLevels", []) if mission else [],
        "WorkspaceOnly": bool(mission and mission.get("WorkspaceOnly") is True),
        "OriginalWrite": bool(mission and mission.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(mission and mission.get("OriginalWriteBlocked") is True),
        "OriginalAdoptionAllowed": bool(mission and mission.get("OriginalAdoptionAllowed") is True),
        "ExternalOperation": bool(mission and mission.get("ExternalOperation") is True),
        "RealGUIOperation": bool(mission and mission.get("RealGUIOperation") is True),
        "FileDelete": bool(mission and mission.get("FileDelete") is True),
        "HumanApprovalRequiredForOriginalAdoption": bool(
            mission and mission.get("HumanApprovalRequiredForOriginalAdoption") is True
        ),
        "PermissionPolicyRequired": bool(mission and mission.get("PermissionPolicyRequired") is True),
        "AutomaticValidationRequired": bool(mission and mission.get("AutomaticValidationRequired") is True),
        "RiskCount": int(mission.get("RiskCount", 999)) if mission else 999,
    }

    safe_to_continue = (
        checks["MissionLoopFound"]
        and checks["MissionLoopCreated"]
        and checks["MissionLoopReady"]
        and checks["RequiredStepsComplete"]
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
        "source_mission_path": str(mission_path) if mission_path else None,
        **checks,
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase38-3 Autonomous Mission Loop Completion Report"
        if safe_to_continue
        else "Review Phase38-1 Mission Loop Builder",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"autonomous_mission_loop_diagnostics_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Autonomous Mission Loop Diagnostics ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()