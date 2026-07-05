from pathlib import Path
from navikoLAB.task_planner import TaskPlanner
from navikoLAB.planner_feedback.capability_feedback_adapter import (
    adapt_capability_selection_with_feedback,
)

try:
    from navikoLAB.capabilities.capability_connector import CapabilityConnector
except ImportError:
    from capability_connector import CapabilityConnector


class CapabilityRouter:
    """
    目的に応じて必要な外部能力を選択するクラス
    """

    def __init__(self, root_dir):

        self.root_dir = Path(root_dir)

        self.connector = CapabilityConnector(
            self.root_dir
        )

    def detect_required_capabilities(self, purpose):

        text = purpose.lower()

        required = ["chatgpt"]

        if "アプリ" in text or "app" in text or "ツール" in text:
            required.append("app_operator")

        if "ゲーム" in text or "game" in text:
            required.append("app_operator")

        if "画像" in text or "イラスト" in text or "image" in text:
            required.append("image_ai")

        if "動画" in text or "youtube" in text or "video" in text:
            required.append("video_ai")
            required.append("image_ai")

        if "音声" in text or "ナレーション" in text or "voice" in text:
            required.append("voice_ai")

        if "調査" in text or "検索" in text or "research" in text:
            required.append("browser")

        if "ai" in text or "人工知能" in text or "エージェント" in text:
            required.append("chatgpt")

        unique_required = []

        for capability_id in required:
            if capability_id not in unique_required:
                unique_required.append(capability_id)

        return unique_required

    def route(self, purpose):

        required_ids = self.detect_required_capabilities(
            purpose
        )

        planner = TaskPlanner(self.root_dir)
        plan = planner.create_plan(purpose)

        # DISABLED: planner_feedback module removed
        # capability_feedback = adapt_capability_selection_with_feedback(
        #     plan,
        #     required_ids,
        # )
        capability_feedback = {}  # Fallback to empty dict

        selected = []
        missing = []

        for capability_id in required_ids:

            capability = self.connector.find_by_id(
                capability_id
            )

            if capability and capability.get("enabled"):
                selected.append(capability)
            else:
                missing.append(capability_id)

        return {
            "purpose": purpose,
            "required_ids": required_ids,
            "selected": selected,
            "missing": missing,
            "selected_count": len(selected),
            "missing_count": len(missing),
            "capability_feedback": capability_feedback,
            "feedback_based_selection": True,
            "experience_based_score": capability_feedback.get(
                "experience_based_score",
                0,
            ),
            "feedback_priority": capability_feedback.get(
                "feedback_priority",
                "low",
            )
        }

    def diagnose(self):

        connector_diagnosis = self.connector.diagnose()

        return {
            "router_status": "ok",
            "connector": connector_diagnosis
        }