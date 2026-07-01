from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADOPTION_DIR = ROOT / "navikoLAB" / "original_adoption"
REQUEST_DIR = ADOPTION_DIR / "requests"


FEATURES = [
    {
        "name": "MissionManager",
        "risk": "medium",
        "purpose": "目的をMissionとして管理する",
        "integration_type": "import_call",
        "target": "navikoLAB.missions",
    },
    {
        "name": "CapabilityRouter",
        "risk": "medium",
        "purpose": "目的に必要な能力を選定する",
        "integration_type": "import_call",
        "target": "navikoLAB.capabilities",
    },
    {
        "name": "AgentManager",
        "risk": "medium",
        "purpose": "利用可能なAIエージェントを管理する",
        "integration_type": "import_call",
        "target": "navikoLAB.capabilities",
    },
    {
        "name": "AgentExecutor",
        "risk": "medium",
        "purpose": "選択されたエージェントを実行する",
        "integration_type": "import_call",
        "target": "navikoLAB.capabilities",
    },
    {
        "name": "MultiAIOrchestrator",
        "risk": "medium",
        "purpose": "複数AIの処理を統合する",
        "integration_type": "import_call",
        "target": "navikoLAB.multi_ai",
    },
    {
        "name": "MultiAIReflection",
        "risk": "low",
        "purpose": "成果物を評価する",
        "integration_type": "import_call",
        "target": "navikoLAB.multi_ai",
    },
    {
        "name": "MultiAIImprovementRequest",
        "risk": "low",
        "purpose": "改善要求を生成する",
        "integration_type": "import_call",
        "target": "navikoLAB.multi_ai",
    },
    {
        "name": "AutonomousCapabilityFlow",
        "risk": "low",
        "purpose": "Missionから成果物生成までを安全に接続する",
        "integration_type": "import_call",
        "target": "navikoLAB.capabilities",
    },
]


INTEGRATION_ORDER = [
    "MissionManager",
    "CapabilityRouter",
    "AgentManager",
    "AgentExecutor",
    "MultiAIOrchestrator",
    "MultiAIReflection",
    "MultiAIImprovementRequest",
    "AutonomousCapabilityFlow",
]


def build_original_adoption_request() -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    return {
        "request_id": f"original_adoption_request_{now}",
        "status": "requested",
        "created_at": now,
        "project": "オリジナルナビ子 完全自律進化AIプロジェクト",
        "phase": "第20工程-2 original_adoption_request 作成",
        "policy": {
            "do_not_expand_naviko_py": True,
            "use_import_connection": True,
            "add_new_features_under_navikoLAB": True,
            "require_human_approval": True,
            "require_syntax_check": True,
            "require_startup_test": True,
            "require_rollback_ready": True,
        },
        "integration_order": INTEGRATION_ORDER,
        "features": FEATURES,
        "safety_summary": {
            "high_risk": 0,
            "medium_risk": 5,
            "low_risk": 3,
            "allowed": True,
            "reason": "high risk が0件であり、import方式による安全接続方針のため申請可能。",
        },
        "next_step": "第20工程-3 オリジナル反映シミュレーション",
    }


def save_original_adoption_request() -> Path:
    REQUEST_DIR.mkdir(parents=True, exist_ok=True)

    request = build_original_adoption_request()
    output_path = REQUEST_DIR / f"{request['request_id']}.json"

    output_path.write_text(
        json.dumps(request, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path


def main() -> None:
    output_path = save_original_adoption_request()

    print("=== original_adoption_request 作成 ===")
    print("状態: requested")
    print(f"保存先: {output_path}")
    print("反映順序:")
    for index, name in enumerate(INTEGRATION_ORDER, start=1):
        print(f"{index}. {name}")

    print("安全判定: allowed")
    print("次工程: 第20工程-3 オリジナル反映シミュレーション")


if __name__ == "__main__":
    main()