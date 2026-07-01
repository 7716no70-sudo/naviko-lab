class ReflectionBridge:
    def __init__(self):
        self.name = "ReflectionBridge"
        self.connected = True

    def transfer(self, reflection: dict):
        return {
            "bridge": self.name,
            "status": "transferred",
            "target": "Original Naviko",
            "direct_write": False,
            "reflection": reflection,
        }