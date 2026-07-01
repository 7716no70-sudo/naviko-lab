class ImprovementBridge:
    def __init__(self):
        self.name = "ImprovementBridge"
        self.connected = True

    def transfer(self, improvement: dict):
        return {
            "bridge": self.name,
            "status": "transferred",
            "target": "Original Naviko",
            "direct_write": False,
            "auto_apply": False,
            "human_approval_required": True,
            "improvement": improvement,
        }