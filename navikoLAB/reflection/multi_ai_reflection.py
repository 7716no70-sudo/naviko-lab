from pathlib import Path
from datetime import datetime
import json


class MultiAIReflection:
    """
    MultiAI成果物を評価するReflection。
    現段階では安全なルールベース評価。
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)

        self.reflection_dir = (
            self.root_dir
            / "reflection"
        )
        self.reflection_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        self.history_file = (
            self.reflection_dir
            / "multi_ai_reflection_history.json"
        )

    def evaluate(self, mission, artifacts):
        merged_output = artifacts.get(
            "merged_output",
            ""
        )

        outputs = artifacts.get(
            "outputs",
            []
        )

        good_points = []
        improvement_points = []

        if merged_output:
            good_points.append(
                "MultiAIの統合成果物が生成されている。"
            )
        else:
            improvement_points.append(
                "統合成果物 merged_output が空です。"
            )

        if len(outputs) >= 2:
            good_points.append(
                "複数AIの成果物を統合できている。"
            )
        else:
            improvement_points.append(
                "複数AI連携としては出力数が不足しています。"
            )

        if "chatgpt" in merged_output.lower():
            good_points.append(
                "テキスト生成AIの成果が含まれている。"
            )

        if "image_ai" in merged_output.lower():
            good_points.append(
                "画像AIの成果が含まれている。"
            )

        if "video_ai" in merged_output.lower():
            good_points.append(
                "動画AIの成果が含まれている。"
            )

        if not improvement_points:
            improvement_points.append(
                "現段階ではmock成果物のため、次工程で実成果物生成へ接続する。"
            )

        result = {
            "timestamp": datetime.now().isoformat(),
            "mission_id": mission.get("id", "unknown"),
            "mission_title": mission.get("title", ""),
            "status": "reflected",
            "artifact_length": len(merged_output),
            "output_count": len(outputs),
            "good_points": good_points,
            "improvement_points": improvement_points,
            "score": self.calculate_score(
                merged_output,
                outputs
            )
        }

        self.save_history(result)

        return result

    def calculate_score(self, merged_output, outputs):
        score = 0

        if merged_output:
            score += 40

        if len(outputs) >= 2:
            score += 30

        if len(outputs) >= 3:
            score += 20

        if len(merged_output) >= 100:
            score += 10

        return min(score, 100)

    def save_history(self, result):
        history = []

        if self.history_file.exists():
            try:
                history = json.loads(
                    self.history_file.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                history = []

        history.append(result)

        self.history_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=2
            ),
            encoding="utf-8"
        )