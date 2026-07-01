from pathlib import Path
from datetime import datetime
import json

from navikoLAB.core.autonomous_capability_flow import AutonomousCapabilityFlow


class MultiAICompletionReport:
    """
    第19工程 MultiAI統合の完成診断レポート。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        self.report_dir = (
            self.root_dir
            / "reports"
        )
        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def run_diagnosis(self):
        mission = {
            "id": "multi_ai_completion_diagnosis",
            "title": "YouTube用の短い紹介動画を作りたい",
            "description": "ChatGPT、画像AI、動画AIを使って紹介動画を作成する",
            "status": "active"
        }

        flow = AutonomousCapabilityFlow(
            root_dir=self.root_dir.parent
        )

        result = flow.run(
            mission
        )

        checks = {
            "capability_flow": bool(result),
            "required_capabilities": bool(result.get("required_capabilities")),
            "agent_result": bool(result.get("agent_result")),
            "execution_result": bool(result.get("execution_result")),
            "multi_ai_result": bool(result.get("multi_ai_result")),
            "artifacts": bool(result.get("artifacts", {}).get("merged_output")),
            "multi_ai_reflection": bool(result.get("multi_ai_reflection")),
            "multi_ai_improvement_request": bool(result.get("multi_ai_improvement_request"))
        }

        completed_count = sum(1 for value in checks.values() if value)
        total_count = len(checks)

        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": "completed" if completed_count == total_count else "partial",
            "completion_rate": round(completed_count / total_count * 100, 1),
            "checks": checks,
            "flow_result": result
        }

    def format_report(self, diagnosis):
        flow = diagnosis.get("flow_result", {})

        lines = []
        lines.append("=== 第19工程 MultiAI統合 完成診断レポート ===")
        lines.append(f"保存日時: {diagnosis.get('timestamp')}")
        lines.append("")
        lines.append(f"状態: {diagnosis.get('status')}")
        lines.append(f"完成率: {diagnosis.get('completion_rate')}%")
        lines.append("")

        lines.append("【診断項目】")
        for key, value in diagnosis.get("checks", {}).items():
            lines.append(f"- {key}: {'OK' if value else 'NG'}")

        lines.append("")
        lines.append("【Mission】")
        lines.append(f"Mission ID: {flow.get('mission_id')}")
        lines.append(f"Title: {flow.get('mission_title')}")

        lines.append("")
        lines.append("【Capability】")
        lines.append(f"必要能力: {flow.get('required_capabilities')}")
        lines.append(f"不足能力: {flow.get('missing_capabilities')}")
        lines.append(f"推奨Agent: {flow.get('recommended_agents')}")

        lines.append("")
        lines.append("【MultiAI】")
        multi_ai = flow.get("multi_ai_result", {})
        lines.append(f"状態: {multi_ai.get('status')}")
        lines.append(f"出力数: {multi_ai.get('output_count')}")

        lines.append("")
        lines.append("【Reflection】")
        reflection = flow.get("multi_ai_reflection", {})
        lines.append(f"状態: {reflection.get('status')}")
        lines.append(f"スコア: {reflection.get('score')}")
        lines.append(f"良かった点: {reflection.get('good_points')}")
        lines.append(f"改善点: {reflection.get('improvement_points')}")

        lines.append("")
        lines.append("【Improvement】")
        improvement = flow.get("multi_ai_improvement_request", {})
        lines.append(f"状態: {improvement.get('status')}")
        lines.append(f"優先度: {improvement.get('priority')}")
        lines.append(f"保存先: {improvement.get('file_path')}")

        lines.append("")
        lines.append("【総合判定】")
        if diagnosis.get("status") == "completed":
            lines.append("第19工程 MultiAI統合は完成状態です。")
        else:
            lines.append("第19工程 MultiAI統合には未完了項目があります。")

        return "\n".join(lines)

    def save_report(self):
        diagnosis = self.run_diagnosis()
        report_text = self.format_report(
            diagnosis
        )

        report_file = (
            self.report_dir
            / (
                "multi_ai_completion_report_"
                + datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".txt"
            )
        )

        report_file.write_text(
            report_text,
            encoding="utf-8"
        )

        return {
            "diagnosis": diagnosis,
            "report_text": report_text,
            "report_file": str(report_file)
        }