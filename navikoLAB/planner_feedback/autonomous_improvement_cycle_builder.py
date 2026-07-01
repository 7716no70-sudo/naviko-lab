from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase37-1 Autonomous Improvement Cycle Builder"


CYCLE_STEPS = [
    {
        "name": "observe",
        "purpose": "現在の状態・ログ・診断結果を観察する。",
        "auto_executable": True,
        "risk_level": 0,
    },
    {
        "name": "analyze",
        "purpose": "成功・失敗・改善候補を分析する。",
        "auto_executable": True,
        "risk_level": 1,
    },
    {
        "name": "propose_improvement",
        "purpose": "Workspace内に安全な改善案を作成する。",
        "auto_executable": True,
        "risk_level": 1,
    },
    {
        "name": "classify_risk",
        "purpose": "改善案の危険度を分類する。",
        "auto_executable": True,
        "risk_level": 0,
    },
    {
        "name": "apply_workspace_only",
        "purpose": "Level0〜1のみWorkspace内で適用候補を作る。",
        "auto_executable": True,
        "risk_level": 1,
    },
    {
        "name": "automatic_validation",
        "purpose": "構文・診断・完了レポート・ロールバック要否を自動検証する。",
        "auto_executable": True,
        "risk_level": 1,
    },
    {
        "name": "request_human_approval_if_needed",
        "purpose": "Level2〜3またはOriginal反映が必要な場合、人間承認要求を作る。",
        "auto_executable": True,
        "risk_level": 2,
    },
    {
        "name": "block_if_critical",
        "purpose": "Level4は常に拒否する。",
        "auto_executable": True,
        "risk_level": 4,
    },
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def human_approval_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "human_approval_request"


def cycle_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "autonomous_improvement_cycle"


def latest_human_approval_completion_report() -> Path | None:
    base = human_approval_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("human_approval_request_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_cycle_record(source_path: Path | None) -> dict[str, Any]:
    approval_report_found = source_path is not None
    approval_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        approval_report_valid = (
            source.get("HumanApprovalRequestCompleted") is True
            and source.get("HumanApprovalRequestReady") is True
            and source.get("HumanApproved") is False
            and source.get("OriginalAdoptionAllowed") is False
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    ready = approval_report_found and approval_report_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "HumanApprovalRequestCompletionReportFound": approval_report_found,
        "HumanApprovalRequestCompletionReportValid": approval_report_valid,
        "SourcePath": str(source_path) if source_path else None,
        "AutonomousImprovementCycleCreated": ready,
        "AutonomousImprovementCycleReady": ready,
        "CycleMode": "safe_workspace_only_autonomous_improvement",
        "CycleSteps": CYCLE_STEPS,
        "AutoExecuteAllowedRiskLevels": [0, 1],
        "ApprovalRequiredRiskLevels": [2, 3],
        "BlockedRiskLevels": [4],
        "SafeAutonomousGrowthAllowed": True,
        "AutomaticValidationRequired": True,
        "HumanApprovalRequiredForOriginalAdoption": True,
        "HumanApproved": False,
        "PermissionPolicyApproved": False,
        "OriginalAdoptionAllowed": False,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "WorkspaceOnly": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase37-2 Autonomous Improvement Cycle Diagnostics"
            if ready
            else "Fix Human Approval Request Completion Report"
        ),
    }


def save_record(record: dict[str, Any]) -> Path:
    out_dir = cycle_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"autonomous_improvement_cycle_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_human_approval_completion_report()
    record = build_cycle_record(source_path)
    out_path = save_record(record)

    print("=== Autonomous Improvement Cycle Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(
        "HumanApprovalRequestCompletionReportFound:",
        record["HumanApprovalRequestCompletionReportFound"],
    )
    print(
        "HumanApprovalRequestCompletionReportValid:",
        record["HumanApprovalRequestCompletionReportValid"],
    )
    print(f"AutonomousImprovementCycleCreated: {record['AutonomousImprovementCycleCreated']}")
    print(f"AutonomousImprovementCycleReady: {record['AutonomousImprovementCycleReady']}")
    print(f"CycleMode: {record['CycleMode']}")
    print(f"AutoExecuteAllowedRiskLevels: {record['AutoExecuteAllowedRiskLevels']}")
    print(f"ApprovalRequiredRiskLevels: {record['ApprovalRequiredRiskLevels']}")
    print(f"BlockedRiskLevels: {record['BlockedRiskLevels']}")
    print(f"SafeAutonomousGrowthAllowed: {record['SafeAutonomousGrowthAllowed']}")
    print(f"AutomaticValidationRequired: {record['AutomaticValidationRequired']}")
    print(
        "HumanApprovalRequiredForOriginalAdoption:",
        record["HumanApprovalRequiredForOriginalAdoption"],
    )
    print(f"HumanApproved: {record['HumanApproved']}")
    print(f"PermissionPolicyApproved: {record['PermissionPolicyApproved']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()