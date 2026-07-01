from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_FILES = {
    "HistoryFound": WORKSPACE / "mission_success_history.json",
    "StatisticsFound": WORKSPACE / "mission_success_statistics.json",
    "TrendFound": WORKSPACE / "mission_success_trend.json",
    "LongTermProfileFound": WORKSPACE / "mission_long_term_learning_profile.json",
    "HintFound": WORKSPACE / "mission_self_optimization_hint.json",
}

def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main():
    found = {name: path.exists() for name, path in REQUIRED_FILES.items()}
    required_ok = all(found.values())

    hint = load_json(REQUIRED_FILES["HintFound"])

    risk_flags = [
        hint.get("OriginalWrite") is True,
        hint.get("PlannerWriteAllowed") is True,
        hint.get("CapabilityRouterWriteAllowed") is True,
        hint.get("ConnectorDispatcherWriteAllowed") is True,
        hint.get("FileDelete") is True,
        hint.get("ExternalOperation") is True,
        hint.get("RealGUIOperation") is True,
    ]

    risk_count = sum(1 for flag in risk_flags if flag)

    output = {
        "status": "completed" if required_ok and risk_count == 0 else "blocked",
        "phase": "Phase17-6 Mission Self Optimization Diagnostics",
        **found,
        "RequiredOK": required_ok,
        "MissionSelfOptimizationReady": required_ok and risk_count == 0,
        "ReadOnlyReference": hint.get("ReadOnlyReference", False),
        "MissionLearningMode": hint.get("MissionLearningMode"),
        "Trend": hint.get("Trend"),
        "SuccessRate": hint.get("SuccessRate"),
        "FailureRate": hint.get("FailureRate"),
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": risk_count,
        "SafeToContinue": required_ok and risk_count == 0,
        "NextPhase": "Phase17-7 Mission Success Learning Completion Report",
        "updated_at": datetime.now().isoformat(),
    }

    out_path = REPORT_DIR / f"mission_self_optimization_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Self Optimization Diagnostics ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {out_path}")

if __name__ == "__main__":
    main()