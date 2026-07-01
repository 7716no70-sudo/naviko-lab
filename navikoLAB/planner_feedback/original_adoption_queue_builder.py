from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase41-1 Original Adoption Queue Builder"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
QUEUE_DIR = WORKSPACE / "original_adoption_queue"
REPORT_DIR = ROOT / "navikoLAB" / "planner_feedback" / "reports"


def load_latest_phase40_completion():
    files = sorted(
        REPORT_DIR.glob("long_term_self_evolution_completion_report_*.json"),
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
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    phase40_path, phase40 = load_latest_phase40_completion()

    phase40_ready = bool(
        phase40
        and phase40.get("status") == "completed"
        and phase40.get("LongTermSelfEvolutionReady") is True
        and phase40.get("WorkspaceOnly") is True
        and phase40.get("OriginalWrite") is False
        and phase40.get("OriginalWriteBlocked") is True
        and phase40.get("RiskCount") == 0
        and phase40.get("SafeToContinue") is True
    )

    queue = {
        "phase": PHASE,
        "OriginalAdoptionQueueCreated": phase40_ready,
        "OriginalAdoptionQueueReady": phase40_ready,
        "QueueMode": "safe_workspace_only_original_adoption_queue",
        "QueuePurpose": "Manage Original adoption candidates without writing to Original.",
        "QueueSteps": [
            "CollectWorkspaceImprovementCandidate",
            "CreateOriginalAdoptionCandidate",
            "ClassifyRisk",
            "CheckPermissionPolicy",
            "CheckHumanApproval",
            "HoldUntilApproved",
            "BlockIfUnsafe",
            "PrepareSafeAdoptionRequest",
        ],
        "QueueItemSchema": {
            "candidate_id": "string",
            "source_workspace_path": "string",
            "target_original_path": "string_or_none",
            "risk_level": "0_to_4",
            "human_approved": False,
            "permission_policy_approved": False,
            "original_write_allowed": False,
            "status": "pending_approval",
        },
        "AllowedQueueStatuses": [
            "pending_approval",
            "permission_policy_required",
            "human_approval_required",
            "ready_after_approval",
            "blocked",
            "rejected",
        ],
        "AutoExecutableRiskLevels": [0, 1],
        "ApprovalRequiredRiskLevels": [2, 3],
        "BlockedRiskLevels": [4],
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "HumanApproved": False,
        "PermissionPolicyRequired": True,
        "PermissionPolicyApproved": False,
        "AutomaticValidationRequired": True,
        "RiskCount": 0 if phase40_ready else 1,
        "SafeToContinue": phase40_ready,
        "SourcePhase40CompletionPath": str(phase40_path) if phase40_path else None,
        "NextPhase": "Phase41-2 Original Adoption Queue Diagnostics"
        if phase40_ready
        else "Review Phase40 Completion Report",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    queue_path = QUEUE_DIR / f"original_adoption_queue_{ts}.json"
    queue_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    report_path = REPORT_DIR / f"original_adoption_queue_builder_report_{ts}.json"
    report_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original Adoption Queue Builder ===")
    print(f"status: {'completed' if phase40_ready else 'blocked'}")
    for key, value in queue.items():
        print(f"{key}: {value}")
    print(f"保存先: {queue_path}")
    print(f"レポート保存先: {report_path}")


if __name__ == "__main__":
    main()