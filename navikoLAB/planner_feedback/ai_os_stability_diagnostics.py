from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_PATH = WORKSPACE / "ai_os_stability_profile.json"

def main():
    profile_found = PROFILE_PATH.exists()

    if not profile_found:
        output = {
            "status": "missing_profile",
            "phase": "Phase20-3 AI OS Stability Diagnostics",
            "ProfileFound": False,
            "SafeToContinue": False,
        }
    else:
        profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

        risk_flags = [
            profile.get("OriginalWrite") is True,
            profile.get("PlannerWriteAllowed") is True,
            profile.get("CapabilityRouterWriteAllowed") is True,
            profile.get("ConnectorDispatcherWriteAllowed") is True,
            profile.get("FileDelete") is True,
            profile.get("ExternalOperation") is True,
            profile.get("RealGUIOperation") is True,
            profile.get("RiskCount", 1) != 0,
            profile.get("TotalRiskCount", 1) != 0,
        ]

        risk_count = sum(1 for flag in risk_flags if flag)

        stability_ready = (
            profile.get("AIOSStabilityReady") is True
            and profile.get("StabilityMode") == "safe_stable_read_only"
            and risk_count == 0
        )

        output = {
            "status": "completed" if stability_ready else "blocked",
            "phase": "Phase20-3 AI OS Stability Diagnostics",
            "ProfileFound": True,
            "AIOSStabilityDiagnosticsCompleted": True,
            "AIOSStabilityReady": profile.get("AIOSStabilityReady"),
            "StabilityMode": profile.get("StabilityMode"),
            "SourceCount": profile.get("SourceCount"),
            "CompletedPhaseCount": profile.get("CompletedPhaseCount"),
            "BlockedPhaseCount": profile.get("BlockedPhaseCount"),
            "TotalRiskCount": profile.get("TotalRiskCount"),
            "ReadOnlyReference": profile.get("ReadOnlyReference"),
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "PlannerWriteAllowed": False,
            "CapabilityRouterWriteAllowed": False,
            "ConnectorDispatcherWriteAllowed": False,
            "FileDelete": False,
            "ExternalOperation": False,
            "RealGUIOperation": False,
            "RiskCount": risk_count,
            "SafeToContinue": stability_ready,
            "NextPhase": "Phase20-4 AI OS Stability Finalization Completion Report",
            "updated_at": datetime.now().isoformat(),
        }

    out_path = REPORT_DIR / f"ai_os_stability_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== AI OS Stability Diagnostics ===")
    for k, v in output.items():
        print(f"{k}: {v}")
    print(f"保存先: {out_path}")

if __name__ == "__main__":
    main()