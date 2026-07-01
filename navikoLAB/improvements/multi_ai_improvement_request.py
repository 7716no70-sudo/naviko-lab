from pathlib import Path
from datetime import datetime
import json


class MultiAIImprovementRequest:
    """
    MultiAIReflectionの結果からImprovement要求を生成する。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        self.improvement_dir = (
            self.root_dir
            / "improvements"
        )
        self.improvement_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_request(self, mission, reflection):
        request = {
            "timestamp": datetime.now().isoformat(),
            "source": "multi_ai_reflection",
            "mission_id": mission.get("id", "unknown"),
            "mission_title": mission.get("title", ""),
            "reflection_status": reflection.get("status", "unknown"),
            "reflection_score": reflection.get("score", 0),
            "good_points": reflection.get("good_points", []),
            "improvement_points": reflection.get("improvement_points", []),
            "request_type": "multi_ai_improvement",
            "priority": self.detect_priority(reflection),
            "status": "requested",
            "suggested_next_actions": self.create_next_actions(reflection)
        }

        file_path = self.save_request(request)

        request["file_path"] = str(file_path)

        return request

    def detect_priority(self, reflection):
        score = reflection.get("score", 0)

        if score >= 90:
            return "low"

        if score >= 60:
            return "medium"

        return "high"

    def create_next_actions(self, reflection):
        actions = []

        for item in reflection.get("improvement_points", []):
            actions.append(
                {
                    "reason": item,
                    "action": "該当改善点を次回BuildまたはConnector実装に反映する"
                }
            )

        if not actions:
            actions.append(
                {
                    "reason": "明確な改善点なし",
                    "action": "現状維持し、次の高度化工程へ進む"
                }
            )

        return actions

    def save_request(self, request):
        file_name = (
            "multi_ai_improvement_request_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )

        file_path = self.improvement_dir / file_name

        file_path.write_text(
            json.dumps(
                request,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )

        return file_path