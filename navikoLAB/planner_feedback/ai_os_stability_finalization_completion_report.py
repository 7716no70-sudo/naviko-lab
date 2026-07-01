from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def find_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("ai_os_stability_diagnostics_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return files[0] if files else None

def load_json(path):
    if not path or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    diagnostics_path = find_latest_diagnostics()
    diagnostics = load_json(diagnostics_path)

    diagnostics_ok = diagnostics.get("AIOSStabilityReady") is True
    risk_count = diagnostics.get("RiskCount", 1)

    output = {
        "status": "completed" if diagnostics_ok and risk_count == 0 else "blocked",
        "phase": "Phase20-4 AI OS Stability Finalization Completion Report",
        "DiagnosticsFound": diagnostics_path is not None,
        "DiagnosticsConfirmed": diagnostics_ok,
        "AIOSStabilityFinalizationCompleted": diagnostics_ok and risk_count == 0,
        "AIOSStabilityReady": diagnostics.get("AIOSStabilityReady"),
        "StabilityMode": diagnostics.get("StabilityMode"),
        "SourceCount": diagnostics.get("SourceCount"),
        "CompletedPhaseCount": diagnostics.get("CompletedPhaseCount"),
        "BlockedPhaseCount": diagnostics.get("BlockedPhaseCount"),
        "TotalRiskCount": diagnostics.get("TotalRiskCount"),
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
        "NextPhase": "Phase21 AI OS Final Package Report",
        "updated_at": datetime.now().isoformat(),
        "DiagnosticsPath": str(diagnostics_path) if diagnostics_path else None,
    }

    out_path = REPORT_DIR / f"ai_os_stability_finalization_completion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== AI OS Stability Finalization Completion Report ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {out_path}")

if __name__ == "__main__":
    main()