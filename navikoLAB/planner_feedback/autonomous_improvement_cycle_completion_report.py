from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase37-3 Autonomous Improvement Cycle Completion Report"
ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("autonomous_improvement_cycle_diagnostics_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not files:
        return None, None

    path = files[0]
    return path, json.loads(path.read_text(encoding="utf-8"))


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    diagnostics_path, diagnostics = load_latest_diagnostics()
    diagnostics_found = diagnostics is not None

    diagnostics_confirmed = bool(
        diagnostics
        and diagnostics.get("status") == "completed"
        and diagnostics.get("SafeToContinue") is True
        and diagnostics.get("CycleReady") is True
        and diagnostics.get("WorkspaceOnly") is True
        and diagnostics.get("OriginalWrite") is False
        and diagnostics.get("OriginalWriteBlocked") is True
        and diagnostics.get("RiskCount") == 0
    )

    completion_ready = diagnostics_found and diagnostics_confirmed

    report = {
        "status": "completed" if completion_ready else "blocked",
        "phase": PHASE,
        "DiagnosticsFound": diagnostics_found,
        "DiagnosticsConfirmed": diagnostics_confirmed,
        "AutonomousImprovementCycleCompleted": completion_ready,
        "AutonomousImprovementCycleReady": completion_ready,
        "CycleMode": "safe_workspace_only_autonomous_improvement",
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "PermissionPolicyRequired": True,
        "AutomaticValidationRequired": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if completion_ready else 1,
        "SafeToContinue": completion_ready,
        "NextPhase": "Phase38 Autonomous Mission Loop" if completion_ready else "Review Phase37-2 Diagnostics",
        "source_diagnostics_path": str(diagnostics_path) if diagnostics_path else None,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"autonomous_improvement_cycle_completion_report_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Autonomous Improvement Cycle Completion Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()