from pathlib import Path
import json
from datetime import datetime

class AppOperatorExperienceSaver:
    def __init__(self, experience_dir=None):
        self.experience_dir = Path(experience_dir or Path(__file__).resolve().parents[1] / "experience")
        self.experience_dir.mkdir(parents=True, exist_ok=True)

    def save(self, reflection):
        experience = {
            "status": "saved",
            "category": "app_operator",
            "title": "AppOperator dry_run approval pipeline completed",
            "learned_patterns": [
                "Level1 actions can proceed through auto dry_run",
                "Level2 and Level3 actions should wait for approval",
                "Level4 actions should be rejected or require strict approval",
                "Executor must not perform real GUI operations while dry_run is True",
            ],
            "safety_principles": [
                "Human approval is required before real GUI operation",
                "External operation must remain False during diagnostics",
                "Dangerous actions must be blocked by default",
            ],
            "source_reflection": reflection,
            "saved_at": datetime.now().isoformat(timespec="seconds"),
        }

        path = self.experience_dir / f"app_operator_experience_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(experience, ensure_ascii=False, indent=2), encoding="utf-8")
        return experience, str(path)