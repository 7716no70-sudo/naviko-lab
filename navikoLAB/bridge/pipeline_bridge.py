from navikoLAB.bridge.mission_bridge import MissionBridge
from navikoLAB.bridge.knowledge_bridge import KnowledgeBridge
from navikoLAB.bridge.reflection_bridge import ReflectionBridge
from navikoLAB.bridge.improvement_bridge import ImprovementBridge


class PipelineBridge:
    def __init__(self):
        self.name = "PipelineBridge"
        self.mission_bridge = MissionBridge()
        self.knowledge_bridge = KnowledgeBridge()
        self.reflection_bridge = ReflectionBridge()
        self.improvement_bridge = ImprovementBridge()

    def transfer_pipeline(self, payload: dict):
        return {
            "bridge": self.name,
            "status": "pipeline_transferred",
            "target": "Original Naviko",
            "direct_write": False,
            "auto_apply": False,
            "human_approval_required": True,
            "mission": self.mission_bridge.transfer(payload.get("mission", {})),
            "knowledge": self.knowledge_bridge.transfer(payload.get("knowledge", {})),
            "reflection": self.reflection_bridge.transfer(payload.get("reflection", {})),
            "improvement": self.improvement_bridge.transfer(payload.get("improvement", {})),
        }


if __name__ == "__main__":
    bridge = PipelineBridge()
    result = bridge.transfer_pipeline({
        "mission": {"goal": "TODOアプリを作りたい"},
        "knowledge": {"summary": "GUIアプリ生成に関する知識"},
        "reflection": {"result": "改善候補あり"},
        "improvement": {"proposal": "安全な最小差分改善"},
    })

    print("=== PipelineBridge Test ===")
    print("状態:", result["status"])
    print("対象:", result["target"])
    print("直接書込:", result["direct_write"])
    print("人間承認必須:", result["human_approval_required"])