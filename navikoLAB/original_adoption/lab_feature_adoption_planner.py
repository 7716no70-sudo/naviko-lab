from pathlib import Path
from datetime import datetime
import json


class LabFeatureAdoptionPlanner:
    """
    LAB完成機能をオリジナルナビ子へ安全反映するための候補整理。
    まだ反映は行わない。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        self.adoption_dir = (
            self.root_dir
            / "original_adoption"
        )
        self.adoption_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def collect_features(self):
        features = [
            {
                "name": "MissionManager",
                "status": "completed",
                "risk": "medium",
                "target": "navikoLAB/core",
                "reason": "Mission生成・状態管理を行う中核機能"
            },
            {
                "name": "CapabilityRouter",
                "status": "completed",
                "risk": "medium",
                "target": "navikoLAB/capabilities",
                "reason": "目的から必要能力を判定する機能"
            },
            {
                "name": "AgentManager_AgentExecutor",
                "status": "completed",
                "risk": "medium",
                "target": "navikoLAB/capabilities",
                "reason": "選択Agentのmock実行基盤"
            },
            {
                "name": "MultiAIOrchestrator",
                "status": "completed",
                "risk": "medium",
                "target": "navikoLAB/capabilities",
                "reason": "複数AI成果物の統合基盤"
            },
            {
                "name": "MultiAIReflection",
                "status": "completed",
                "risk": "low",
                "target": "navikoLAB/reflection",
                "reason": "MultiAI成果物の評価"
            },
            {
                "name": "MultiAIImprovementRequest",
                "status": "completed",
                "risk": "low",
                "target": "navikoLAB/improvements",
                "reason": "Reflection結果から改善要求を生成"
            },
            {
                "name": "CapabilityGUI",
                "status": "completed",
                "risk": "low",
                "target": "naviko.py GUI",
                "reason": "Capability状態をGUI表示する機能"
            },
            {
                "name": "AutonomousCapabilityFlow",
                "status": "completed",
                "risk": "medium",
                "target": "navikoLAB/core",
                "reason": "MissionからImprovement要求までを統合する流れ"
            }
        ]

        return features

    def create_plan(self):
        features = self.collect_features()

        high_risk = [
            item for item in features
            if item.get("risk") == "high"
        ]

        medium_risk = [
            item for item in features
            if item.get("risk") == "medium"
        ]

        low_risk = [
            item for item in features
            if item.get("risk") == "low"
        ]

        plan = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": "planned",
            "purpose": "LAB完成機能をオリジナルナビ子へ安全反映するための候補整理",
            "features": features,
            "feature_count": len(features),
            "risk_summary": {
                "high": len(high_risk),
                "medium": len(medium_risk),
                "low": len(low_risk)
            },
            "recommended_strategy": [
                "naviko.pyへ巨大コードを直接追加しない",
                "新機能はnavikoLAB配下のモジュールとして維持する",
                "オリジナルnaviko.pyにはimportと呼び出しだけ追加する",
                "まず診断系・表示系から反映する",
                "次にAutonomousCapabilityFlowを安全モードで接続する",
                "外部API実行はまだmockのまま維持する"
            ],
            "next_step": "original_adoption_request を作成する"
        }

        file_path = self.save_plan(plan)

        plan["file_path"] = str(file_path)

        return plan

    def save_plan(self, plan):
        file_path = (
            self.adoption_dir
            / (
                "lab_feature_adoption_plan_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".json"
            )
        )

        file_path.write_text(
            json.dumps(
                plan,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return file_path

    def format_plan(self, plan):
        lines = []
        lines.append("=== LAB機能 オリジナル反映計画 ===")
        lines.append(f"状態: {plan.get('status')}")
        lines.append(f"機能数: {plan.get('feature_count')}")
        lines.append(f"リスク: {plan.get('risk_summary')}")
        lines.append(f"保存先: {plan.get('file_path')}")
        lines.append("")

        lines.append("【反映候補】")
        for item in plan.get("features", []):
            lines.append(
                f"- {item.get('name')} / {item.get('status')} / risk={item.get('risk')}"
            )

        lines.append("")
        lines.append("【推奨反映方針】")
        for item in plan.get("recommended_strategy", []):
            lines.append(f"- {item}")

        lines.append("")
        lines.append(f"次工程: {plan.get('next_step')}")

        return "\n".join(lines)