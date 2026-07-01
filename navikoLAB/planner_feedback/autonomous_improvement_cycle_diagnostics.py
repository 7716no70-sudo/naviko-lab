from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase37-2 Autonomous Improvement Cycle Diagnostics"
ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
CYCLE_DIR = WORKSPACE / "autonomous_improvement_cycle"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_json(directory: Path):
    if not directory.exists():
        return None, None

    files = sorted(directory.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        return None, None

    path = files[0]
    try:
        return path, json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return path, None


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    source_path, source = load_latest_json(CYCLE_DIR)

    source_found = source is not None

    checks = {
        "AutonomousImprovementCycleFound": source_found,
        "CycleReady": bool(source and source.get("AutonomousImprovementCycleReady") is True),
        "SafeAutonomousGrowthAllowed": bool(source and source.get("SafeAutonomousGrowthAllowed") is True),
        "AutomaticValidationRequired": bool(source and source.get("AutomaticValidationRequired") is True),
        "HumanApprovalRequired": bool(source and source.get("HumanApprovalRequiredForOriginalAdoption") is True),
        "HumanApproved": bool(source and source.get("HumanApproved") is True),
        "PermissionPolicyApproved": bool(source and source.get("PermissionPolicyApproved") is True),
        "OriginalWrite": bool(source and source.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(source and source.get("OriginalWriteBlocked") is True),
        "OriginalAdoptionAllowed": bool(source and source.get("OriginalAdoptionAllowed") is True),
        "WorkspaceOnly": bool(source and source.get("WorkspaceOnly") is True),
        "ExternalOperation": bool(source and source.get("ExternalOperation") is True),
        "RealGUIOperation": bool(source and source.get("RealGUIOperation") is True),
        "FileDelete": bool(source and source.get("FileDelete") is True),
        "RiskCount": int(source.get("RiskCount", 999)) if source else 999,
    }

    risk_count = checks["RiskCount"]

    safe_to_continue = (
        checks["AutonomousImprovementCycleFound"]
        and checks["CycleReady"]
        and checks["SafeAutonomousGrowthAllowed"]
        and checks["AutomaticValidationRequired"]
        and checks["HumanApprovalRequired"]
        and checks["OriginalWriteBlocked"]
        and checks["WorkspaceOnly"]
        and not checks["HumanApproved"]
        and not checks["PermissionPolicyApproved"]
        and not checks["OriginalWrite"]
        and not checks["OriginalAdoptionAllowed"]
        and not checks["ExternalOperation"]
        and not checks["RealGUIOperation"]
        and not checks["FileDelete"]
        and risk_count == 0
    )

    report = {
        "status": "completed" if safe_to_continue else "blocked",
        "phase": PHASE,
        "source_path": str(source_path) if source_path else None,
        **checks,
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase37-3 Autonomous Improvement Cycle Completion Report"
        if safe_to_continue
        else "Review Phase37-1 source report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"autonomous_improvement_cycle_diagnostics_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Autonomous Improvement Cycle Diagnostics ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()