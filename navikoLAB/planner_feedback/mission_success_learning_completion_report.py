from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def find_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("mission_self_optimization_diagnostics_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[0] if files else None

def load_json(path):
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main():
    diagnostics_path = find_latest_diagnostics()
    diagnostics = load_json(diagnostics_path)

    diagnostics_ok = diagnostics.get("MissionSelfOptimizationReady") is True
    risk_count = diagnostics.get("RiskCount", 1)

    output = {
        "status": "completed" if diagnostics_ok and risk_count == 0 else "blocked",
        "phase": "Phase17-7 Mission Success Learning Completion Report",
        "DiagnosticsFound": diagnostics_path is not None,
        "DiagnosticsConfirmed": diagnostics_ok,
        "MissionSuccessLearningCompleted": diagnostics_ok and risk_count == 0,
        "MissionSelfOptimizationReady": diagnostics.get("MissionSelfOptimizationReady", False),
        "MissionLearningMode": diagnostics.get("MissionLearningMode"),
        "Trend": diagnostics.get("Trend"),
        "SuccessRate": diagnostics.get("SuccessRate"),
        "FailureRate": diagnostics.get("FailureRate"),
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "PlannerWriteAllowed": False,
        "CapabilityRouterWriteAllowed": False,
        "ConnectorDispatcherWriteAllowed": False,
        "FileDelete": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "RiskCount": risk_count,
        "SafeToContinue": diagnostics_ok and risk_count == 0,
        "NextPhase": "Phase18 Mission Self Optimization Integration",
        "updated_at": datetime.now().isoformat(),
        "DiagnosticsPath": str(diagnostics_path) if diagnostics_path else None,
    }

    out_path = REPORT_DIR / f"mission_success_learning_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== Mission Success Learning Completion Report ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {out_path}")

if __name__ == "__main__":
    main()