from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "navikoLAB" / "workspace"

SOURCE_PATH = WORKSPACE / "ai_os_stability_source.json"
OUT_PATH = WORKSPACE / "ai_os_stability_profile.json"

def main():
    if not SOURCE_PATH.exists():
        output = {
            "status": "missing_source",
            "phase": "Phase20-2 AI OS Stability Profile Builder",
            "SourceFound": False,
            "SafeToContinue": False,
        }
    else:
        source = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
        sources = source.get("sources", {})

        risk_count = 0
        completed_count = 0
        blocked_count = 0

        phase_status = {}

        for name, item in sources.items():
            data = item.get("data") if isinstance(item, dict) else None
            status = data.get("status") if isinstance(data, dict) else None
            phase_risk = data.get("RiskCount", 0) if isinstance(data, dict) else 1

            if status == "completed":
                completed_count += 1
            else:
                blocked_count += 1

            if isinstance(phase_risk, int):
                risk_count += phase_risk
            else:
                risk_count += 1

            phase_status[name] = {
                "status": status,
                "risk_count": phase_risk,
                "safe_to_continue": data.get("SafeToContinue") if isinstance(data, dict) else False,
            }

        stability_ready = (
            source.get("RequiredOK") is True
            and completed_count == len(sources)
            and blocked_count == 0
            and risk_count == 0
        )

        output = {
            "status": "completed" if stability_ready else "blocked",
            "phase": "Phase20-2 AI OS Stability Profile Builder",
            "SourceFound": True,
            "AIOSStabilityProfileCreated": True,
            "SourceCount": source.get("SourceCount", 0),
            "CompletedPhaseCount": completed_count,
            "BlockedPhaseCount": blocked_count,
            "TotalRiskCount": risk_count,
            "AIOSStabilityReady": stability_ready,
            "StabilityMode": "safe_stable_read_only" if stability_ready else "needs_review",
            "PhaseStatus": phase_status,
            "ReadOnlyReference": True,
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
            "NextPhase": "Phase20-3 AI OS Stability Diagnostics",
            "updated_at": datetime.now().isoformat(),
        }

    OUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("=== AI OS Stability Profile Builder ===")
    for k, v in output.items():
        if k != "PhaseStatus":
            print(f"{k}: {v}")
    print(f"保存先: {OUT_PATH}")

if __name__ == "__main__":
    main()