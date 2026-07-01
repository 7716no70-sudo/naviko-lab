from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase43-1 Original Safe Adoption Builder"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
SAFE_ADOPTION_DIR = WORKSPACE / "original_safe_adoption"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_phase42_completion():
    files = sorted(
        REPORT_DIR.glob("creator_approval_ui_completion_report_*.json"),
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
    SAFE_ADOPTION_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase42_path, phase42 = load_latest_phase42_completion()

    phase42_ready = bool(
        phase42
        and phase42.get("status") == "completed"
        and phase42.get("CreatorApprovalUIReady") is True
        and phase42.get("WorkspaceOnly") is True
        and phase42.get("OriginalWrite") is False
        and phase42.get("OriginalWriteBlocked") is True
        and phase42.get("HumanApproved") is False
        and phase42.get("PermissionPolicyApproved") is False
        and phase42.get("RiskCount") == 0
        and phase42.get("SafeToContinue") is True
    )

    adoption = {
        "phase": PHASE,
        "OriginalSafeAdoptionCreated": phase42_ready,
        "OriginalSafeAdoptionReady": phase42_ready,
        "AdoptionMode": "safe_workspace_only_original_adoption",
        "AdoptionPurpose": "Prepare safe original adoption pipeline without executing writes.",
        "AdoptionSteps": [
            "LoadCreatorApprovalRecords",
            "VerifyQueueItems",
            "VerifyRiskLevel",
            "VerifyPermissionPolicy",
            "VerifyHumanApproval",
            "CreateAdoptionPlan",
            "RequireFinalGateBeforeWrite",
            "BlockIfUnsafe",
        ],
        "AdoptionRules": {
            "allow_write": False,
            "require_human_approval": True,
            "require_permission_policy": True,
            "require_validation": True,
            "workspace_only": True,
        },
        "AutoExecutableRiskLevels": [0, 1],
        "ApprovalRequiredRiskLevels": [2, 3],
        "BlockedRiskLevels": [4],
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "HumanApproved": False,
        "PermissionPolicyApproved": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if phase42_ready else 1,
        "SafeToContinue": phase42_ready,
        "SourcePhase42CompletionPath": str(phase42_path) if phase42_path else None,
        "NextPhase": "Phase43-2 Original Safe Adoption Diagnostics"
        if phase42_ready
        else "Review Phase42 Completion Report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    adoption_path = SAFE_ADOPTION_DIR / f"original_safe_adoption_{ts}.json"
    adoption_path.write_text(json.dumps(adoption, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / f"original_safe_adoption_builder_report_{ts}.json"
    report_path.write_text(json.dumps(adoption, ensure_ascii=False), encoding="utf-8")

    print("=== Original Safe Adoption Builder ===")
    print(f"status: {'completed' if phase42_ready else 'blocked'}")
    for k, v in adoption.items():
        print(f"{k}: {v}")
    print(f"保存先: {adoption_path}")
    print(f"レポート保存先: {report_path}")


if __name__ == "__main__":
    main()