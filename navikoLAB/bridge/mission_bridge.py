class MissionBridge:
    def __init__(self):
        self.name = "MissionBridge"
        self.connected = True

    def transfer(self, mission: dict):
        return {
            "bridge": self.name,
            "status": "transferred",
            "target": "Original Naviko",
            "direct_write": False,
            "mission": mission,
        }