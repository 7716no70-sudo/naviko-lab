from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase43-3 Original Safe Adoption Completion Report"
ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_diagnostics():
    files = sorted(
        REPORT_DIR.glob("original_safe_adoption_diagnostics_*.json"),
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

    diag_path, diag = load_latest_diagnostics()
    found = diag is not None

    confirmed = bool(
        diag
        and diag.get("status") == "completed"
        and diag.get("OriginalSafeAdoptionReady") is True
        and diag.get("RequiredStepsComplete") is True
        and diag.get("WorkspaceOnly") is True
        and diag.get("OriginalWrite") is False
        and diag.get("OriginalWriteBlocked") is True
        and diag.get("allow_write") is False
        and diag.get("require_human_approval") is True
        and diag.get("require_permission_policy") is True
        and diag.get("RiskCount") == 0
        and diag.get("SafeToContinue") is True
    )

    completed = found and confirmed

    report = {
        "status": "completed" if completed else "blocked",
        "phase": PHASE,
        "DiagnosticsFound": found,
        "DiagnosticsConfirmed": confirmed,
        "OriginalSafeAdoptionCompleted": completed,
        "PipelineStatus": "SAFE_ADOPTION_READY",
        "Mode": "safe_workspace_only_original_adoption",
        "Policy": {
            "WorkspaceOnly": True,
            "OriginalWrite": False,
            "OriginalWriteBlocked": True,
            "HumanApprovalRequired": True,
            "PermissionPolicyRequired": True,
            "ExternalOperation": False,
            "RealGUIOperation": False,
        },
        "RiskModel": {
            "RiskLevels": [0, 1, 2, 3, 4],
            "Auto": [0, 1],
            "Approval": [2, 3],
            "Block": [4],
            "CurrentRisk": 0,
        },
        "NextPhase": "Phase44 (Future Expansion / System Integration)",
        "source_diagnostics": str(diag_path) if diag_path else None,
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = REPORT_DIR / f"original_safe_adoption_completion_report_{ts}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original Safe Adoption Completion Report ===")
    for k, v in report.items():
        print(f"{k}: {v}")
    print(f"保存先: {out}")


if __name__ == "__main__":
    main()