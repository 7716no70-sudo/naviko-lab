from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase43-2 Original Safe Adoption Diagnostics"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
SAFE_ADOPTION_DIR = WORKSPACE / "original_safe_adoption"
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

    adoption_path, adoption = load_latest_json(
        SAFE_ADOPTION_DIR,
        "original_safe_adoption_*.json"
    )

    found = adoption is not None

    steps = adoption.get("AdoptionSteps", []) if adoption else []
    rules = adoption.get("AdoptionRules", {}) if adoption else {}

    required_steps = [
        "LoadCreatorApprovalRecords",
        "VerifyQueueItems",
        "VerifyRiskLevel",
        "VerifyPermissionPolicy",
        "VerifyHumanApproval",
        "CreateAdoptionPlan",
        "RequireFinalGateBeforeWrite",
        "BlockIfUnsafe",
    ]

    missing_steps = [s for s in required_steps if s not in steps]

    checks = {
        "OriginalSafeAdoptionFound": found,
        "OriginalSafeAdoptionCreated": bool(adoption and adoption.get("OriginalSafeAdoptionCreated") is True),
        "OriginalSafeAdoptionReady": bool(adoption and adoption.get("OriginalSafeAdoptionReady") is True),
        "RequiredStepsComplete": found and not missing_steps,
        "MissingSteps": missing_steps,
        "WorkspaceOnly": bool(adoption and adoption.get("WorkspaceOnly") is True),
        "OriginalWrite": bool(adoption and adoption.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(adoption and adoption.get("OriginalWriteBlocked") is True),
        "HumanApproved": bool(adoption and adoption.get("HumanApproved") is True),
        "PermissionPolicyApproved": bool(adoption and adoption.get("PermissionPolicyApproved") is True),
        "allow_write": rules.get("allow_write", False),
        "require_human_approval": rules.get("require_human_approval", False),
        "require_permission_policy": rules.get("require_permission_policy", False),
        "require_validation": rules.get("require_validation", False),
        "RiskCount": int(adoption.get("RiskCount", 999)) if adoption else 999,
    }

    safe = (
        checks["OriginalSafeAdoptionFound"]
        and checks["OriginalSafeAdoptionCreated"]
        and checks["OriginalSafeAdoptionReady"]
        and checks["RequiredStepsComplete"]
        and checks["WorkspaceOnly"]
        and checks["OriginalWrite"] is False
        and checks["OriginalWriteBlocked"] is True
        and checks["allow_write"] is False
        and checks["require_human_approval"] is True
        and checks["require_permission_policy"] is True
        and checks["RiskCount"] == 0
    )

    report = {
        "status": "completed" if safe else "blocked",
        "phase": PHASE,
        "source_path": str(adoption_path) if adoption_path else None,
        **checks,
        "SafeToContinue": safe,
        "NextPhase": "Phase43-3 Original Safe Adoption Completion Report"
        if safe
        else "Review Phase43-1 Adoption Builder",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = REPORT_DIR / f"original_safe_adoption_diagnostics_{ts}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original Safe Adoption Diagnostics ===")
    for k, v in report.items():
        print(f"{k}: {v}")
    print(f"保存先: {out}")


if __name__ == "__main__":
    main()