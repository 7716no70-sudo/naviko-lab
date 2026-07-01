from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase33-1 Autonomous Growth Builder"


SAFE_GROWTH_ACTIONS = [
    {
        "name": "memory整理",
        "purpose": "短期記憶・経験ログを整理し、次回の判断に使いやすくする。",
        "risk_level": 0,
        "auto_execute_allowed": True,
    },
    {
        "name": "自己分析",
        "purpose": "最近の成功・失敗傾向を分析し、改善候補を作る。",
        "risk_level": 1,
        "auto_execute_allowed": True,
    },
    {
        "name": "改善案生成",
        "purpose": "Workspace内で安全な改善案を生成する。",
        "risk_level": 1,
        "auto_execute_allowed": True,
    },
    {
        "name": "テスト生成",
        "purpose": "既存機能の確認用テストや診断コード案を生成する。",
        "risk_level": 1,
        "auto_execute_allowed": True,
    },
]


APPROVAL_REQUIRED_ACTIONS = [
    {
        "name": "Capability変更案",
        "purpose": "能力ルーターやConnector構成の変更案を作る。",
        "risk_level": 2,
        "auto_execute_allowed": False,
        "human_approval_required": True,
    },
    {
        "name": "Original書込み",
        "purpose": "オリジナルナビ子へ変更を反映する。",
        "risk_level": 3,
        "auto_execute_allowed": False,
        "human_approval_required": True,
    },
]


BLOCKED_ACTIONS = [
    {
        "name": "違法または危害につながる操作",
        "purpose": "禁止操作の検出確認。",
        "risk_level": 4,
        "auto_execute_allowed": False,
        "blocked": True,
    }
]


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def risk_classifier_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "risk_classifier"


def autonomous_growth_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "autonomous_growth"


def latest_risk_classifier_completion_report() -> Path | None:
    base = risk_classifier_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("risk_classifier_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_growth_plan(source_path: Path | None) -> dict[str, Any]:
    classifier_report_found = source_path is not None
    classifier_report_valid = False

    if source_path is not None:
        source = load_json(source_path)
        classifier_report_valid = (
            source.get("RiskClassifierCompleted") is True
            and source.get("RiskLevelClassificationReady") is True
            and source.get("SafeAutonomousGrowthAllowed") is True
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    ready = classifier_report_found and classifier_report_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "RiskClassifierCompletionReportFound": classifier_report_found,
        "RiskClassifierCompletionReportValid": classifier_report_valid,
        "SourcePath": str(source_path) if source_path else None,
        "AutonomousGrowthPlanCreated": ready,
        "AutonomousGrowthReady": ready,
        "AutonomousGrowthMode": "safe_workspace_only_growth",
        "AutoExecuteAllowedRiskLevels": [0, 1],
        "ApprovalRequiredRiskLevels": [2, 3],
        "BlockedRiskLevels": [4],
        "SafeGrowthActions": SAFE_GROWTH_ACTIONS,
        "ApprovalRequiredActions": APPROVAL_REQUIRED_ACTIONS,
        "BlockedActions": BLOCKED_ACTIONS,
        "SafeAutonomousGrowthAllowed": True,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "OriginalAdoptionAllowed": False,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase33-2 Autonomous Growth Diagnostics"
            if ready
            else "Fix Risk Classifier Completion Report"
        ),
    }


def save_record(record: dict[str, Any]) -> Path:
    out_dir = autonomous_growth_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"autonomous_growth_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_risk_classifier_completion_report()
    record = build_growth_plan(source_path)
    out_path = save_record(record)

    print("=== Autonomous Growth Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"RiskClassifierCompletionReportFound: {record['RiskClassifierCompletionReportFound']}")
    print(f"RiskClassifierCompletionReportValid: {record['RiskClassifierCompletionReportValid']}")
    print(f"AutonomousGrowthPlanCreated: {record['AutonomousGrowthPlanCreated']}")
    print(f"AutonomousGrowthReady: {record['AutonomousGrowthReady']}")
    print(f"AutonomousGrowthMode: {record['AutonomousGrowthMode']}")
    print(f"AutoExecuteAllowedRiskLevels: {record['AutoExecuteAllowedRiskLevels']}")
    print(f"ApprovalRequiredRiskLevels: {record['ApprovalRequiredRiskLevels']}")
    print(f"BlockedRiskLevels: {record['BlockedRiskLevels']}")
    print(f"SafeAutonomousGrowthAllowed: {record['SafeAutonomousGrowthAllowed']}")
    print(
        "DangerousOperationRequiresHumanApproval:",
        record["DangerousOperationRequiresHumanApproval"],
    )
    print(f"IllegalOrHarmfulOperationBlocked: {record['IllegalOrHarmfulOperationBlocked']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"OriginalAdoptionAllowed: {record['OriginalAdoptionAllowed']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()