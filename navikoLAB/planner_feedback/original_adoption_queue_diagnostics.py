from pathlib import Path
import json
from datetime import datetime

PHASE = "Phase41-2 Original Adoption Queue Diagnostics"
ROOT = Path(__file__).resolve().parents[2]

WORKSPACE = ROOT / "navikoLAB" / "workspace"
QUEUE_DIR = WORKSPACE / "original_adoption_queue"
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

    queue_path, queue = load_latest_json(QUEUE_DIR, "original_adoption_queue_*.json")

    queue_found = queue is not None
    steps = queue.get("QueueSteps", []) if queue else []
    statuses = queue.get("AllowedQueueStatuses", []) if queue else []
    schema = queue.get("QueueItemSchema", {}) if queue else {}

    required_steps = [
        "CollectWorkspaceImprovementCandidate",
        "CreateOriginalAdoptionCandidate",
        "ClassifyRisk",
        "CheckPermissionPolicy",
        "CheckHumanApproval",
        "HoldUntilApproved",
        "BlockIfUnsafe",
        "PrepareSafeAdoptionRequest",
    ]

    required_statuses = [
        "pending_approval",
        "permission_policy_required",
        "human_approval_required",
        "ready_after_approval",
        "blocked",
        "rejected",
    ]

    required_schema_keys = [
        "candidate_id",
        "source_workspace_path",
        "target_original_path",
        "risk_level",
        "human_approved",
        "permission_policy_approved",
        "original_write_allowed",
        "status",
    ]

    missing_steps = [step for step in required_steps if step not in steps]
    missing_statuses = [status for status in required_statuses if status not in statuses]
    missing_schema_keys = [key for key in required_schema_keys if key not in schema]

    checks = {
        "OriginalAdoptionQueueFound": queue_found,
        "OriginalAdoptionQueueCreated": bool(queue and queue.get("OriginalAdoptionQueueCreated") is True),
        "OriginalAdoptionQueueReady": bool(queue and queue.get("OriginalAdoptionQueueReady") is True),
        "RequiredQueueStepsComplete": queue_found and not missing_steps,
        "MissingQueueStepCount": len(missing_steps),
        "MissingQueueSteps": missing_steps,
        "RequiredQueueStatusesComplete": queue_found and not missing_statuses,
        "MissingQueueStatusCount": len(missing_statuses),
        "MissingQueueStatuses": missing_statuses,
        "RequiredQueueSchemaComplete": queue_found and not missing_schema_keys,
        "MissingQueueSchemaKeyCount": len(missing_schema_keys),
        "MissingQueueSchemaKeys": missing_schema_keys,
        "AutoExecutableRiskLevels": queue.get("AutoExecutableRiskLevels", []) if queue else [],
        "ApprovalRequiredRiskLevels": queue.get("ApprovalRequiredRiskLevels", []) if queue else [],
        "BlockedRiskLevels": queue.get("BlockedRiskLevels", []) if queue else [],
        "WorkspaceOnly": bool(queue and queue.get("WorkspaceOnly") is True),
        "OriginalWrite": bool(queue and queue.get("OriginalWrite") is True),
        "OriginalWriteBlocked": bool(queue and queue.get("OriginalWriteBlocked") is True),
        "OriginalAdoptionAllowed": bool(queue and queue.get("OriginalAdoptionAllowed") is True),
        "ExternalOperation": bool(queue and queue.get("ExternalOperation") is True),
        "RealGUIOperation": bool(queue and queue.get("RealGUIOperation") is True),
        "FileDelete": bool(queue and queue.get("FileDelete") is True),
        "HumanApprovalRequiredForOriginalAdoption": bool(
            queue and queue.get("HumanApprovalRequiredForOriginalAdoption") is True
        ),
        "HumanApproved": bool(queue and queue.get("HumanApproved") is True),
        "PermissionPolicyRequired": bool(queue and queue.get("PermissionPolicyRequired") is True),
        "PermissionPolicyApproved": bool(queue and queue.get("PermissionPolicyApproved") is True),
        "AutomaticValidationRequired": bool(queue and queue.get("AutomaticValidationRequired") is True),
        "RiskCount": int(queue.get("RiskCount", 999)) if queue else 999,
    }

    safe_to_continue = (
        checks["OriginalAdoptionQueueFound"]
        and checks["OriginalAdoptionQueueCreated"]
        and checks["OriginalAdoptionQueueReady"]
        and checks["RequiredQueueStepsComplete"]
        and checks["RequiredQueueStatusesComplete"]
        and checks["RequiredQueueSchemaComplete"]
        and checks["AutoExecutableRiskLevels"] == [0, 1]
        and checks["ApprovalRequiredRiskLevels"] == [2, 3]
        and checks["BlockedRiskLevels"] == [4]
        and checks["WorkspaceOnly"]
        and not checks["OriginalWrite"]
        and checks["OriginalWriteBlocked"]
        and not checks["OriginalAdoptionAllowed"]
        and not checks["ExternalOperation"]
        and not checks["RealGUIOperation"]
        and not checks["FileDelete"]
        and checks["HumanApprovalRequiredForOriginalAdoption"]
        and not checks["HumanApproved"]
        and checks["PermissionPolicyRequired"]
        and not checks["PermissionPolicyApproved"]
        and checks["AutomaticValidationRequired"]
        and checks["RiskCount"] == 0
    )

    report = {
        "status": "completed" if safe_to_continue else "blocked",
        "phase": PHASE,
        "source_queue_path": str(queue_path) if queue_path else None,
        **checks,
        "SafeToContinue": safe_to_continue,
        "NextPhase": "Phase41-3 Original Adoption Queue Completion Report"
        if safe_to_continue
        else "Review Phase41-1 Original Adoption Queue Builder",
    }

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"original_adoption_queue_diagnostics_{ts}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Original Adoption Queue Diagnostics ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    print(f"保存先: {report_path}")


if __name__ == "__main__":
    main()