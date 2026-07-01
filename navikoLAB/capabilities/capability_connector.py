import json
from pathlib import Path
from datetime import datetime


class CapabilityConnector:
    """
    外部能力接続管理クラス

    現段階では実API接続は行わず、
    どの能力が使えるか・何に向いているかを管理する。
    """

    def __init__(self, root_dir):

        self.root_dir = Path(root_dir)

        self.capability_dir = self.root_dir / "capabilities"
        self.capability_dir.mkdir(parents=True, exist_ok=True)

        self.registry_file = self.capability_dir / "capability_registry.json"
        self.history_file = self.capability_dir / "capability_history.json"

        self.capabilities = self.load_or_create_registry()

    def load_or_create_registry(self):

        if self.registry_file.exists():
            try:
                return json.loads(
                    self.registry_file.read_text(
                        encoding="utf-8"
                    )
                )
            except Exception:
                pass

        capabilities = self.default_capabilities()

        self.registry_file.write_text(
            json.dumps(
                capabilities,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

        return capabilities

    def default_capabilities(self):

        return [
            {
                "id": "chatgpt",
                "name": "ChatGPT",
                "type": "text_ai",
                "enabled": True,
                "status": "mock",
                "strengths": [
                    "reasoning",
                    "coding",
                    "writing",
                    "planning"
                ]
            },
            {
                "id": "claude",
                "name": "Claude",
                "type": "text_ai",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "long_context",
                    "writing",
                    "analysis"
                ]
            },
            {
                "id": "gemini",
                "name": "Gemini",
                "type": "text_ai",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "multimodal",
                    "search",
                    "analysis"
                ]
            },
            {
                "id": "grok",
                "name": "Grok",
                "type": "text_ai",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "realtime",
                    "social_trends"
                ]
            },
            {
                "id": "image_ai",
                "name": "Image Generation AI",
                "type": "image",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "image_generation",
                    "illustration",
                    "design"
                ]
            },
            {
                "id": "video_ai",
                "name": "Video Generation AI",
                "type": "video",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "video_generation",
                    "editing_plan",
                    "storyboard"
                ]
            },
            {
                "id": "voice_ai",
                "name": "Voice AI",
                "type": "voice",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "speech",
                    "narration",
                    "voice_generation"
                ]
            },
            {
                "id": "browser",
                "name": "Browser Operator",
                "type": "browser",
                "enabled": False,
                "status": "not_connected",
                "strengths": [
                    "web_search",
                    "research",
                    "site_operation"
                ]
            },
            {
                "id": "app_operator",
                "name": "App Operator",
                "type": "app",
                "enabled": True,
                "status": "mock",
                "strengths": [
                    "app_operation",
                    "file_operation",
                    "workflow"
                ]
            }
        ]

    def save(self):

        self.registry_file.write_text(
            json.dumps(
                self.capabilities,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    def save_history(self, action, detail=None):

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

        history.append(
            {
                "time": datetime.now().isoformat(),
                "action": action,
                "detail": detail or {}
            }
        )

        self.history_file.write_text(
            json.dumps(
                history,
                ensure_ascii=False,
                indent=4
            ),
            encoding="utf-8"
        )

    def list_capabilities(self):

        return self.capabilities

    def get_enabled_capabilities(self):

        return [
            capability
            for capability in self.capabilities
            if capability.get("enabled")
        ]

    def find_by_id(self, capability_id):

        for capability in self.capabilities:
            if capability.get("id") == capability_id:
                return capability

        return None

    def enable_capability(self, capability_id):

        capability = self.find_by_id(capability_id)

        if not capability:
            return False

        capability["enabled"] = True
        capability["status"] = "mock"

        self.save()

        self.save_history(
            "enable_capability",
            {
                "capability_id": capability_id
            }
        )

        return True

    def disable_capability(self, capability_id):

        capability = self.find_by_id(capability_id)

        if not capability:
            return False

        capability["enabled"] = False
        capability["status"] = "disabled"

        self.save()

        self.save_history(
            "disable_capability",
            {
                "capability_id": capability_id
            }
        )

        return True

    def diagnose(self):

        enabled_count = 0
        type_count = {}

        for capability in self.capabilities:

            if capability.get("enabled"):
                enabled_count += 1

            cap_type = capability.get("type", "unknown")

            type_count[cap_type] = type_count.get(
                cap_type,
                0
            ) + 1

        return {
            "capability_count": len(self.capabilities),
            "enabled_count": enabled_count,
            "disabled_count": len(self.capabilities) - enabled_count,
            "type_count": type_count,
            "registry_file": str(self.registry_file),
            "history_file": str(self.history_file)
        }