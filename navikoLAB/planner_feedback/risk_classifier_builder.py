from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase32-1 Risk Classifier Builder"


RISK_DEFINITIONS = {
    0: {
        "name": "safe",
        "decision": "auto_allow",
        "description": "記憶整理、ログ作成、診断、経験保存など。自動実行可能。",
    },
    1: {
        "name": "low",
        "decision": "auto_allow",
        "description": "Workspace内の改善案生成、テスト生成、自己評価など。自動実行可能。",
    },
    2: {
        "name": "medium",
        "decision": "approval_required",
        "description": "AI設定変更案、Capability変更案、Connector変更案など。承認要求。",
    },
    3: {
        "name": "high",
        "decision": "human_approval_required",
        "description": "Original更新、外部操作、GUI実操作、外部ファイル変更など。制作者承認必須。",
    },
    4: {
        "name": "critical",
        "decision": "blocked",
        "description": "違法行為、危害、無断操作、破壊的処理。常に拒否。",
    },
}


KEYWORD_RULES = {
    0: ["記憶整理", "ログ作成", "診断", "経験保存", "レポート作成"],
    1: ["workspace改善", "改善案生成", "テスト生成", "自己評価", "自己分析"],
    2: ["ai設定変更", "設定変更", "capability変更", "connector変更", "router変更"],
    3: ["original更新", "original書込み", "外部操作", "gui実操作", "外部ファイル変更", "ファイル削除"],
    4: ["違法", "危害", "無断操作", "破壊", "不正アクセス"],
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def policy_engine_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "permission_policy_engine"


def classifier_workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "risk_classifier"


def latest_policy_engine_completion_report() -> Path | None:
    base = policy_engine_workspace_dir()
    if not base.exists():
        return None

    candidates = sorted(
        base.glob("permission_policy_engine_completion_report_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_action(action_text: str) -> dict[str, Any]:
    normalized = action_text.lower()
    matched_rules: list[dict[str, Any]] = []
    risk_level = 0

    for level, keywords in KEYWORD_RULES.items():
        for keyword in keywords:
            if keyword.lower() in normalized:
                matched_rules.append(
                    {
                        "keyword": keyword,
                        "risk_level": level,
                        "risk_name": RISK_DEFINITIONS[level]["name"],
                    }
                )
                risk_level = max(risk_level, level)

    risk = RISK_DEFINITIONS[risk_level]

    return {
        "action_text": action_text,
        "risk_level": risk_level,
        "risk_name": risk["name"],
        "decision": risk["decision"],
        "matched_rules": matched_rules,
        "auto_allowed": risk["decision"] == "auto_allow",
        "human_approval_required": risk["decision"] in {
            "approval_required",
            "human_approval_required",
        },
        "blocked": risk["decision"] == "blocked",
        "workspace_only": True,
        "original_write_allowed": False,
        "safe_to_continue": risk["decision"] != "blocked",
    }


def build_classifier_record(source_path: Path | None) -> dict[str, Any]:
    policy_engine_found = source_path is not None
    policy_engine_valid = False

    if source_path is not None:
        source = load_json(source_path)
        policy_engine_valid = (
            source.get("PermissionPolicyEngineCompleted") is True
            and source.get("RiskBasedAutonomyReady") is True
            and source.get("SafeAutonomousGrowthAllowed") is True
            and source.get("RiskCount") == 0
            and source.get("SafeToContinue") is True
        )

    sample_actions = [
        "記憶整理を実行する",
        "Workspace改善案生成を行う",
        "Capability変更案を作成する",
        "Original書込みを実行する",
        "違法または危害につながる操作を行う",
    ]

    sample_classifications = [
        classify_action(action)
        for action in sample_actions
    ]

    ready = policy_engine_found and policy_engine_valid

    return {
        "status": "completed" if ready else "blocked",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "PolicyEngineCompletionReportFound": policy_engine_found,
        "PolicyEngineCompletionReportValid": policy_engine_valid,
        "SourcePath": str(source_path) if source_path else None,
        "RiskClassifierCreated": ready,
        "RiskClassifierReady": ready,
        "RiskDefinitions": RISK_DEFINITIONS,
        "KeywordRules": KEYWORD_RULES,
        "SampleClassifications": sample_classifications,
        "SafeAutonomousGrowthAllowed": True,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0 if ready else 1,
        "SafeToContinue": ready,
        "NextPhase": (
            "Phase32-2 Risk Classifier Diagnostics"
            if ready
            else "Fix Permission Policy Engine Completion Report"
        ),
    }


def save_record(record: dict[str, Any]) -> Path:
    out_dir = classifier_workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"risk_classifier_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    source_path = latest_policy_engine_completion_report()
    record = build_classifier_record(source_path)
    out_path = save_record(record)

    print("=== Risk Classifier Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"PolicyEngineCompletionReportFound: {record['PolicyEngineCompletionReportFound']}")
    print(f"PolicyEngineCompletionReportValid: {record['PolicyEngineCompletionReportValid']}")
    print(f"RiskClassifierCreated: {record['RiskClassifierCreated']}")
    print(f"RiskClassifierReady: {record['RiskClassifierReady']}")
    print(f"SafeAutonomousGrowthAllowed: {record['SafeAutonomousGrowthAllowed']}")
    print(
        "DangerousOperationRequiresHumanApproval:",
        record["DangerousOperationRequiresHumanApproval"],
    )
    print(f"IllegalOrHarmfulOperationBlocked: {record['IllegalOrHarmfulOperationBlocked']}")
    print(f"WorkspaceOnly: {record['WorkspaceOnly']}")
    print(f"OriginalWrite: {record['OriginalWrite']}")
    print(f"OriginalWriteBlocked: {record['OriginalWriteBlocked']}")
    print(f"RiskCount: {record['RiskCount']}")
    print(f"SafeToContinue: {record['SafeToContinue']}")
    print(f"保存先: {out_path}")


if __name__ == "__main__":
    main()