from datetime import datetime
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
RELEASE_DIR = ROOT / "navikoLAB" / "release"
REPORT_DIR = RELEASE_DIR / "reports"


class ReleaseCandidateManager:
    def __init__(self):
        self.version = "v2.0-rc1"
        self.stage = "第40工程 Release Candidate v2.0"
        self.release_name = "Original Naviko Release Candidate"

    def create_manifest(self):
        manifest = {
            "status": "release_candidate_created",
            "version": self.version,
            "release_name": self.release_name,
            "stage": self.stage,
            "created_at": datetime.now().isoformat(),
            "includes": {
                "MissionManager": True,
                "TaskPlanner": True,
                "CapabilityRouter": True,
                "ConnectorDispatcher": True,
                "SearchDispatcher": True,
                "BrowserConnector": True,
                "DeepSearchEngine": True,
                "KnowledgeBase": True,
                "ExperienceManager": True,
                "KnowledgeReflection": True,
                "AutoImprovementSuggestion": True,
                "AutoRefactoringPlan": True,
                "OriginalNavikoBridge": True,
                "HumanApprovalWorkflow": True,
                "FinalSafetyAudit": True,
                "LongTermKnowledge": True,
            },
            "safety_policy": {
                "original_direct_write": False,
                "auto_apply": False,
                "human_approval_required": True,
                "backup_required": True,
                "syntax_check_required": True,
                "startup_check_required": True,
                "rollback_required": True,
            },
            "connector_status": {
                "ChatGPT": "api_key_not_set",
                "Claude": "api_key_not_set",
                "Gemini": "api_key_not_set",
                "Grok": "api_key_not_set",
                "Browser": "ready",
                "Image": "mock",
                "Video": "mock",
                "Voice": "not_implemented",
                "AppOperator": "mock",
            },
        }

        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        path = REPORT_DIR / f"release_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        return manifest, path


if __name__ == "__main__":
    manager = ReleaseCandidateManager()
    manifest, path = manager.create_manifest()

    print("=== Release Candidate Manager ===")
    print("状態:", manifest["status"])
    print("Version:", manifest["version"])
    print("工程:", manifest["stage"])
    print("保存先:", path)