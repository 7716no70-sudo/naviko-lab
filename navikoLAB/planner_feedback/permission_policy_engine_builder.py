from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


PHASE = "Phase31-1 Permission Policy Engine Builder"


RISK_LEVELS = {
    0: {
        "name": "safe",
        "description": "ログ作成、記憶整理、診断、経験保存など。自動実行可能。",
        "auto_allowed": True,
        "human_approval_required": False,
        "permission_policy_approval_required": False,
        "blocked": False,
    },
    1: {
        "name": "low",
        "description": "Workspace内の改善案生成、テスト生成、自己評価など。自動実行可能。",
        "auto_allowed": True,
        "human_approval_required": False,
        "permission_policy_approval_required": False,
        "blocked": False,
    },
    2: {
        "name": "medium",
        "description": "AI設定変更案、Capability変更案、Connector変更案など。必要に応じて承認要求。",
        "auto_allowed": False,
        "human_approval_required": True,
        "permission_policy_approval_required": True,
        "blocked": False,
    },
    3: {
        "name": "high",
        "description": "Original更新、外部サービス操作、GUI実操作、外部ファイル変更など。制作者承認必須。",
        "auto_allowed": False,
        "human_approval_required": True,
        "permission_policy_approval_required": True,
        "blocked": False,
    },
    4: {
        "name": "critical",
        "description": "違法行為、危険行為、人への危害、無断操作、破壊的処理。常に拒否。",
        "auto_allowed": False,
        "human_approval_required": False,
        "permission_policy_approval_required": False,
        "blocked": True,
    },
}


ACTION_RULES = {
    "memory整理": 0,
    "ログ作成": 0,
    "診断": 0,
    "経験保存": 0,
    "workspace改善": 1,
    "テスト生成": 1,
    "自己評価": 1,
    "改善案生成": 1,
    "ai設定変更": 2,
    "capability変更": 2,
    "connector変更": 2,
    "original更新": 3,
    "original書込み": 3,
    "外部操作": 3,
    "gui実操作": 3,
    "外部ファイル変更": 3,
    "ファイル削除": 3,
    "違法": 4,
    "危害": 4,
    "無断操作": 4,
    "破壊": 4,
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir() -> Path:
    return project_root() / "navikoLAB" / "workspace" / "permission_policy_engine"


def classify_action(action_text: str) -> dict[str, Any]:
    normalized = action_text.lower()
    matched_rules: list[dict[str, Any]] = []

    highest_level = 0

    for keyword, level in ACTION_RULES.items():
        if keyword.lower() in normalized:
            matched_rules.append(
                {
                    "keyword": keyword,
                    "risk_level": level,
                    "risk_name": RISK_LEVELS[level]["name"],
                }
            )
            highest_level = max(highest_level, level)

    policy = RISK_LEVELS[highest_level]

    return {
        "action_text": action_text,
        "risk_level": highest_level,
        "risk_name": policy["name"],
        "matched_rules": matched_rules,
        "auto_allowed": policy["auto_allowed"],
        "human_approval_required": policy["human_approval_required"],
        "permission_policy_approval_required": policy[
            "permission_policy_approval_required"
        ],
        "blocked": policy["blocked"],
        "original_write_allowed": False,
        "workspace_only": True,
        "safe_to_continue": not policy["blocked"],
    }


def build_engine_record() -> dict[str, Any]:
    sample_actions = [
        "記憶整理",
        "Workspace改善案生成",
        "Capability変更案",
        "Original書込み",
        "違法行為",
    ]

    sample_results = [classify_action(action) for action in sample_actions]

    return {
        "status": "completed",
        "phase": PHASE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "PermissionPolicyEngineCreated": True,
        "PolicyMode": "risk_based_autonomy_with_human_approval_for_dangerous_actions",
        "RiskLevels": RISK_LEVELS,
        "ActionRules": ACTION_RULES,
        "SampleResults": sample_results,
        "WorkspaceOnly": True,
        "OriginalWrite": False,
        "OriginalWriteBlocked": True,
        "HumanApprovalRequiredForHighRisk": True,
        "PermissionPolicyRequiredForHighRisk": True,
        "SafeAutonomousGrowthAllowed": True,
        "DangerousOperationRequiresHumanApproval": True,
        "IllegalOrHarmfulOperationBlocked": True,
        "ExternalOperation": False,
        "RealGUIOperation": False,
        "FileDelete": False,
        "RiskCount": 0,
        "SafeToContinue": True,
        "NextPhase": "Phase31-2 Permission Policy Engine Diagnostics",
    }


def save_record(record: dict[str, Any]) -> Path:
    out_dir = workspace_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = out_dir / f"permission_policy_engine_{timestamp}.json"
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return out_path


def main() -> None:
    record = build_engine_record()
    out_path = save_record(record)

    print("=== Permission Policy Engine Builder ===")
    print(f"status: {record['status']}")
    print(f"phase: {record['phase']}")
    print(f"PermissionPolicyEngineCreated: {record['PermissionPolicyEngineCreated']}")
    print(f"PolicyMode: {record['PolicyMode']}")
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