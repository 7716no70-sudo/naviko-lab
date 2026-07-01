from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase38-1 Autonomous Mission Loop Builder"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
MISSION_DIR = WORKSPACE / "autonomous_mission_loop"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_phase37_completion():
    files = sorted(
        REPORT_DIR.glob("autonomous_improvement_cycle_completion_report_*.json"),
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
    MISSION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase37_path, phase37 = load_latest_phase37_completion()

    phase37_ready = bool(
        phase37
        and phase37.get("status") == "completed"
        and phase37.get("AutonomousImprovementCycleReady") is True
        and phase37.get("WorkspaceOnly") is True
        and phase37.get("OriginalWrite") is False
        and phase37.get("OriginalWriteBlocked") is True
        and phase37.get("RiskCount") == 0
        and phase37.get("SafeToContinue") is True
    )

    mission_loop = {
        "phase": PHASE,
        "MissionLoopCreated": phase37_ready,
        "MissionLoopReady": phase37_ready,
        "MissionMode": "safe_workspace_only_autonomous_mission_loop",
        "LoopSteps": [
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
        "RiskCount": 0 if phase37_ready else 1,
        "SafeToContinue": phase37_ready,
        "SourcePhase37CompletionPath": str(phase37_path) if phase37_path else None,
        "NextPhase": "Phase38-2 Autonomous Mission Loop Diagnostics"
        if phase37_ready
        else "Review Phase37 Completion Report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    mission_path = MISSION_DIR / f"autonomous_mission_loop_{ts}.json"
    mission_path.write_text(json.dumps(mission_loop, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / f"autonomous_mission_loop_builder_report_{ts}.json"
    report_path.write_text(json.dumps(mission_loop, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Autonomous Mission Loop Builder ===")
    print(f"status: {'completed' if phase37_ready else 'blocked'}")
    for key, value in mission_loop.items():
        print(f"{key}: {value}")
    print(f"保存先: {mission_path}")
    print(f"レポート保存先: {report_path}")


if __name__ == "__main__":
    main()