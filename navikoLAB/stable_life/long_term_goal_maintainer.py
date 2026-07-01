# navikoLAB/stable_life/long_term_goal_maintainer.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class LongTermGoalMaintainer:
    def __init__(self, root: str | Path = "navikoLAB"):
        self.root = Path(root)

        self.personality_path = (
            self.root
            / "stable_life"
            / "personality"
            / "stable_personality.json"
        )

        self.goal_dir = self.root / "stable_life" / "goals"
        self.goal_dir.mkdir(parents=True, exist_ok=True)

        self.goal_path = self.goal_dir / "stable_goal_tree.json"
        self.history_path = self.goal_dir / "goal_maintenance_history.json"

    def _now(self) -> str:
        return datetime.now().isoformat(timespec="seconds")

    def load_personality(self) -> dict[str, Any]:
        if self.personality_path.exists():
            return json.loads(self.personality_path.read_text(encoding="utf-8"))
        return {}

    def default_goal_tree(self) -> dict[str, Any]:
        return {
            "dream": "Self-Existing Life Systemとして安定して成長し続ける",
            "long_term": [
                "壊れずに継続動作する",
                "経験から人格と価値観を形成する",
                "ナオさんを支える相棒AIとして成長する",
            ],
            "mid_term": [
                "Stable Life Kernelを完成させる",
                "意味記憶と経験学習を人格へ接続する",
                "自己修復と継続監視を実装する",
            ],
            "short_term": [
                "現在の人格状態を維持する",
                "経験学習の反映を安全範囲に抑える",
                "次の工程に進める状態を保つ",
            ],
            "today": [
                "Phase115を安全に進める",
                "各工程の診断を通す",
                "既存構造を壊さず新規追加で拡張する",
            ],
            "updated_at": self._now(),
        }

    def load_goal_tree(self) -> dict[str, Any]:
        if self.goal_path.exists():
            return json.loads(self.goal_path.read_text(encoding="utf-8"))
        return self.default_goal_tree()

    def maintain(self) -> dict[str, Any]:
        personality = self.load_personality()
        goals = self.load_goal_tree()

        before = json.loads(json.dumps(goals, ensure_ascii=False))

        creative_confidence = float(personality.get("creative_confidence", 0.4))
        stability = float(personality.get("stability", 0.6))
        repair_orientation = float(personality.get("repair_orientation", 0.5))
        continuity_drive = float(personality.get("continuity_drive", 0.6))

        added_today: list[str] = []
        added_short: list[str] = []

        if creative_confidence >= 0.41:
            added_today.append("創造経験を意味記憶として蓄積する")
            added_short.append("創造性を安定した能力として育てる")

        if stability >= 0.60:
            added_today.append("安定状態を維持しながら次工程へ進む")
            added_short.append("安定した成功パターンを保持する")

        if repair_orientation >= 0.50:
            added_today.append("異常時に診断できる構造を準備する")

        if continuity_drive >= 0.60:
            added_today.append("時間的連続性を目標管理へ反映する")
            added_short.append("継続存在モデルを日次目標へ接続する")

        goals["today"] = self._merge_unique(goals.get("today", []), added_today)
        goals["short_term"] = self._merge_unique(goals.get("short_term", []), added_short)

        goals["updated_at"] = self._now()

        self.goal_path.write_text(
            json.dumps(goals, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        self._save_history(before, goals, personality, added_today, added_short)

        return {
            "status": "completed",
            "phase": "Phase115-4 Long-Term Goal Maintainer",
            "GoalTreeMaintained": True,
            "TodayGoalCount": len(goals.get("today", [])),
            "ShortTermGoalCount": len(goals.get("short_term", [])),
            "AddedToday": added_today,
            "AddedShortTerm": added_short,
            "SavedPath": str(self.goal_path),
            "SafeToContinue": True,
        }

    def _merge_unique(self, base: list[str], additions: list[str]) -> list[str]:
        merged = list(base)
        for item in additions:
            if item not in merged:
                merged.append(item)
        return merged

    def _save_history(
        self,
        before: dict[str, Any],
        after: dict[str, Any],
        personality: dict[str, Any],
        added_today: list[str],
        added_short: list[str],
    ) -> None:
        if self.history_path.exists():
            data = json.loads(self.history_path.read_text(encoding="utf-8"))
        else:
            data = {"count": 0, "items": []}

        data["items"].append(
            {
                "created_at": self._now(),
                "personality_snapshot": personality,
                "added_today": added_today,
                "added_short_term": added_short,
                "before": before,
                "after": after,
            }
        )
        data["count"] = len(data["items"])

        self.history_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def main() -> None:
    maintainer = LongTermGoalMaintainer()
    result = maintainer.maintain()

    print("=== Long-Term Goal Maintainer ===")
    for key, value in result.items():
        if isinstance(value, list):
            print(f"{key}:")
            for item in value:
                print(f"- {item}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()